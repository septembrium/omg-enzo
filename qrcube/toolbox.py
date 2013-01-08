#-------------------------------------------------------------------------------
# Name:        toolbox.py
# Purpose:     make a little library of reusable code
#
# Author:      bert heymans
#
# Created:     08/12/2010
#-------------------------------------------------------------------------------
#!/usr/bin/env python
"""
A Python coding toolbox by Bert Heymans.

TODO:
    - create random string
    - clean up ensure proper newline
    - unit tests
"""
import time
import os
import random
import unittest
import sys

debug = False

WINDOWS_NEWLINE = '\r\n'
UNIX_NEWLINE = '\n'
OS9_NEWLINE = '\r'

# project config helper
import default_config
sys.path.append(default_config.LIBS_DIR)

class NoDataProvidedError(Exception): pass
class FolderDoesNotExistError(Exception): pass

## UNIT TESTS

class ToolsForStrings(unittest.TestCase):
    """
    testcase for testing string operation related tool functions
    """
    def test_random_string(self):
        result = random_string(20)
        self.assertEqual(20, len(result))
        self.assertEqual(-1, result.find(' '))

    def test_ensure_windows_newline(self):
        text = "the quick \n brown fox \r\n jumps over \r\n the lazy \
dog \n\n\n"
        self.assertEqual(ensure_windows_newline(text), "the quick \r\n brown \
fox \r\n jumps over \r\n the lazy dog \r\n\r\n\r\n")

    def test_string_has_content(self):
        self.assertFalse(string_has_content(None), "None is not content")
        self.assertFalse(string_has_content(5), "an integer is not a string")
        self.assertFalse(string_has_content(''), "an empty string has no content")
        self.assertFalse(string_has_content('       '), "all spaces does not count as content")
        self.assertTrue(string_has_content('I have content'), "a string like \
    'I have content' should count as content")

## END OF UNIT TESTS
## START OF TOOLS

def random_string(length):
    """
    returns a random string of a given length, it will only contain ascii characters and will not contain spaces
    """
    res = []
    for i in range(0, length):
        val = random.randint(33, 126) # 33 - 126 decimal are visible printable characters in ascii, 32 is the space character
        res.append(chr(val))
    return ''.join(res)

def random_identifier():
    ''' time and random, no guarantee that it's unique '''
    timepart = str(time.time())[-5:].replace('.','')
    rndpart = str(random.random())[-5:].replace('.','')
    return ''.join([timepart, rndpart])

def ensure_windows_newline(text):
    """
    ensures that all the newlines are in a Windows OS flavor
    note: quick and dirty, needs cleanup
    """
    # replace all proper windows newline combinations with a scrambled string
    scramble = random_string(20)
    while text.find(scramble) <> -1:
        scramble = random_string(30)
    text = text.replace(WINDOWS_NEWLINE,scramble)
    text = text.replace(UNIX_NEWLINE, WINDOWS_NEWLINE)
    text = text.replace(WINDOWS_NEWLINE,scramble)
    text = text.replace(OS9_NEWLINE, WINDOWS_NEWLINE)
    text = text.replace(scramble, WINDOWS_NEWLINE)
    return text


# debugging with unicode confidence
def log_if_debug(*to_print):
	"""
	takes any mount of arguments to print, prints them if the toolbox debug boolean is set to True
	"""
	for part in to_print:
		if debug:
			if isinstance(part, unicode): print part.encode('utf8')
			else: print part

# write files with timestamps, timestamps that save humans!
def write_file(name=None, extension='txt', data=None, timestamp=False):
    '''
    name = full file path
    extension = no dot
    data = what to write
    timestamp = set True if needed, appended before extension

    writes data to a named file, adds a timestamp to the beginning of the provided file name
	if html or xml extension, it will prettify the output
    '''
    if data:
        if timestamp:
            filename = name + str(time.time()) + '.' + extension
        else:
            filename = name + '.' + extension
        timestamped_file = open(filename, 'wb') # binary write!!
        timestamped_file.write(data)
        timestamped_file.close()
    else:
        raise NoDataProvidedError, 'no data provided, refusing to create an empty file'

def string_has_content(cont):
    """
    checks if the a value is a string and if it has characters other than spaces
    """
    return cont and type(cont) == str and not len(cont) == 0 and not cont.isspace()

def sql_escape_string(text):
    """
    looks for single quotes in a string and inserts a single quote next to it
    this escapes the ' characters in an sql string (' -> '')
    """
    text_length = len(text)
    i = 0
    while i < text_length:
        if text[i] == "'":
            text_list = list(text)
            text_list.insert(i,"'")
            text = ''.join(text_list)
            text_length += 1
            i += 1
        i += 1
    return text

# yield input stream handles of every file with a certain extension in a folder (does not walk tree)
def all_files_in_folder(path, file_has_extension=None, filename_must_contain=None, keep_open=False):
    """
    generator returning input stream of every file matching expectation
    yields tuple <extension stripped filename, file content stream>
    """
    if os.path.exists(path):
        filenames = os.listdir(path)
    else:
        raise FolderDoesNotExistError
    for filename in filenames:
        full_file_path = path+filename
        # only handle files
        if not os.path.isfile(full_file_path):
            continue
        # skip files not having a certain extension
        if file_has_extension and not file_has_extension == filename.split('.')[-1]:
            continue
        # skip files not containing a certain string
        if filename_must_contain and not filename.find(filename_must_contain) == -1:
            continue
        if filename.find('.') == -1:
            stripped_name = filename
        else:
            stripped_name = filename.split('.')[0]

        log_if_debug('reading: ', full_file_path)
        try:
            input_file = open(full_file_path, 'rb') # maybe make this read binary in the future, not touching it for now
            yield (stripped_name, input_file)
        except (IOError, OSError):
            print 'ERROR reading: ', full_file_path
            sys.exit(2)
        finally:
            if not keep_open:
                log_if_debug('closing: ', full_file_path)
                input_file.close()

class SettingsObject(object):
    """
    singleton holding settings
    """
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(SettingsObject, self).__new__(self, *args, **kwargs)
        self._instance.update_with_module(default_config)
        return self._instance

    def update_with_module(self, module):
        """
        add module values to settings
        """
        for name, value in module.__dict__.iteritems():
            setattr(self, name, value)
        return self

    @classmethod
    def from_module(self, module):
        """
        create instance with values based on ones from passed module
        """
        settings = self()
        settings.update_with_module(module)
        return settings

    def update_with_file(self, filepath):
        """
        updates the settings with the given module file
        TODO: is this type of loading modules safe?
        """
        sys.path.insert(0, os.path.dirname(filepath))
        module_name = os.path.splittext(os.path.basename(filepath))[0]
        return self.update_with_module(__import__(module_name))

settings = SettingsObject()

if __name__ == "__main__":
    #run all tests
    unittest.main()
