import re
from copy import deepcopy
from pymorphy2 import MorphAnalyzer


def intersect(list1, list2):
    result = []
    idx = 0
    step = 5
    for number in list1:
        while idx + step < len(list2) and list2[idx + step] <= number:
            idx += step
        while idx + 1 < len(list2) and list2[idx + 1] <= number:
            idx += 1
        if list2[idx] == number:
            result.append(number)

    return result


class InvertedIndex:
    def __init__(self, save_documents=True):
        self.index = dict()
        self.documents = dict()
        self.morph = MorphAnalyzer()
        self.save_documents = save_documents

    def add_document(self, document):
        document_number = len(self.documents)
        if self.save_documents:
            self.documents[document_number] = document
        else:
            self.documents[document_number] = None

        words = re.sub(r'[^\w\s]', '', document.lower()).split()
        for word in words:
            word = word.strip()
            word = self.morph.normal_forms(word)[0]

            if word in self.index.keys():
                if len(self.index[word]) > 0 and self.index[word][-1][0] == document_number:
                    self.index[word][-1][1] += 1
                else:
                    self.index[word].append([document_number, 1])
            else:
                self.index[word] = [[document_number, 1]]

        return document_number

    def find_quote(self, quote):
        words = re.sub(r'[^\w\s]', '', quote.lower()).split()
        if len(words) == 0:
            return []
        documents = []
        for word in words:
            word = word.strip()
            word = self.morph.normal_forms(word)[0]
            if word not in self.index.keys():
                return []
            else:
                documents.append([record[0] for record in self.index[word]])

        documents.sort(key=lambda x: len(x))
        current_list = deepcopy(documents[0])
        for record in documents[1:]:
            current_list = intersect(current_list, record)

        return [(number, self.documents[number]) for number in current_list]


if __name__ == '__main__':
    print(intersect([2 * x for x in range(100)] + [205, 255], [5 * x for x in range(50)]))
