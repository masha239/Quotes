import pickle
from inverted_index import InvertedIndex

with open('chehow.pkl', 'rb') as f:
    letters = pickle.load(f)

chehow_index = InvertedIndex()
for letter in letters:
    chehow_index.add_document(letter)

test_qoutes = ['фотографию буду хранить',
               'Интернета тогда еще не было!',
               'мы и собака',
               'Если он в Петербурге, то будьте добры, скажите ему,',
               'чтобы он поскорее прислал мне обещанные фотографии.']

for quote in test_qoutes:
    res = chehow_index.find_quote(quote)
    print(f'Found {len(res)} letters for quote "{quote}":')
    for doc in res:
        print(doc[0])
    print()



