import os
import sys
import time
from datetime import datetime
from app import config_parser
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


def process_args(default_settings={}):
    settings = default_settings

    for arg in sys.argv:
        if arg == 'sample':
            with open('app_sample.ini', 'w') as f:
                f.write(samples.app_ini())

            with open('config_sample.ini', 'w') as f:
                f.write(samples.config_ini())

            exit()
        if arg.startswith('app_ini:'):
            settings['app_ini'] = arg.split(':')[1]

    processed_settings = process_settings(settings)

    return processed_settings

def process_settings(settings):
    parsed_settings = config_parser.load(settings)

    div('Ita PC is running')

    if parsed_settings['output_mode'] == 'append':
        pass

    if parsed_settings['output_mode'] == 'fresh':
        try:
            os.remove(parsed_settings['output'])
        except:
            print(f'>>> Cannot remove file {parsed_settings["output"]}')

    if parsed_settings['output_mode'] == 'timestamp':
        filename = parsed_settings['output']

        dt_object = datetime.fromtimestamp(time.time())
        time_formatted = dt_object.strftime('%Y%m%d%H%M%S')

        parsed_settings['output'] = f'{filename}_{time_formatted}.csv'

    if 'app_key' not in parsed_settings:
        parsed_settings['secret'] = 'app_secret_key_CHANGE_ME'

    return parsed_settings

def config_from_settings(settings):
    config = {}
    config['SECRET_KEY'] = settings['secret']

    return config

def main():
    default_settings = {
      'output': 'data.csv',
      'output_mode': 'append',
      'config': 'config.ini',
      'host': '0.0.0.0',
      'debug': False,
      'port': 6789,
      'app_ini': 'app.ini'
    }

    settings = process_args(default_settings)
    config = config_from_settings(settings)

    div('Settings', settings)
    div('Config', config)
    app, socketio = create_app(settings, config)

    div('Server running')
    print('-' * 17)
    socketio.run(app, host=settings['host'], port=settings['port'], debug=settings['debug'])

if __name__ == "__main__":
    main()
