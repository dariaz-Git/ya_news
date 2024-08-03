from http import HTTPStatus

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        (pytest.lazy_fixture('detail_url')),
        (pytest.lazy_fixture('home_url')),
        (pytest.lazy_fixture('login_url')),
        (pytest.lazy_fixture('logout_url')),
        (pytest.lazy_fixture('signup_url')),
    )
)
def test_home_page_availability_for_anonymous_user(
    client, url
):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'user, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('client'), HTTPStatus.FOUND),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'url', (
        (pytest.lazy_fixture('comment_edit_url')),
        (pytest.lazy_fixture('comment_delete_url'))
    )
)
def test_availability_for_comment_edit_and_delete(
    user, expected_status, url
):
    response = user.get(url)
    assert response.status_code == expected_status

# "Проверки ВСЕХ статус кодов достаточно реализовать в 1 параметризованном
# методе. В качестве параметров стоит объявить запрашиваемый url, клиент
# (аноним, автор или подписчик), и ожидаемый ответ ."
# Только delete/edit объединила
# Все статус кода реализовывать не стала, потому что лишком сложным и
# громоздким получается в едином целом
