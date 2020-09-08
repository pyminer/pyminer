# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing various functions/classes needed everywhere within eric6.
"""
import os
import re
from codecs import BOM_UTF8, BOM_UTF16, BOM_UTF32

try:
    EXTSEP = os.extsep
except AttributeError:
    EXTSEP = "."
codingBytes_regexps = [
    (5, re.compile(br'''coding[:=]\s*([-\w_.]+)''')),
    (1, re.compile(br'''<\?xml.*\bencoding\s*=\s*['"]([-\w_.]+)['"]\?>''')),
]


def decode(text):
    """
    Function to decode some byte text into a string.
    
    @param text byte text to decode (bytes)
    @return tuple of decoded text and encoding (string, string)
    """
    try:
        if text.startswith(BOM_UTF8):
            # UTF-8 with BOM
            return str(text[len(BOM_UTF8):], 'utf-8'), 'utf-8-bom'
        elif text.startswith(BOM_UTF16):
            # UTF-16 with BOM
            return str(text[len(BOM_UTF16):], 'utf-16'), 'utf-16'
        elif text.startswith(BOM_UTF32):
            # UTF-32 with BOM
            return str(text[len(BOM_UTF32):], 'utf-32'), 'utf-32'
        coding = get_codingBytes(text)
        if coding:
            return str(text, coding), coding
    except (UnicodeError, LookupError):
        pass

    # Assume UTF-8
    try:
        return str(text, 'utf-8'), 'utf-8-guessed'
    except (UnicodeError, LookupError):
        pass

    guess = None
    # Try the universal character encoding detector
    try:
        import chardet
        guess = chardet.detect(text)
        if (
                guess and
                guess['confidence'] > 0.95 and
                guess['encoding'] is not None
        ):
            codec = guess['encoding'].lower()
            return str(text, codec), '{0}-guessed'.format(codec)
    except (UnicodeError, LookupError):
        pass
    except ImportError:
        pass

    # Try default encoding
    try:
        codec = Preferences.getEditor("DefaultEncoding")
        return str(text, codec), '{0}-default'.format(codec)
    except (UnicodeError, LookupError):
        pass

    # Use the guessed one even if confifence level is low
    if guess and guess['encoding'] is not None:
        try:
            codec = guess['encoding'].lower()
            return str(text, codec), '{0}-guessed'.format(codec)
        except (UnicodeError, LookupError):
            pass

    # Assume UTF-8 loosing information
    return str(text, "utf-8", "ignore"), 'utf-8-ignore'


def get_codingBytes(text):
    """
    Function to get the coding of a bytes text.

    @param text bytes text to inspect (bytes)
    @return coding string
    """
    lines = text.splitlines()
    for coding in codingBytes_regexps:
        coding_re = coding[1]
        head = lines[:coding[0]]
        for line in head:
            m = coding_re.search(line)
            if m:
                return str(m.group(1), "ascii").lower()
    return None


def readEncodedFile(filename):
    """
    Function to read a file and decode its contents into proper text.
    
    @param filename name of the file to read (string)
    @return tuple of decoded text and encoding (string, string)
    """
    f = open(filename, "rb")
    text = f.read()
    f.close()
    return decode(text)


def joinext(prefix, ext):
    """
    Function to join a file extension to a path.
    
    The leading "." of ext is replaced by a platform specific extension
    separator if necessary.
    
    @param prefix the basepart of the filename (string)
    @param ext the extension part (string)
    @return the complete filename (string)
    """
    if ext[0] != ".":
        ext = ".{0}".format(ext)
        # require leading separator to match os.path.splitext
    return prefix + EXTSEP + ext[1:]


def getDirs(path, excludeDirs):
    """
    Function returning a list of all directories below path.
    
    @param path root of the tree to check
    @param excludeDirs basename of directories to ignore
    @return list of all directories found
    """
    try:
        names = os.listdir(path)
    except EnvironmentError:
        return []

    dirs = []
    for name in names:
        if (
                os.path.isdir(os.path.join(path, name)) and
                not os.path.islink(os.path.join(path, name))
        ):
            exclude = 0
            for e in excludeDirs:
                if name.split(os.sep, 1)[0] == e:
                    exclude = 1
                    break
            if not exclude:
                dirs.append(os.path.join(path, name))

    for name in dirs[:]:
        if not os.path.islink(name):
            dirs = dirs + getDirs(name, excludeDirs)

    return dirs


def isWindowsPlatform():
    return os.name == 'nt'
