import os
import sys
import time
from datetime import datetime
from app import create_app
from app import samples
from tools.shortcuts import b

def print_hash(d):
    m = 0
    for k, v in d.items():
        m = max(m, len(k))

    for key in sorted(d):
        print(f'  - {key.ljust(m)} = {d[key]}')

def div(title, d={}):
    formatted_title = '- ' + title
    if d == {}:
        print(formatted_title)
    else:
        print(formatted_title + ':')
        print_hash(d)


def process_args():
    for arg in sys.argv:
        if arg == 'sample':
            with open('app_sample.ini', 'w') as f:
                f.write(samples.app_ini())

            exit()


def main():
    settings = {
      'host': '0.0.0.0',
      'debug': False,
      'port': 6789
    }

    div('Settings', settings)
    app, socketio = create_app()

    div('Server running')
    print('-' * 17)
    socketio.run(app, host=settings['host'], port=settings['port'], debug=settings['debug'])

if __name__ == "__main__":
    main()
