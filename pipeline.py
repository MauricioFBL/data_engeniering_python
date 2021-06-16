import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['eluniversal', 'elpais']

def _extract():
    logger.info('Staring extract process')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python','main.py', news_site_uid], cwd='./extract')
        subprocess.run(['find','.','-name',f'{news_site_uid}*',
                        '-exec','mv','{}','..transform/{}_.csv'.format(news_site_uid),
                        ';'], cwd = './extract')
                        
    print('extraccion completa')


def _transform():
    logger.info('Staring transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = '{}_.csv'.format(news_site_uid)
        clean_data_filename = '{}_trusted_.csv'.format(dirty_data_filename)
        subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform')
        subprocess.run(['rm', dirty_data_filename], cwd='./transform')
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_site_uid)], cwd='./transform')


def _load():
    logger.info('Staring extract process')
    for news_site_uid in news_sites_uids:
        clean_data_filename = '{}.csv'.format(news_site_uid)
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        subprocess.run(['rm', clean_data_filename], cwd='./load')


def main():
    _extract()
    _transform()
    -_load()



if __name__ == '__main__':
    main()