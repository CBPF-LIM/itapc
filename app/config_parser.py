import os
from tools.shortcuts import b

valid_true = ['true', '1', 'yes', 'y', 't', 'on', 'enable', 'enabled', 'ok']
valid_false = ['false', '0', 'no', 'n', 'f', 'off', 'disable', 'disabled', 'ko']
true_values = ', '.join(valid_true)
false_values = ', '.join(valid_false)


def is_valid_ipv4(ip):
    ipv4_regex = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return bool(ipv4_regex.match(ip))

def host_type(s):
    if s in [ 'localhost', 'local', 'private', 'intenal']:
        return '127.0.0.1'
    if s in ['public', 'external', 'all', 'any']:
        return '0.0.0.0'
    return s

def output_mode_type(s):
    if s.lower() in ['append', 'a']:
        return 'append'
    if s.lower() in ['fresh', 'f']:
        return 'fresh'
    if s.lower() in ['timestamp', 't']:
        return 'timestamp'

    return {'error': f'Invalid value for output_mode: <{s}>. Valid values are append, overwrite, new'}

def str_to_bool(s):
    if s.lower() in valid_true:
        return True

    if s.lower() in valid_false:
        return False

    message = f'Invalid value for boolean: <{s}>. TRUE is <{true_values}> and FALSE is <{false_values}>'
    return {'error': message}

def print_settings(settings):
    print('> App configuration loaded:')
    print('-' * 25)
    for key, value in settings.items():
        print(f'- {key}: {value}')

def load(settings):
    settings_types = {
      'output': str,
      'output_mode': output_mode_type,
      'config': str,
      'host': host_type,
      'debug': str_to_bool,
      'port': int,
      'app_ini': str
    }

    errors = {}
    app_ini = settings['app_ini']

    if os.path.isfile(app_ini):
        with open(app_ini, 'r') as f:
            for line in f:
                if line.startswith('#') or line.startswith('//'):
                    continue
                line = line.split('//')[0]
                pair = line.split(':')
                if len(pair) != 2:
                    continue

                key, value = pair
                key = key.strip()
                value = value.strip()

                # if key exists in settings_types, get value. Otherwise, str
                parsed_value = ""
                if key in settings_types:
                    try:
                        parsed_value = settings_types[key](value)

                        if type(parsed_value) == dict:
                            errors[key] = {
                                'key': key,
                                'value': value,
                                'message': parsed_value['error']
                            }
                    except:
                        errors[key] = {
                            'key': key,
                            'value': value,
                            'message': f'Invalid value. Got <{value}> ({type(value)}), expected {settings_types[key]}'
                        }
                else:
                    parsed_value = str(value)

                settings[key] = parsed_value

    # print errors if it is not {}
    if errors:
        print(f'Errors in {app_ini}:')
        print('------------------')
        for key, error in errors.items():
            print(f'{error["key"]}: {error["value"]}')
            print(f'  - {error["message"]}')
        print()
        print('(!) Fix the errors and try again.')
        exit()


    else:
        print_settings(settings)
        return settings
