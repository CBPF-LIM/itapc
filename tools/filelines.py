import os

def last(filename):
  with open(filename, "rb") as f:
      # Find file size
      f.seek(0, 2)
      file_size = f.tell()

      # empty file
      if file_size == 0:
          print('File is empty')
          return None

      # single char file
      if file_size == 1:
          char = f.read(1)
          if char != b'\n' and char != b'\r':
              return char.decode()
          return None

      # File has at least 2 chars

      # Get the last two chars
      f.seek(-2, os.SEEK_END)

      # char 1 and char 2 are the last two chars in direct order
      # in the first read, char2 is the last char
      char1 = f.read(1)
      char2 = f.read(1)

      # if the file has only two chars
      if file_size == 2:
        if (char1+char2) in [b'\r\n', b'\n\r', b'\r\r', b'\n\n']:
          return None
        elif char1 not in [b'\r', b'\n'] and char2 in [b'\r', b'\n']:
          return char1.decode()
        elif char2 not in [b'\r', b'\n']:
          return char2.decode()

      # File has more than two chars

      # Move to the third last char
      f.seek(-3, os.SEEK_END)

      # k is the byte position from the end of the file
      k = 0
      while(True):
          k+=1
          if char1 == b'\r' and char2 == b'\n':
              if(k > 1):
                print("Windows newline")
                f.seek(3, os.SEEK_CUR)
                return f.readline().decode()
          elif char1 == b'\n':
              if(k > 1):
                print("Linux newline")
                f.seek(2, os.SEEK_CUR)
                return f.readline().decode()
          elif char1 == b'\r':
              if(k > 1):
                print("Mac newline")
                f.seek(2, os.SEEK_CUR)
                return f.readline().decode()
          try:
            char2 = char1
            char1 = f.read(1)
            f.seek(-2, os.SEEK_CUR)
          except:
              f.seek(-1, os.SEEK_CUR)
              return f.readline().decode()
