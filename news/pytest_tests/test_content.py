import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_authorized_client_has_form(author_client, detail_url_fix):
    response = author_client.get(detail_url_fix)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url_fix):
    response = client.get(detail_url_fix)
    assert 'form' not in response.context


def test_comments_order(comment_list, client, detail_url_fix):
    response = client.get(detail_url_fix)
    assert 'news' in response.context
    all_timestamps = [comment.created for comment in comment_list]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_news_count(news_list, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(news_list, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
