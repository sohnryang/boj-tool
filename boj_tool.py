import os
import requests
import pickle
import getpass
import logging
import logging.handlers
import argparse

from bs4 import BeautifulSoup as bs
from xdg import XDG_DATA_HOME

data_dir = XDG_DATA_HOME + '/boj-tool'
boj_url = 'https://www.acmicpc.net'
cookiefile_path = data_dir + '/cookiefile'
username = ''
sess = requests.Session()
logger = logging.getLogger('boj-tool')
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)


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
    if os.path.isfile(data_dir + '/cookiefile'):
        with open(data_dir + '/cookiefile', 'rb') as f:
            sess.cookies.update(pickle.load(f))
    else:
        username = input('Username: ')
        password = getpass.getpass()
        auth_user(username, password)
        save_cookie(sess)
    if check_login():
        logger.info('Logged in')
    else:
        logger.error('Login failed')
        logger.debug('Removing cookiefile...')
        os.remove(cookiefile_path)
        logger.debug('Removed cookiefile')


def submit(number, filename):
    soup = bs(sess.get(boj_url + '/submit/' + str(number)).text, 'html.parser')
    key = soup.find('input', {'name': 'csrf_key'})['value']
    # TODO: add more languages
    language_code = 88 # default is C++14
    file_ext = os.path.splitext(filename)
    if file_ext in ['.cc', '.cpp', '.c++']:
        language_code = 88
    elif file_ext == '.py':
        language_code = 28
    elif file_ext == '.java':
        language_code = 3
    elif file_ext == '.txt':
        language_code = 58
    elif file_ext == '.js':
        language_code = 17
    code = ''
    with open(filename, 'r') as f:
        code = f.read()

    data = {
        'problem_id': number,
        'source': code,
        'language': language_code,
        'code_open': 'open',
        'csrf_key': key
    }
    sess.post(boj_url + '/submit/' + str(number), data=data)


def print_result(number, username):
    done = False
    while not done:
        _url = boj_url + "/status?from_mine=1&problem_id=" + number + "&user_id=" + username
        soup = bs(sess.get(_url).text, 'html.parser')
        text = soup.find('span', {'class': 'result-text'}).find('span').string.strip()
        print("\r                          ", end='')
        print("\r%s" % text, end='')
        if text in result:
            done = True
    print()


def main():
    parser = argparse.ArgumentParser(description='boj-tool: a CLI tool for BOJ')
    parser.add_argument('-v', '--verbose', help='set log level to INFO',
                        action='store_true')
    parser.add_argument('-d', '--debug', help='set log level to DEBUG',
                        action='store_true')
    subparsers = parser.add_subparsers(dest='subparser')
    login_parser = subparsers.add_parser('login')
    submit_parser = subparsers.add_parser('submit')
    submit_parser.add_argument('number', type=int, help='the problem number')
    submit_parser.add_argument('filename', help='filename to submit')
    args = parser.parse_args()
    print(args)

    initialize()
    if args.verbose:
        logger.setLevel(logging.INFO)
    elif args.debug:
        logger.setLevel(logging.DEBUG)

    if args.subparser == 'login':
        login()
    elif args.subparser == 'submit':
        submit(args.number, args.filename)
        print_result(args.number, username)


if __name__ == '__main__':
    main()
