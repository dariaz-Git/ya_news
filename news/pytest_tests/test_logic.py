import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_user_can_create_comment(
    news, author_client, form_data, author, detail_url
):
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    form_data, client, detail_url, login_url
):
    response = client.post(detail_url, data=form_data)
    expected_url = f'{login_url}?next={detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'bad_word', BAD_WORDS
)
def test_user_cant_use_bad_words(author_client, detail_url, bad_word):
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response, form='form', field='text', errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(
    detail_url, author_client, comment, form_data, comment_edit_url
):
    response = author_client.post(comment_edit_url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert Comment.objects.count() == 1


def test_user_cant_edit_comment_of_another_user(
    not_author_client, form_data, comment, comment_edit_url
):
    old_text = comment.text
    response = not_author_client.post(comment_edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert old_text == comment.text


def test_author_can_delete_comment(
    author_client, detail_url, comment_delete_url
):
    response = author_client.post(comment_delete_url)
    assertRedirects(response, detail_url + '#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_delete_url
):
    response = not_author_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
