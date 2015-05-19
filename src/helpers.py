import codecs, fnmatch, os

def detectEncoding(filename):
    encodings = ['utf-8', 'ascii', 'cp1250', 'cp1252', 'latin1', 'latin2']
    for en in encodings:
        try:
            with codecs.open(filename, 'r', encoding=en) as f:
                for l in range(200):
                    line = f.readline()
                    if "áè" in line or "¾" in line or "ï" in line or "" in line:
                        # print(line)
                        raise UnicodeError()
                return en
        except UnicodeError:
            pass
    raise UnicodeError("Undetected encoding of file: %s" % filename)

def glob_recursively(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
