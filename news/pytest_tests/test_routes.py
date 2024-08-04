from http import HTTPStatus

from pytest_django.asserts import assertRedirects
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, url, expected_status',
    (
        (
            pytest.lazy_fixture('client'), pytest.lazy_fixture('detail_url'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('client'), pytest.lazy_fixture('home_url'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('client'), pytest.lazy_fixture('login_url'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('client'), pytest.lazy_fixture('logout_url'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('client'), pytest.lazy_fixture('signup_url'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('client'),
            pytest.lazy_fixture('comment_edit_url'), HTTPStatus.FOUND
        ),
        (
            pytest.lazy_fixture('client'),
            pytest.lazy_fixture('comment_delete_url'), HTTPStatus.FOUND
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('comment_edit_url'), HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('comment_delete_url'), HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('comment_edit_url'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('comment_delete_url'), HTTPStatus.NOT_FOUND
        )
    )
)
def test_availability(user, expected_status, url, login_url):
    response = user.get(url)
    assert response.status_code == expected_status
    if expected_status == HTTPStatus.FOUND:
        redirect_url = f'{login_url}?next={url}'
        assertRedirects(response, redirect_url)
