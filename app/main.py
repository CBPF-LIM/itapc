import os
import sys
import time
from datetime import datetime
from app import config_parser
from app import create_app
from app import samples
from tools.shortcuts import b
import ita

def process_args():
    for arg in sys.argv:
        if arg == 'sample':
            with open('config_sample.ini', 'w') as f:
                f.write(samples.app_ini())

            with open('app_sample.ini', 'w') as f:
                f.write(samples.config_ini())

            exit()
        if arg.startswith('app_ini:'):
            app.settings['app_ini'] = arg.split(':')[1]

def main():
    app = create_app(ita.processPost, ita.processGet)
    process_args()

    settings = {
      'output': 'data.csv',
      'output_mode': 'append',
      'config': 'config.ini',
      'host': '127.0.0.1',
      'debug': False,
      'port': 5000,
      'app_ini': 'app.ini'
    }

    app.settings = config_parser.load(settings)

    print('Ita PC is running')
    print('-' * 25)
    ita.use_settings(app.settings)
    print('-' * 25)
    print('> Starting server')
    print('-' * 25)

    if app.settings['output_mode'] == 'append':
        pass

    if app.settings['output_mode'] == 'fresh':
        try:
            os.remove(app.settings['output'])
        except:
            print(f'>>> Cannot remove file {app.settings["output"]}')

    if app.settings['output_mode'] == 'timestamp':
        filename = app.settings['output']

        dt_object = datetime.fromtimestamp(time.time())
        time_formatted = dt_object.strftime('%Y%m%d%H%M%S')

        app.settings['output'] = f'{filename}_{time_formatted}.csv'

    app.run(
        host=app.settings['host'],
        port=app.settings['port'],
        debug=app.settings['debug']
    )

if __name__ == "__main__":
    main()
