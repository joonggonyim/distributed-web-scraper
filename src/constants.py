from item_parser import *

###  === Instagram ===
POSTS_DATA = ('user', 'edge_owner_to_timeline_media', 'edges')
# Following keys must be used after accessing a post using POSTS_DATA
POSTS_DATA__DESCRIPTION = ('node', 'edge_media_to_caption', 'edges', 0, 
                            'node', 'text')
POSTS_DATA__TIMESTAMP = ('node', 'taken_at_timestamp')

# This only works when posts data is fetched via 'html' or 'a1'
POSTS_DATA__MEDIA = ('node', 'edge_sidecar_to_children', 'edges')


IG_USERNAME_TO_PARSER_MAP = {
  'caseoffice.official': caseoffice_official,
  'highkalla': highkalla,
}

IG_USERNAME = 'jybot1234'
IG_PASSWORD = '1234jybot'

# When using this header, make sure to set 'x-csrftoken'
IG_REQUEST_HEADERS = {
  'authority': 'www.instagram.com',
  'x-ig-www-claim': 'hmac.AR2-43UfYbG2ZZLxh-BQ8N0rqGa-hESkcmxat2RqMAXejXE3',
  'x-instagram-ajax': 'adb961e446b7-hot',
  'content-type': 'application/x-www-form-urlencoded',
  'accept': '*/*',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest',
  'x-csrftoken': None,
  'x-ig-app-id': '1217981644879628',
  'origin': 'https://www.instagram.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.instagram.com/create/details/',
  'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
}

IG_POST_URL_TMPL = 'https://www.instagram.com/p/{}'
IG_LOGIN_URL = 'https://www.instagram.com/accounts/login/'
IG_LOGIN_AJAX_URL = 'https://www.instagram.com/accounts/login/ajax/'

IG_BASE_URL = 'https://www.instagram.com/'
MAIN_STORIES_URL = (IG_BASE_URL + 'graphql/query/?query_hash=45246d3fe16ccc6577'
                    'e0bd297a5db1ab&variables=%7B%22reel_ids%22%3A%5B%22{0}%22%'
                    '5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5'
                    'D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_ove'
                    'rlay%22%3Afalse%7D')


IG_GRAPHQL_QUERY_URL_TMPL = query_base_url = (
    'https://www.instagram.com/graphql/query/?query_id={}&variables={}')

# ref: https://github.com/MohanSha/InstagramResearch
IG_QUERY_IDS = {
  'user_following': 17874545323001329,
  'user_followers': 17851374694183129,
  'user_posts': 17888483320059182,
  'posts_on_feed': 17842794232208280
}
IG_GET_POSTS_QUERY_ID = 17888483320059182
IG_GET_FOLLOWERS_QUERY_ID = 17851374694183129


DEFAULT_QUERY_POST_COUNT = 12