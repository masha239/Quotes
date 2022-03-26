import pickle
from inverted_index import InvertedIndex


def create_inverted_index(infile='chekhov.pkl'):
    with open(infile, 'rb') as f:
        letters = pickle.load(f)

    index = InvertedIndex()
    for letter in letters:
        index.add_document(letter)
    return index


if __name__ == "__main__":
    test_qoutes = ['фотографию буду хранить',
                   'Интернета тогда еще не было!',
                   'мы и собака',
                   'Если он в Петербурге, то будьте добры, скажите ему,',
                   'чтобы он поскорее прислал мне обещанные фотографии.']

    index = create_inverted_index()
    for quote in test_qoutes:
        res = index.find_quote(quote)
        print(f'Found {len(res)} letters for quote "{quote}":')
        for doc in res:
            print(doc[0])
        print()
