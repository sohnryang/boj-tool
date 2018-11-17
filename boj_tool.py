import argparse
import configparser
import getpass
import logging
import logging.handlers
import os
import pickle
import requests

from bs4 import BeautifulSoup as bs
from xdg import (XDG_CONFIG_HOME, XDG_DATA_HOME)

data_dir = XDG_DATA_HOME + '/boj-tool'
config_dir = XDG_CONFIG_HOME + '/boj-tool'
boj_url = 'https://www.acmicpc.net'
cookiefile_path = data_dir + '/cookiefile'
configfile_path = config_dir + '/config'
sess = requests.Session()

logger = logging.getLogger('boj-tool')
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)
config = configparser.ConfigParser()

result = {
    '맞았습니다!!',
    '20점', '40점', '60점', '80점', '100점',
    '출력 형식이 잘못되었습니다', '틀렸습니다', '시간 초과',
    '메모리 초과', '출력 초과', '런타임 에러', '컴파일 에러'
}


def initialize():
    if not os.path.exists(data_dir):
        logger.debug('Creating directory for cookiefile...')
        os.makedirs(data_dir)
        logger.debug('Created directory for cookiefile')
    if os.path.isfile(configfile_path):
        logger.debug('Config file found')
        config.read(configfile_path)


def auth_user(username, password):
    soup = bs(sess.get(boj_url).text, 'html.parser')
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


def load_cookie():
    if os.path.isfile(data_dir + '/cookiefile'):
        logger.debug('Cookiefile found. Loading...')
        with open(data_dir + '/cookiefile', 'rb') as f:
            sess.cookies.update(pickle.load(f))
        logger.info('Loaded cookiefile')
    else:
        logger.error('Cookiefile not found')
        login()


def login():
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
        logger.info('Removed cookiefile')


def get_compiler(lang, default):
    if 'Compiler' in config[lang]:
        return config[lang]['Compiler']
    return default


def get_version(lang, default):
    if 'Version' in config[lang]:
        return config[lang]['Version']
    return default


def get_lang_code(ext):
    if ext in ['.cc', '.cpp', '.c++']:
        if 'C++' not in config:
            return 88 # default is C++14
        compiler = get_compiler('C++', default='g++')
        version = get_version('C++', default='C++14')
        if compiler.lower() == 'g++':
            if '11' in version:
                return 49
            elif '14' in version:
                return 88
            elif '17' in version:
                return 84
            else:
                logger.error('Invalid C++ version: {0}'.format(version))
        elif compiler.lower() == 'clang':
            if '11' in version:
                return 66
            elif '14' in version:
                return 67
            elif '17' in version:
                return 85
            else:
                logger.error('Invalid C++ version: {0}'.format(version))
        else:
            logger.error('Invalid C++ compiler: {0}'.format(compiler))
    elif ext == '.c':
        if 'C' not in config:
            return 75 # default is C11
        compiler = get_compiler('C', default='gcc')
        version = get_version('C', default='C11')
        if compiler.lower() == 'gcc':
            if '11' in version:
                return 75
            elif version == 'C':
                return 0
            else:
                logger.error('Invalid C version: {0}'.format(version))
        elif compiler.lower() == 'clang':
            if '11' in version:
                return 77
            elif version == 'C':
                return 59
            else:
                logger.error('Invalid C version: {0}'.format(version))
        else:
            logger.error('Invalid C compiler: {0}'.format(compiler))
    elif ext == '.py':
        if 'Python' not in config:
            return 28 # default is CPython 3
        compiler = get_compiler('Python', default='CPython')
        version = get_version('Python', default='3')
        if compiler.lower() == 'cpython':
            if '2' in version:
                return 6;
            elif '3' in version:
                return 28
            else:
                logger.error('Invalid Python version: {0}'.format(version))
        elif compiler.lower() == 'pypy':
            if '2' in version:
                return 32
            elif '3' in version:
                return 73
            else:
                logger.error('Invalid Python version: {0}'.format(version))
        else:
            logger.error('Invalid Python interpreter: {0}'.format(compiler))
    elif ext == '.java':
        if 'Java' not in config:
            return 3 # default is Java (oracle)
        compiler = get_compiler('Java', default='Oracle')
        if compiler.lower() == 'oracle':
            return 3;
        elif compiler.lower() == 'openjdk':
            return 91
        else:
            logger.error('Invalid Java compiler: {0}'.format(compiler))
    elif ext == '.txt':
        return 58
    elif ext == '.js':
        return 17
    elif ext == '.aheui':
        return 83
    return 88 # fallback


def submit(number, filename):
    load_cookie()
    logger.debug('Problem number is {0}, filename is {1}'.format(number,
                                                                 filename))
    soup = bs(sess.get(boj_url + '/submit/' + str(number)).text, 'html.parser')
    key = soup.find('input', {'name': 'csrf_key'})['value']
    file_ext = os.path.splitext(filename)
    language_code = get_lang_code(file_ext)
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


def get_username():
    soup = bs(sess.get(boj_url).text, 'html.parser')
    return soup.find('a', {'class': 'username'}).get_text()


def convert_msg(msg):
    if '채점 준비 중' in msg:
        msg = '\u001b[33mPreparing...\u001b[0m'
        return msg
    elif '채점 중' in msg:
        msg = msg.replace('채점 중', '\u001b[33mJudging...')
        msg += '\u001b[0m'
        return msg
    conversion_table = {
        '맞았습니다!!': '\u001b[32mAC\u001b[0m',
        '20점': '\u001b[33mPartial (20)\u001b[0m',
        '40점': '\u001b[33mPartial (40)\u001b[0m',
        '60점': '\u001b[33mPartial (60)\u001b[0m',
        '80점': '\u001b[33mPartial (80)\u001b[0m',
        '100점': '\u001b[33mPartial (100)\u001b[0m',
        '출력 형식이 잘못되었습니다': '\u001b[31mPE\u001b[0m',
        '틀렸습니다': '\u001b[31mWA\u001b[0m',
        '시간 초과': '\u001b[31mTLE\u001b[0m',
        '메모리 초과': '\u001b[31mMLE\u001b[0m',
        '출력 초과': '\u001b[31mPLE\u001b[0m',
        '런타임 에러': '\u001b[34mRTE\u001b[0m',
        '컴파일 에러': '\u001b[34mCompile Error\u001b[0m',
        '기다리는 중': '\u001b[33mWaiting...\u001b[0m'
    }
    return conversion_table[msg]


def print_result(number):
    done = False
    while not done:
        logger.debug('Getting username from HTML...')
        username = get_username()
        logger.debug('Username is {0}'.format(username))
        _url = boj_url + "/status?from_mine=1&problem_id=" + str(number) +\
               "&user_id=" + username
        soup = bs(sess.get(_url).text, 'html.parser')
        text = soup.find('span',
                         {'class': 'result-text'}).find('span').string.strip()
        print('\r' + ' ' * 20, end='')
        print('\r{0}'.format(convert_msg(text)), end='')
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

    initialize()
    if args.verbose:
        logger.setLevel(logging.INFO)
    elif args.debug:
        logger.setLevel(logging.DEBUG)

    if args.subparser == 'login':
        login()
    elif args.subparser == 'submit':
        submit(args.number, args.filename)
        print_result(args.number)


if __name__ == '__main__':
    main()
