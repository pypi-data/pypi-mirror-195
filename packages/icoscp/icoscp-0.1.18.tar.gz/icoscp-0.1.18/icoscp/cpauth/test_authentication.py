import base64
import os
import json

import pandas
import pytest

from icoscp.cpauth.authentication import Authentication
from icoscp.cpauth.exceptions import AuthenticationError, CredentialsError
from icoscp.cpb.dobj import Dobj
from icoscp.station import station

configuration_file = os.path.join(os.path.expanduser('~'),
                                  'icoscp',
                                  '.icos_carbon_portal')


def write_config(path: str = None, content: dict = None):
    with open(file=path, mode='w') as json_file_handle:
        json.dump(content, json_file_handle)
    return


def encode_password(password: str = None) -> str:
    """Base64 encode given password."""
    password_bytes = password.encode(encoding='utf-8')
    b64_password_bytes = base64.b64encode(password_bytes)
    b64_password_string = b64_password_bytes.decode(encoding='utf-8')
    return b64_password_string


def test_args_correct_username_and_password():
    cp_auth = Authentication(username='zoiszogop@gmail.com', password='login-test')
    assert cp_auth.valid_token
    return


def test_args_incorrect_username_and_correct_password():
    with pytest.raises(AuthenticationError) as exc_info:
        Authentication(username='zoiszogop@gmail.co', password='login-test')
        assert exc_info.type is AuthenticationError
    return


def test_args_correct_username_and_incorrect_password():
    with pytest.raises(AuthenticationError) as exc_info:
        Authentication(username='zoiszogop@gmail.com', password='login-tes')
        assert exc_info.type is AuthenticationError
    return


def test_args_incorrect_username_and_incorrect_password():
    with pytest.raises(AuthenticationError) as exc_info:
        Authentication(username='zoiszogop@gmail.co', password='login-tes')
        assert exc_info.type is AuthenticationError
    return


def test_file_correct_username_and_password():
    credentials = dict({
        'username': 'zoiszogop@gmail.com',
        'password': 'login-test',
        'token': None
    })
    with open(file=configuration_file, mode='w') as json_file_handle:
        json.dump(credentials, json_file_handle)
    cp_auth = Authentication()
    assert cp_auth.valid_token
    os.remove(configuration_file)
    return

# Something weird is going on with this test. The encoded password,
# although correctly decoded (at least in the debugger) gives back
# 403 error for correct(?) credentials.
# def test_file_correct_username_and_encoded_password():
#     credentials = dict({
#         'username': 'zoiszogop@gmail',
#         'password': 'bG9naW4tdGVzdA==',
#         'token': None
#     })
#     write_config(path=configuration_file, content=credentials)
#     cp_auth = Authentication()
#     assert cp_auth.valid_token
#     # os.remove(configuration_file)
#     return


def test_file_incorrect_username_and_password():
    credentials = dict({
        'username': 'zoiszogop@gmail.',
        'password': 'wrong-password',
        'token': None
    })
    with open(file=configuration_file, mode='w') as json_file_handle:
        json.dump(credentials, json_file_handle)
    match = 'Incorrect user name or password'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication()
        assert exc_info.type is AuthenticationError
    os.remove(configuration_file)
    return


def test_file_incorrect_username_and_correct_password():
    credentials = dict({
        'username': 'zoiszogop@gmail.',
        'password': 'login-test',
        'token': None
    })
    write_config(path=configuration_file, content=credentials)
    match = 'Incorrect user name or password'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication()
        assert exc_info.type is AuthenticationError
    os.remove(configuration_file)
    return


def test_file_correct_username_and_incorrect_password():
    credentials = dict({
        'username': 'zoiszogop@gmail.com',
        'password': 'wrong-password',
        'token': None
    })
    write_config(path=configuration_file, content=credentials)
    match = 'Incorrect user name or password'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication()
        assert exc_info.type is AuthenticationError
    os.remove(configuration_file)
    return


def test_wronly_formatted_input_token():
    invalid_token = (
        'cpauthToken=WzE2Nzc3NjY2NTU3OTgsInpvaXN6b2dvcEBnbWFpbC5jb20iLCJQYXNz'
        'd29yZCJdHm3+8d6DcN01oEE4e2vHt8Zlk1rsC8boVkuwxGAoO4hXI+VenpfS+MjgHTrK'
        'OdF4b/H2t/RMdQukPhaXIAlkGML22fBcvYmrwlQGVFFNoYN7bY12z7/HibPr9EbVeerT'
        'ujDwLW0xuCZ+Pppb776pUULCVuFbF3lfeN9SMg+AS6HZa1PNfV8up0RNitk2sWlv+rda'
        'NDPjH0zK0u6S2H78wiWWh2PWzQME65IiDxVGAi5bA9ijzei7RIg+97b9/vjCrNILTz4n'
        'yal8mCGaaWuJZjJsnYe0eItc8lUN5E6PC+9OCQ2oLhgzLMrEFeGTOBW17kG+wUF9NZSX'
        'P6J4h7pK0='
    )
    match = 'Invalid token format. Please re-enter your token.'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication(token=invalid_token)
        assert exc_info.type is AuthenticationError
    return


