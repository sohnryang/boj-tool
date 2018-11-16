import os
import requests
import pickle
import getpass
import logging

from bs4 import BeautifulSoup as bs
from xdg import XDG_DATA_HOME

data_dir = XDG_DATA_HOME + '/boj-submit'
boj_url = 'https://www.acmicpc.net'
cookiefile_path = data_dir + '/cookiefile'
sess = requests.Session()


def initialize():
    if not os.path.exists(data_dir):
        logging.debug('Creating directory for cookiefile...')
        os.makedirs(data_dir)
        logging.debug('Created directory for cookiefile')


def auth_user(username, password):
    data = {'login_user_id': username,
            'login_password': password,
            'auto_login': 'on'}
    logging.info('Authenticating...')
    logging.debug('Username: {0}, Password: {1}'.format(username,
                                                        '*' * len(password)))
    sess.post(boj_url + '/signin', data=data)


def check_login():
    soup = bs(sess.get(boj_url).text, 'html.parser')
    return soup.find('a', {'class': 'username'}) is not None


def save_cookie(session):
    with open(cookiefile_path, 'wb') as f:
        logging.debug('Saving cookie to {0}...'.format(cookiefile_path))
        pickle.dump(session.cookies, f)
        logging.debug('Saved cookie to {0}'.format(cookiefile_path))


def login():
    username = input('Username: ')
    password = getpass.getpass()
    auth_user(username, password)
    save_cookie(sess)


if __name__ == '__main__':
    main()


def main():
    initialize()
    if os.path.isfile(data_dir + '/cookiefile'):
        with open(data_dir + '/cookiefile', 'rb') as f:
            sess.cookies.update(pickle.load(f))
    else:
        login()
    if check_login():
        logging.info('Logged in')
    else:
        logging.error('Login failed')
        os.remove(cookiefile_path)
