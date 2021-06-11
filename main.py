import argparse
import logging
import news_page_objects as news
from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _new_scrapper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info(f'Beginning scrapper fot {host}')
    homepage = news.HomePage(news_site_uid, host)
    for link in homepage.article_links:
        print(link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_sites'].keys())
    print(news_site_choices)
    parser.add_argument('news_site',
                        help='The new site you want to scrape',
                        type=str,
                        choices=news_site_choices)
    args = parser.parse_args()
    _new_scrapper(args.news_site)
