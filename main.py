# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
text1 = '''
Dear Mr. Hynes,

As we discussed on the phone, I am very pleased to accept the position of Advertising Assistant with Smithfield Granite and Stonework. Thank you again for the opportunity. I am eager to make a positive contribution to the company and to work with everyone on the Smithfield team.

As we discussed, my starting salary will be $48,000 and health and life insurance benefits will be provided after 30 days of employment.

I look forward to starting employment on July 1, 20XX. If there is any additional information or paperwork you need prior to then, please let me know.

Again, thank you very much.

Handwritten Signature (hard copy letter)

Jason Burnett
'''


text2 = '''
Dear Mr Kelly

Thank you very much for offering me the position of Customer Service Manager with XYZ Corporation.

While I understand the position and your company offer a great deal to a prospective employee, I have had another offer which I believe more closely matches what I am looking for. Therefore, after giving it much careful thought, I must decline your offer.

Thank you for your time and effort. I wish you and your company well.

Sincerely

Your signature
Typed name
'''
# -

a = iter(x for x in (1,2,3))

# +
# #!pip install nltk
# -

openings = [line.strip().lower() for line in open('./data/opening_closing/opening.csv')]
closings = [line.strip().lower() for line in open('./data/opening_closing/closing.csv')]

# +
import string as String

from nltk.tokenize import sent_tokenize, word_tokenize
def is_substring_in_string(substring,string):
    '''Two criteria for a substring to be contained in string'''
    string = string.strip().lower()
    substring = substring.strip().lower()
    set_token = lambda sent: set(word_tokenize(sent))
    
    if not substring in string:
        return False    
    if not set_token(substring).issubset(set_token(string)):
        return False
    
    return True
    
def is_valid_string(substrings,string):
    '''A valid string is an opening or a closing'''
    length = len([token for token in word_tokenize(string) if token not in String.punctuation])
    if length > 6:
        return False
    return any(is_substring_in_string(substring,string) for substring in substrings)
    


# -

#should return True
string = 'Dear Mr. Hynes,'
substrings = ['hello','dear']
is_valid_string(substrings,string)

#should return True
string = 'Again, thank you very much.'
substrings = ['bye','thank you']
is_valid_string(substrings,string)

#should return False
string = 'i said hi before cause it is important'
substrings = ['hello','hi']
is_valid_string(substrings,string) 


def find_text(openings,closings,text):
    '''Results are openings or closings'''
   
    isopening, isclosing = False, False
    lines = [line.strip() for line in text.split('\n') if line]

    results = []
    
    
    for k,line in enumerate(lines):
       
        if isopening and isclosing:
            result = '\n'.join(lines[nb_open:nb_close])
            results.append(result)
            isopening, isclosing = False, False
            
        if not isopening:
            isopening = is_valid_string(openings,line)
            nb_open = k + 1

        elif not isclosing:
            isclosing = is_valid_string(closings,line)
            nb_close = k
            
    return results       
            

# +
#Test find_text
text1 = '''
Dear Mr. Hynes,

As we discussed on the phone, I am very pleased to accept the position of Advertising Assistant with Smithfield Granite and Stonework. Thank you again for the opportunity. I am eager to make a positive contribution to the company and to work with everyone on the Smithfield team.
As we discussed, my starting salary will be $48,000 and health and life insurance benefits will be provided after 30 days of employment.
I look forward to starting employment on July 1, 20XX. If there is any additional information or paperwork you need prior to then, please let me know.

Again, thank you very much.

Handwritten Signature (hard copy letter)
Jason Burnett
'''


text2 = '''
Dear Mr Kelly

Thank you very much for offering me the position of Customer Service Manager with XYZ Corporation.
While I understand the position and your company offer a great deal to a prospective employee, I have had another offer which I believe more closely matches what I am looking for. Therefore, after giving it much careful thought, I must decline your offer.
Thank you for your time and effort. I wish you and your company well.

Sincerely

Your signature
Typed name
'''

openings = ['hello', 'good morning', 'good afternoon', 'hi', 'dear', 'to whom it may concern', 'my darling']

closings = ['best', 'my best', 'regards', 'respectfully', 'sincerely',
            'thank you', 'yours', 'cordially', 'with appreciation',
            'with gratitude', 'with sincere']


# -

find_text(openings,closings,text1.lower())

find_text(openings,closings,text2.lower())

text3 = text1+'\n'+text2
find_text(openings,closings,text3.lower())

# +
# #!pip install nltk

# +
## Declines

# +
import os
import pandas as pd
data_dir = 'data/raw/accept'
files = [os.path.join(data_dir,fn) for fn in os.listdir(data_dir)[:15]]

def file_to_sentences(file):
    text =open(file).read()
    return sentencize_findings(openings,closings,text)

def dir_to_sentences(files):
    return (sent for file in files for sent in file_to_sentences(file))

documents = pd.Series(dir_to_sentences(data_dir))
files

# +
import os
import pandas as pd
data_dir = 'data/raw/accept'

def load_data(data_dir):
    file_paths = [os.path.join(data_dir,fn) for fn in os.listdir(data_dir)[:15]]
    read_files = (open(path).read() for path in file_paths)
    return (result for read_f in read_files for result in find_text(openings,closings,read_f.lower()))

documents = pd.Series(load_data(data_dir))

# -

documents.shape

documents.drop_duplicates().shape



[document for document in documents.values[:20]]

[i for i in documents[:100]]


