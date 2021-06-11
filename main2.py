import argparse 
import logging
logging.basicConfig(level=logging.INFO)

from common import config 

logger = logging.getLogger(__name__)

def _news_scraper(news_site):
    host = config()['news_sites'][news_site]['url']
    #host = config()['news_sites'].keys()
    #print(f'Sample: {host}')
    #print(type(host))
    logging.info('Beginning scrapper for {}'.format(host))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())
    print(f'First print: {news_site_choices}')
    parser.add_argument('news_site', 
                        help='The news site that you want to scrape', 
                        type=str, 
                        choices=news_site_choices)

    args = parser.parse_args()
    print(f'Second print: {args}')
    _news_scraper(args.news_site)