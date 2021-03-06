"""
Authentication Functions
"""

import json
import traceback
from functools import wraps
from flask import abort
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request
)
from flask import current_app
from werkzeug.security import check_password_hash

USERS = [
    {
        'username': 'admin',
        'password': 'admin',
        'enabled': True,
        'is_admin': True
    },
    {
        'username': 'user',
        'password': 'user',
        'enabled': True,
        'is_admin': False
    }
]


class AuthenticationError(Exception):
    """Base Authentication Exception"""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.msg) + ')'


class InvalidCredentials(AuthenticationError):
    """Invalid username/password"""


class AccountInactive(AuthenticationError):
    """Account is disabled"""


class AccessDenied(AuthenticationError):
    """Access is denied"""


class UserNotFound(AuthenticationError):
    """User identity not found"""


def authenticate_user(username, password):
    """
    Authenticate a user
    """
    employee_info = None
    sql_base = "select get_employee_password('{0}')"
    loginname = json.dumps({"loginname": username})
    sql_str = sql_base.format(loginname)
    try:
        employee_info = current_app.db.query_one(sql_str)
    except Exception:
        current_app.logger.error(traceback.format_exc())

    if len(employee_info[0]):
        # print(employee_info, "employee_info>>")
        db_passwd = employee_info[0][0]['password']
        if db_passwd == password:
            return (
                create_access_token(identity=username),
                create_refresh_token(identity=username)
            )
        else:
            raise AccountInactive(username)
    else:
        raise InvalidCredentials()


def get_authenticated_user():
    """
    Get authentication token user identity and verify account is active
    """
    identity = get_jwt_identity()

    if identity:
        return identity
    else:
        raise AccountInactive()


def deauthenticate_user():
    """
    Log user out
    in a real app, set a flag in user database requiring login, or
    implement token revocation scheme
    """
    identity = get_jwt_identity()
    current_app.logger.debug('logging user "%s" out', identity)


def refresh_authentication():
    """
    Refresh authentication, issue new access token
    """
    user = get_authenticated_user()
    return create_access_token(identity=user['username'])


def auth_required(func):
    """
    View decorator - require valid access token
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            # get_authenticated_user()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            current_app.logger.error('authorization failed: %s', error)
            abort(403)

    return wrapper


def auth_refresh_required(func):
    """
    View decorator - require valid refresh token
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request()
        try:
            get_authenticated_user()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            current_app.logger.error('authorization failed: %s', error)
            abort(403)

    return wrapper


def admin_required(func):
    """
    View decorator - required valid access token and admin access
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            user = get_authenticated_user()
            if user['is_admin']:
                return func(*args, **kwargs)
            else:
                abort(403)
        except (UserNotFound, AccountInactive) as error:
            current_app.logger.error('authorization failed: %s', error)
            abort(403)

    return wrapper
