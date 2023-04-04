from datetime import datetime, timedelta
from typing import Dict
from unittest.mock import Mock

import inject
import pytest

from src.domain.user.output.user_repository import UserRepository
from src.domain.user.user import User, Token
from src.domain.user.user_service_impl import UserServiceImpl
from src.domain.utils.exceptions import ApplicationError


@pytest.fixture
def mock_user_repository() -> Mock:
    return Mock()


@pytest.fixture
def injector(
        mock_user_repository: Mock
) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(UserRepository, mock_user_repository)

    inject.clear_and_configure(config)


@pytest.fixture
def user_test() -> User:
    return User(
        username='test',
        password='123456'
    )


@pytest.fixture
def token_response() -> Token:
    return Token(
        token='jwt123456'
    )


@pytest.fixture
def decoded_token() -> Dict:
    return {
        'exp': datetime.utcnow() + timedelta(days=0, seconds=5), 'iat': datetime.utcnow(), 'sub': 'uid123'
    }


class TestUserServiceImpl:

    def test_should_return_token_when_sign_in_is_success(
            self, injector: None, mock_user_repository: Mock, user_test: User, token_response: Token
    ) -> None:
        user_id = 'uid123'

        mock_user_repository.check_user.return_value = user_id
        mock_user_repository.generate_token.return_value = token_response

        token = UserServiceImpl().sign_in(user_test)

        assert token_response.token == token.token
        mock_user_repository.check_user.assert_called_once_with(user_test)
        mock_user_repository.generate_token.assert_called_once_with(user_id)

    def test_should_return_application_error_when_credentials_are_wrong(
            self, injector: None, mock_user_repository: Mock, user_test: User
    ) -> None:
        mock_user_repository.check_user.return_value = None

        with pytest.raises(ApplicationError) as app_error:
            UserServiceImpl().sign_in(user_test)
        assert app_error.value.status_code == 403
        assert app_error.value.message == "Wrong credentials"
        mock_user_repository.check_user.assert_called_once_with(user_test)

    def test_should_return_application_error_when_token_generation_failed(
            self, injector: None, mock_user_repository: Mock, user_test: User
    ) -> None:
        user_id = 'uid123'

        mock_user_repository.check_user.return_value = user_id
        mock_user_repository.generate_token.return_value = None

        with pytest.raises(ApplicationError) as app_error:
            UserServiceImpl().sign_in(user_test)
        assert app_error.value.status_code == 403
        assert app_error.value.message == "A problem occurred generating the token"
        mock_user_repository.check_user.assert_called_once_with(user_test)
        mock_user_repository.generate_token.assert_called_once_with(user_id)

    def test_should_sign_out(
            self, injector: None, mock_user_repository: Mock, token_response: Token, decoded_token: Dict
    ) -> None:
        mock_user_repository.decode_token.return_value = decoded_token
        mock_user_repository.remove_token.return_value = None

        UserServiceImpl().sign_out(token_response)

        mock_user_repository.decode_token.assert_called_once_with(token_response.token)
        mock_user_repository.remove_token.assert_called_once_with(token_response.token, decoded_token)

    def test_should_return_application_error_when_decoding_token(
            self, injector: None, mock_user_repository: Mock, token_response: Token, decoded_token: Dict
    ) -> None:
        mock_user_repository.decode_token.return_value = None

        with pytest.raises(ApplicationError) as app_error:
            UserServiceImpl().sign_out(token_response)

        assert app_error.value.status_code == 403
        assert app_error.value.message == "A problem occurred decoding the token"
        mock_user_repository.decode_token.assert_called_once_with(token_response.token)
