import os

def initial_search(f):
        # Find file size
    f.seek(0, 2)
    file_size = f.tell()

    # empty file
    if file_size == 0:
        # File is empty
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

    return [char1, char2]

def search_from(f, n):
  f.seek(0)
  f.seek(n)

  char1 = f.read(1)
  char2 = f.read(1)

  # k is the byte position from the end of the file
  k = 0

  cur = f.tell()

  while(True):
      k+=1
      cur = f.tell()
      if char1 == b'\r' and char2 == b'\n':
          if(k > 1):
            # "Windows newline"
            f.seek(3, os.SEEK_CUR)
            return 2, cur, f.readline().decode()
      elif char1 == b'\n':
          if(k > 1):
            # Linux newline
            f.seek(2, os.SEEK_CUR)
            return 1, cur, f.readline().decode()
      elif char1 == b'\r':
          if(k > 1):
            # Mac newline
            f.seek(2, os.SEEK_CUR)
            return 1, cur, f.readline().decode()

      try:
        char2 = char1
        char1 = f.read(1)
        f.seek(-2, os.SEEK_CUR)
      except:
        f.seek(-1, os.SEEK_CUR)
        return 0, cur, f.readline().decode()

def tail(filename, n=1):
  if n < 1:
     n = 1

  with open(filename, "rb") as f:
      retval = initial_search(f)

      # check if x type is an array:
      if type(retval) is not list:
         return retval

      f.seek(-2, os.SEEK_END)
      cur = f.tell()

      step = 1
      lines = []
      while(step > 0):
        step, cur, line = search_from(f, cur)
        lines.insert(0, line)
        cur -= (step+1)
        if len(lines) == n:
          break

      print(lines)

      return lines

def tail_index(filename, index=1):
  if os.path.isfile(filename) == False:
    return []

  with open(filename, "rb") as f:
    retval = initial_search(f)

    # check if x type is an array:
    if type(retval) is not list:
        return retval

    f.seek(-2, os.SEEK_END)
    cur = f.tell()

    step = 1
    lines = []
    while(True):
      step, cur, line = search_from(f, cur)
      lines.insert(0, line.strip())
      cur -= (step+1)

      if step == 0:
        break

      line_index = int(line.split('\t')[1])

      if index > 0:
        if index > line_index:
          return []
        if(index == line_index):
          break

    return lines

def lines2rowcol(lines):
  if lines == None:
    return []
  rows = []
  for row in lines:
    cols = []
    for col in row.split('\t'):
      cols.append(col.strip())
    rows.append(cols)

  return rows
