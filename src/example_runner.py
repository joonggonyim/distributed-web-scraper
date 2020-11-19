from absl import logging
from absl import app

from InstagramScraperWorker import InstagramScraperWorker
from instagram_ids import IG_USERNAME_TO_IDS_MAP
import utils
import constants

def main(_):
  session, resp = utils.insta_login(constants.IG_USERNAME, constants.IG_PASSWORD)
  save_root_dir = '/Users/joonggonyim/Documents/insta_crawler_jsons'
  for ig_id in IG_USERNAME_TO_IDS_MAP.keys():
    igsw = InstagramScraperWorker(ig_id, session=session)
    igsw.start(fetch_method='graphql', post_count=100)
    igsw.export_data(save_root_dir)
  logging.info('Done')


if __name__ == '__main__':
  app.run(main)