import argparse
import logging
import pandas as pd
# from sqlalchemy import engine

from article import Article
from base import Base, Engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(Engine)
    session = Session()
    articles = pd.read_csv(filename)

    for index, row in articles.iterrows():
        uid = row['uid']
        logger.info(f'Loding article {uid} ito database')
        article = Article(row['uid'],
                            row['body'],
                            row['host'],
                            row['newspaper_uid'],
                            row['n_tokens_body'],
                            row['n_tokens_title'],
                            row['title'],
                            row['url'],
                            )

        session.add(article)

    session.commit()
    session.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='the file you want to load in the db',
                        type=str)
    args = parser.parse_args()

    main(args.filename)
