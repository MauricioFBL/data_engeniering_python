import argparse
import logging
import re
import pandas as pd
import hashlib
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
# la primera ejecucion se deben instlar estos mdoulos
# nltk.download('punkt')
# ltk.download('stopwords')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uid_for_url(df)
    df = _remove_new_lines(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _drop_duplicates(df, 'title')
    df = _remove_missing_values_rows(df)
    _save_trust_data(df, filename)

    return df


def _read_data(filename):
    logger.info(f'Reading file {filename}')
    return pd.read_csv(filename)


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    logger.info(f'newspaper uid detected {newspaper_uid}')
    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Filling uid column with value {newspaper_uid}')
    df['newspaper_uid'] = newspaper_uid
    return df


def _extract_host(df):
    logger.info('extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles = (df[missing_titles_mask]['url']
                        .str.extract(r'(?P<missing_titles>[^/]+)$')
                        .applymap(lambda title: title.split('-'))
                        .applymap(lambda title_list: ' '.join(title_list))
                        )
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:,'missing_titles']

    return df


def _generate_uid_for_url(df):
    logger.info('Generating UID for url')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis = 1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids

    return df.set_index('uid')


def _remove_new_lines(df):
    logger.info('Removing new lines from body')
    stripped_body = (df
                    .apply(lambda row: row['body'], axis = 1)
                    .apply(lambda body: list(body))
                    .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)))
                    .apply(lambda letters: ''.join(letters))
                    )
    df['body'] = stripped_body
    return df


def _tokenize_column(df, column_name):
    logger.info(f'Tokenizing column {column_name}')
    stop_words = set(stopwords.words('spanish'))
    new_column_name = f'n_tokens_{column_name}'
    tokens = (df
            .dropna()
            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
            .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
            .apply(lambda valid_word_list: len(valid_word_list))
            )
    df[new_column_name] = tokens
    return df


def _drop_duplicates(df, column_name):
    logger.info('Removing duplicates')
    df.drop_duplicates([column_name], keep = 'first', inplace = True)
    return df


def _remove_missing_values_rows(df):
    logger.info('Removing missing values')
    return df.dropna()


def _save_trust_data(df, filename):
    trust_filename = filename.replace('.csv','_trusted.csv')
    logger.info(f'Saving clean data in: {trust_filename}')
    df.to_csv(trust_filename, encoding = 'utf-8-sig')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The patg to the dirty dat',
                        type=str)
    arg = parser.parse_args()
    df = main(arg.filename)
    print(df)