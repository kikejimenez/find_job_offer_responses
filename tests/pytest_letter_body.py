import os, sys
from pathlib import Path
PARENT_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

sys.path.append(os.path.join(PARENT_DIR))
from src.letter_body import is_valid_string, find_text, load_letter_body


def test_is_valid_string():

    assert is_valid_string(
        substrings=['hello', 'hi'], string='hello mr. enrique'
    )
    assert is_valid_string(
        substrings=['bye', 'thank you'], string='Again, thank you very much.'
    )

    assert not is_valid_string(
        substrings=['hello', 'hi'],
        string='i said hi before cause it is important'
    )


def test_find_text():
    #Test find_text
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

    assert find_text(openings, closings, text1) == ['write text here']
    assert find_text(openings, closings, text2) == ['write text here']
    assert find_text(openings, closings,
                     text3) == ['write text here', 'write text here']


def test_load_letter_body():

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

    read_files = [text1, text2, text3]

    results = load_letter_body(openings, closings, read_files)
    print(results)
    assert results.shape == (4, )


if __name__ == "__main__":
    test_load_letter_body()