def test_missing_token():
    # Missing token means that this: "cpauthToken" part of the token
    # is missing. The message from https://cpauth.icos-cp.eu/whoami
    # says that Authentication cookie is missing.
    invalid_token = (
        'WzE2Nzc3NjY2NTU3OTgsInpvaXN6b2dvcEBnbWFpbC5jb20iLCJQYXNz'
        'd29yZCJdHm3+8d6DcN01oEE4e2vHt8Zlk1rsC8boVkuwxGAoO4hXI+VenpfS+MjgHTrK'
        'OdF4b/H2t/RMdQukPhaXIAlkGML22fBcvYmrwlQGVFFNoYN7bY12z7/HibPr9EbVeerT'
        'ujDwLW0xuCZ+Pppb776pUULCVuFbF3lfeN9SMg+AS6HZa1PNfV8up0RNitk2sWlv+rda'
        'NDPjH0zK0u6S2H78wiWWh2PWzQME65IiDxVGAi5bA9ijzei7RIg+97b9/vjCrNILTz4n'
        'yal8mCGaaWuJZjJsnYe0eItc8lUN5E6PC+9OCQ2oLhgzLMrEFeGTOBW17kG+wUF9NZSX'
        'P6J4h7pK0='
    )
    match = 'Invalid token format. Please re-enter your token.'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication(token=invalid_token)
        assert exc_info.type is AuthenticationError
    return


def test_expired_token():
    # Missing token means that this: "cpauthToken" part of the token
    # is missing. The message from https://cpauth.icos-cp.eu/whoami
    # says that Authentication cookie is missing.
    expired_token = (
        'cpauthToken=rO0ABXcIAAABhhzUWJ90ABN6b2lzem9nb3BAZ21haWwuY29tdAAIUGFzc3dv'
        'cmR1cgACW0Ks8xf4BghU4AIAAHhwAAABAL/GZlyjlvw3Af4LytTiGqQC6Ugf2/9oL6T/htyM'
        'C7s6OXKy3Tq0Akt0LZGqCMXJj9H2NyHXIXXs/cD8K9CKFQ4/1JIF0jmevLrOiq0ME75ZcMmo'
        'qE+zv9KRXjg052/ZUz+2VUcfAopbsQfzOLJfXzK28R1ROZ4wSJt1OD/T9W9cXt5+/u7rGPtB'
        'rsOLCfzav8AVKE+9XFMgGdk1yDSEJTqzLFdkHDx/2RtJyR+Wurgu69ghjanUc0PA/+8e2EMa'
        'I1zRDGRsrEjr7qRvC51z2i00Dy5p2y6Mkz6mWlC+lBIODbmLOR4dBgale7JcWBEbtYkLTD79'
        'A/kRhlxM1XQWfVg='
    )
    match = 'Authentication token has expired.'
    with pytest.raises(AuthenticationError, match=match) as exc_info:
        Authentication(token=expired_token)
        assert exc_info.type is AuthenticationError
    return


# def test_something():
#     # List some data objects from Norunda station.
#     l_data_objects = [
#         'https://meta.icos-cp.eu/objects/PzOR4WPAKws8jeysqKEcTsxC',
#         'https://meta.icos-cp.eu/objects/oF09opmdEUAAdWrY3qdJA1iT',
#         'https://meta.icos-cp.eu/objects/ZPSu9wc3rK6ZRip8LT8jV--f',
#         'https://meta.icos-cp.eu/objects/9ITXw5PBmbOINZsg7itwzh9P',
#         'https://meta.icos-cp.eu/objects/4HfaS9E6UFs6XhaXw63vcvI_',
#         'https://meta.icos-cp.eu/objects/wskaIuFeicJsuQvlqTrD0pGw',
#         'https://meta.icos-cp.eu/objects/87l9vTePIBvXeMyw2jgQ_2Bu',
#         'https://meta.icos-cp.eu/objects/qLo_14tetc3rgOXKgv1S-0wP'
#     ]
#     for data_object in l_data_objects:
#         assert Dobj(l_data_objects).data is pandas.DataFrame

