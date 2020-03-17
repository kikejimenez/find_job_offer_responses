import os, sys, shutil
from random import shuffle as Shuffle
from pathlib import Path

PARENT_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

sys.path.append(os.path.join(PARENT_DIR, 'src'))
from letter_body import multiproc_letter_body

import subprocess, tempfile

import pandas as pd


def test_multiproc_letter_body1():

    opening_file = os.path.join(PARENT_DIR, 'data/opening_closing/opening.csv')
    closing_file = os.path.join(PARENT_DIR, 'data/opening_closing/closing.csv')

    openings = [line.strip().lower() for line in open(opening_file)]
    closings = [line.strip().lower() for line in open(closing_file)]

    accept_dir = os.path.join(PARENT_DIR, 'data/raw/accept')
    decline_dir = os.path.join(PARENT_DIR, 'data/raw/decline')

    nb_files = 20

    with tempfile.TemporaryDirectory() as tmpdirname:

        def make_samples(directory):
            all_files = [
                os.path.join(directory, file) for file in os.listdir(directory)
            ]
            Shuffle(all_files)
            temp_dir = os.path.join(tmpdirname, directory.split('/')[-1])
            os.mkdir(temp_dir)

            for file in all_files[:nb_files]:
                new_file = os.path.join(temp_dir, file.split('/')[-1])
                shutil.copyfile(file, new_file)

            return temp_dir

        accept_dir = make_samples(accept_dir)
        decline_dir = make_samples(decline_dir)

        dirs = [accept_dir, decline_dir]

        proc_data_file = os.path.join(tmpdirname, 'documents.csv')

        print('One processes')

        multiproc_letter_body(
            openings=openings,
            closings=closings,
            src_dirs=dirs,
            dst_file=proc_data_file,
            processes=1
        )
        print(pd.read_csv(proc_data_file, header=None))
        os.remove(proc_data_file)

        print('Three processes')

        multiproc_letter_body(
            openings=openings,
            closings=closings,
            src_dirs=dirs,
            dst_file=proc_data_file,
            processes=3
        )

        print(pd.read_csv(proc_data_file, header=None))


def test_multiproc_letter_body2():

    text1 = '''
    Dear Mr. Hynes,

    Write Text Here

    Again, thank you very much.

    Handwritten Signature (hard copy letter)
    Jason Burnett
    '''

    text2 = '''
    Dear Mr Kelly

    Write Text Here

    Sincerely

    Your signature
    Typed name
    '''

    text3 = text1 + '\n' + text2

    openings = [
        'hello', 'good morning', 'good afternoon', 'hi', 'dear',
        'to whom it may concern', 'my darling'
    ]

    closings = [
        'best', 'my best', 'regards', 'respectfully', 'sincerely', 'thank you',
        'yours', 'cordially', 'with appreciation', 'with gratitude',
        'with sincere'
    ]

    opening_file = os.path.join(PARENT_DIR, 'data/opening_closing/opening.csv')
    closing_file = os.path.join(PARENT_DIR, 'data/opening_closing/closing.csv')

    openings = [line.strip().lower() for line in open(opening_file)]
    closings = [line.strip().lower() for line in open(closing_file)]

    arr_texts = [text1, text2, text3]

    with tempfile.TemporaryDirectory() as tmpdirname:

        for k, text in enumerate(arr_texts):
            new_file = os.path.join(tmpdirname, str(k) + '.txt')
            with open(new_file, 'w') as new_f:
                new_f.write(text)

        dirs = [tmpdirname]

        proc_data_file = os.path.join(tmpdirname, 'documents.csv')

        multiproc_letter_body(
            openings=openings,
            closings=closings,
            src_dirs=dirs,
            dst_file=proc_data_file,
            processes=1
        )

        print(pd.read_csv(proc_data_file, header=None))


if __name__ == "__main__":

    test_multiproc_letter_body2()
    test_multiproc_letter_body1()