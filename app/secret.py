import os
import textwrap
import secrets

key_file_path = 'app_secret_key.txt'

def _key_already_exists():
  return os.path.exists(key_file_path)

def _generate():
  return secrets.token_urlsafe(64)

def _generate_info_message():
  return textwrap.dedent("""\
    # This is the app secret key, used in encryptions.
    # Do not share it with anyone.
    # It is generated automatically the first time you run the app.
    # You can generate a new one with:
    #
    #   $ python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
    #
  """)

def _create_app_key():
  secret_key = _generate()

  with open(key_file_path, 'w') as key_file:
    key_file.write(_generate_info_message())
    key_file.write(secret_key)

  return secret_key

def _read_app_key():
  with open(key_file_path, 'r') as key_file:
    for line in key_file:
      line = line.strip()
      if not line.startswith('#'):
        return line.strip()

def get_app_secret():
  return _read_app_key() if _key_already_exists() else _create_app_key()
