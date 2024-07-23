import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_user_can_create_comment(
    news, author_client, form_data, author, detail_url_fix
):
    response = author_client.post(detail_url_fix, data=form_data)
    assertRedirects(response, f'{detail_url_fix}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(form_data, client, detail_url_fix):
    response = client.post(detail_url_fix, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={detail_url_fix}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(author_client, detail_url_fix):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url_fix, data=bad_words_data)
    assertFormError(
        response, form='form', field='text', errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(
    detail_url_fix, author_client, comment, form_data
):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, detail_url_fix + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    not_author_client, form_data, comment
):
    url = reverse('news:edit', args=(comment.id,))
    old_text = comment.text
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert old_text == comment.text


def test_author_can_delete_comment(comment, author_client, detail_url_fix):
    url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(url)
    assertRedirects(response, detail_url_fix + '#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
