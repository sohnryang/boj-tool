import os
import requests
import pickle
import getpass
import logging
import logging.handlers
import argparse

from bs4 import BeautifulSoup as bs
from xdg import XDG_DATA_HOME

data_dir = XDG_DATA_HOME + '/boj-submit'
boj_url = 'https://www.acmicpc.net'
cookiefile_path = data_dir + '/cookiefile'
sess = requests.Session()
logger = logging.getLogger('boj-submit')
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)


def initialize():
    if not os.path.exists(data_dir):
        logger.debug('Creating directory for cookiefile...')
        os.makedirs(data_dir)
        logger.debug('Created directory for cookiefile')


def auth_user(username, password):
    data = {'login_user_id': username,
            'login_password': password,
            'auto_login': 'on'}
    logger.info('Authenticating...')
    logger.debug('Username: {0}, Password: {1}'.format(username,
                                                        '*' * len(password)))
    sess.post(boj_url + '/signin', data=data)


def check_login():
    soup = bs(sess.get(boj_url).text, 'html.parser')
    return soup.find('a', {'class': 'username'}) is not None


def save_cookie(session):
    with open(cookiefile_path, 'wb') as f:
        logger.debug('Saving cookie to {0}...'.format(cookiefile_path))
        pickle.dump(session.cookies, f)
        logger.debug('Saved cookie to {0}'.format(cookiefile_path))


def login():
    username = input('Username: ')
    password = getpass.getpass()
    auth_user(username, password)
    save_cookie(sess)


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    initialize()
    if os.path.isfile(data_dir + '/cookiefile'):
        with open(data_dir + '/cookiefile', 'rb') as f:
            sess.cookies.update(pickle.load(f))
    else:
        login()
    if check_login():
        logger.info('Logged in')
    else:
        logger.error('Login failed')
        logger.debug('Removing cookiefile...')
        os.remove(cookiefile_path)
        logger.debug('Removed cookiefile')


if __name__ == '__main__':
    main()
