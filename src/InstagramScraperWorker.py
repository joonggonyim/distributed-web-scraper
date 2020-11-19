from absl import logging

import pdb
import os.path as osp
import os
import json
import constants
import utils
from bs4 import BeautifulSoup
import requests
import time
import instagram_ids as igid


class InstagramScraperWorker:

  def __init__(self, instagram_username, start=False, session=None,
               fetch_method='html', 
               post_count=constants.DEFAULT_QUERY_POST_COUNT):
    logging.info('Initializing InstagramScraperWorker for instagram_username: '
                 '%s', instagram_username)
    self._instagram_username = instagram_username
    self._instagram_id = igid.IG_USERNAME_TO_IDS_MAP[instagram_username]
    self._target_url = f'https://instagram.com/{instagram_username}'
    self._parser = constants.IG_USERNAME_TO_PARSER_MAP[self._instagram_username]
    self.session = session
    self._default_data = {
      'instagram_username': instagram_username,
      'scraped_timestamp': time.time()
    }
    if start:
      self.start(fetch_method=fetch_method)

  def _get_parsed_post(self, post):
    """Parses each post into desired output dict.

    Output list:
      - post_id: post unique id
      - timestamp: creation timestamp of the post
      - description: description of the post
      - image_urls: list of image urls
    Args:
      post: dictionary containing post data

    Returns:
      dictionary of parsed data. Keys are listed above
    """
    post_id = post['node']['id']
    shortcode = post['node']['shortcode']
    image_nodes = utils.get_dict_at_path(post, 
                                         constants.POSTS_DATA__MEDIA,
                                         return_none=True)
    image_urls = []
    if image_nodes:
      image_urls = [image_node['node']['display_url'] 
                    for image_node in image_nodes]
    description = utils.get_dict_at_path(post, 
                                         constants.POSTS_DATA__DESCRIPTION)
    timestamp = utils.get_dict_at_path(post, constants.POSTS_DATA__TIMESTAMP)
    return {
      'post_id': post_id,
      'timestamp': timestamp,
      'description': description,
      'image_urls': image_urls,
      'item': self._parse_description(description),
      'shortcode': shortcode,
      'post_url': constants.IG_POST_URL_TMPL.format(shortcode),
      **self._default_data
    }

  def _get_all_parsed_posts(self):
    parsed_data = []
    for post in self._posts_data:
      parsed_data.append(self._get_parsed_post(post))  
    return parsed_data

  def _parse_description(self, description):
    return self._parser.parse_description(description)

  def _fetch_posts_data_with_html(self):
    """Fetchs posts data by requesting instagram.com/${username}.

    Currently this method does not provide any benefit over getting the json
    response directly by requesting instagram.com/${username}/?__a=1 other than
    the fact that we get 12 posts instead of 10 from a1.

    """
    headers = constants.IG_REQUEST_HEADERS
    cookies = None
    if self.session:
      headers['x-csrftoken'] = self.session['csrf_token']

      cookies = {
        "sessionid": self.session['session_id'],
        "csrftoken": self.session['csrf_token']
      }
    resp = requests.request("GET", self._target_url, headers=headers, 
                            cookies=cookies)
    self._parsed_page = BeautifulSoup(resp.content, 'html.parser')
    shared_data = None
    for script in self._parsed_page.find_all('script'):
      if script.decode_contents().strip().startswith('window._sharedData ='):
        shared_data =  json.loads(script.decode_contents().split(' = ')[1][:-1])
    if shared_data is None:
      logging.error('Could not find a script element with "window._sharedData '
                    '=" Please try again.')
      return None
    self._posts_data = utils.get_dict_at_path(
        shared_data, ('entry_data', 'ProfilePage', 0, 'graphql') + 
        constants.POSTS_DATA)
    return self._posts_data


  def _fetch_posts_data_with_a1(self):
    headers = constants.IG_REQUEST_HEADERS
    cookies = None
    if self.session:
      headers['x-csrftoken'] = self.session['csrf_token']

      cookies = {
        "sessionid": self.session['session_id'],
        "csrftoken": self.session['csrf_token']
      }
    a1_url = self._target_url + '/?__a=1'
    resp = requests.request("GET", a1_url, headers=headers, cookies=cookies)
    self._posts_data = utils.get_dict_at_path(
        json.loads(resp.text)['graphql'], constants.POSTS_DATA)
    return self._posts_data


  def _fetch_posts_data_with_graphql(
        self, post_count=constants.DEFAULT_QUERY_POST_COUNT):
    headers = constants.IG_REQUEST_HEADERS
    cookies = None
    if self.session:
      headers['x-csrftoken'] = self.session['csrf_token']

      cookies = {
        "sessionid": self.session['session_id'],
        "csrftoken": self.session['csrf_token']
      }
    _, encoded_query_var = utils.get_ig_query_var(self._instagram_id, 
                                                  post_count)
    queyr_url = constants.IG_GRAPHQL_QUERY_URL_TMPL.format(
        constants.IG_GET_POSTS_QUERY_ID, encoded_query_var)
    resp = requests.request("GET", queyr_url, headers=headers, cookies=cookies)
    if resp.ok:
      self._posts_data = utils.get_dict_at_path(
        json.loads(resp.text)['data'], constants.POSTS_DATA)
      return self._posts_data
    else:
      logging.error('somethign went wrong')
      self._posts_data = None



  def start(self, fetch_method='html', 
            post_count=constants.DEFAULT_QUERY_POST_COUNT):
    t0 = time.time()
    logging.info('Start scraping %s', self._instagram_username)
    logging.info('Fetching shared data using %s method', fetch_method)
    if fetch_method == 'html':
      logging.info('Ignoring post_count = %d because we can only query 12 '
                   'posts using html.', post_count)
      self._fetch_posts_data_with_html()
    elif fetch_method == 'graphql':
      self._fetch_posts_data_with_graphql(post_count)
    elif fetch_method == 'a1':
      self._fetch_posts_data_with_a1()
    else:
      e = f'Unrecognized fetch_method: {fetch_method}'
      raise Exception(e)

    self._parsed_data = self._get_all_parsed_posts()
    logging.info('Successfully parsed %d posts. Elapsed time %1.4fs', 
                 len(self._parsed_data), time.time() - t0)

  def export_data(self, save_root_dir, format='json'):
    save_dir = osp.join(save_root_dir, self._instagram_username)
    if not osp.isdir(save_dir):
      os.makedirs(save_dir, exist_ok=True)
      logging.info('Successfully created export dir: %s', save_dir)


    for post in self._parsed_data:
      post_id = post['post_id']
      save_path = osp.join(save_dir, f'{post_id}.json')
      with open(save_path, 'w') as f:
        json.dump(post, f, indent=2, sort_keys=True)
        logging.info('Successfully wrote post %s to %s', str(post_id), 
                     save_path)


  def write_to_db(self):
    """Write post data to db.

    We write to two dbs
    1. key-value paired db: 
      key - post_id, val - timestamp

    2. relational db
      write all fields in columns

    To be implemented ...
    """
    pass




