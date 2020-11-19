"""
python example_runner.py \
  --save_root_dir '/Users/joonggonyim/Documents/insta_crawler_jsons' \
  --fetch_method 'a1'
"""

from absl import logging
from absl import app
from absl import flags

from InstagramScraperWorker import InstagramScraperWorker
from instagram_ids import IG_USERNAME_TO_IDS_MAP
import utils
import constants

FLAGS = flags.FLAGS

flags.DEFINE_string('save_root_dir', '', 'Root dir to save')
flags.DEFINE_enum('fetch_method', 'a1', ['html', 'a1', 'graphql'], 
                  'The method to be used for fetching data.')


def main(_):
  save_root_dir = FLAGS.save_root_dir
  fetch_method = FLAGS.fetch_method
  session, resp = utils.insta_login(constants.IG_USERNAME, constants.IG_PASSWORD)
  for ig_id in IG_USERNAME_TO_IDS_MAP.keys():
    igsw = InstagramScraperWorker(ig_id, session=session)
    igsw.start(fetch_method=fetch_method)
    igsw.export_data(save_root_dir)
  logging.info('Done')


if __name__ == '__main__':
  app.run(main)