from absl import logging
import requests
import constants
import json
import time
import urllib.parse

def get_dict_at_path(input_dict, keys_tuple, return_none=False):
  """Accesses nested dict with keys tuple.
  
  example:
    input_dict = {'a': {'b': [{'c': 'foo'}, {'d': 'bar'}]}}
    keys_tuple = ('a', 'b', 0, 'c')

    output = 'foo'

  Args:
    input_dict: input dictionary
    keys_tuple: array of keys. Note arrays must be accessed with int

  Returns:
    nested value
  """
  d = input_dict
  for key in keys_tuple:
    if isinstance(d, list):
      d = d[key]
    elif key in d:
      d = d[key]
    else:
      if return_none:
        return None
      raise Exception(f'{key} does not exist')
  return d


def insta_login(username: str, password: str) -> dict:
  """Log in to instagram.

  reference:
  https://github.com/softcoder24/insta_share/blob/master/insta_share/instagram.py
  """
  url = constants.IG_LOGIN_URL
  login_url = constants.IG_LOGIN_AJAX_URL

  time_now = int(time.time())

  response = requests.get(url)
  csrf = response.cookies['csrftoken']

  payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time_now}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
  }

  login_header = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"),
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": csrf
  }
  login_response = requests.post(login_url, data=payload, headers=login_header)
  json_data = json.loads(login_response.text)

  if json_data["authenticated"]:
    cookies = login_response.cookies
    cookie_jar = cookies.get_dict()

    session = {
      "csrf_token": cookie_jar['csrftoken'],
      "session_id": cookie_jar['sessionid']
    }
    return session, login_response
  raise Exception(login_response.text)


def get_ig_query_var(user_id, ig_post_count=1, after=''):
  output_query = {'id': user_id, 'first': ig_post_count, 'after': after}
  return output_query, urllib.parse.quote(json.dumps(output_query))
