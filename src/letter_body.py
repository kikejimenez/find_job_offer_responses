''' Select from webpages the body of a letter
'''

import os
import logging
from multiprocessing import Pool
from functools import partial as Partial
import string as String
from pathlib import Path

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd

nltk.download('punkt')
PARENT_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

logging.basicConfig(level=logging.DEBUG)


def is_substring_in_string(substring, string):
    '''Returns True if all the characters and the words of the substrings are 
       contained in the string. False otherwise.
    '''
    string = string.strip().lower()
    substring = substring.strip().lower()
    set_token = lambda sent: set(word_tokenize(sent))

    if not (substring in string):
        return False
    if not set_token(substring).issubset(set_token(string)):
        return False

    return True


def is_valid_string(substrings, string):
    '''Returns True if the string has less than six words and 
       contains any of the substrings
    '''
    length = len(
        [
            token for token in word_tokenize(string)
            if token not in String.punctuation
        ]
    )
    if length > 6:
        return False
    return any(
        is_substring_in_string(substring, string) for substring in substrings
    )


def find_text(openings, closings, text):
    '''Return all the pieces of the text that are between of any 
       of the openings and closings
    '''

    isopening, isclosing = False, False
    lines = [line.lower().strip() for line in text.split('\n') if line]
    results = []

    for k, line in enumerate(lines):

        if isopening and isclosing:
            result = '\n'.join(lines[nb_open:nb_close])
            results.append(result)
            isopening, isclosing = False, False

        if not isopening:
            isopening = is_valid_string(openings, line)
            nb_open = k + 1

        elif not isclosing:
            isclosing = is_valid_string(closings, line)
            nb_close = k

    return results


def load_letter_body(openings, closings, read_files):
    ''' Returns a pandas Series with the resulting body letters
    '''

    return pd.Series(
        result for read_f in read_files
        for result in find_text(openings, closings, read_f.lower())
    )


def load_accept_and_decline(openings, closings, dirs):
    file_paths = []
    for letters_dir in dirs:
        file_paths.extend(
            [os.path.join(letters_dir, fn) for fn in os.listdir(letters_dir)]
        )

    read_files = (open(path).read() for path in file_paths)

    return load_letter_body(openings, closings, read_files)


def letters_body_to_file(read_files, openings, closings, dst_file):

    logging.info('Loading the body of the letters...')

    documents = load_letter_body(
        openings=openings, closings=closings, read_files=read_files
    )

    documents.to_csv(dst_file, mode='a+', header=None, index=False)


def multiproc_letter_body(openings, closings, src_dirs, dst_file, processes=1):

    load_f = Partial(
        letters_body_to_file,
        openings=openings,
        closings=closings,
        dst_file=dst_file
    )

    file_paths = []
    for letters_dir in src_dirs:
        file_paths.extend(
            [os.path.join(letters_dir, fn) for fn in os.listdir(letters_dir)]
        )

    def chunks(file_paths, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(file_paths), n):
            yield [open(path).read() for path in file_paths[i:i + n]]

    chunk_size = len(file_paths) // processes
    with Pool(processes=processes) as procs:

        procs.map(
            func=load_f, iterable=chunks(file_paths=file_paths, n=chunk_size)
        )


if __name__ == "__main__":

    opening_file = os.path.join(PARENT_DIR, 'data/opening_closing/opening.csv')
    closing_file = os.path.join(PARENT_DIR, 'data/opening_closing/closing.csv')

    openings = [line.strip().lower() for line in open(opening_file)]
    closings = [line.strip().lower() for line in open(closing_file)]

    accept_dir = os.path.join(PARENT_DIR, 'data/raw/accept')
    decline_dir = os.path.join(PARENT_DIR, 'data/raw/decline')
    dirs = [accept_dir, decline_dir]

    proc_data_file = os.path.join(PARENT_DIR, 'data/proc/documents.csv')

    multiproc_letter_body(
        openings=openings,
        closings=closings,
        src_dirs=dirs,
        dst_file=proc_data_file,
        processes=8
    )
