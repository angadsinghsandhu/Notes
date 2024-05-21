import re
import argparse
from itertools import groupby

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
# from xgboost import XGBClassifier
from sklearn.metrics import classification_report


class SegmentClassifier:
    def train(self, trainX, trainY):
        # self.create_pos_dict()
        self.create_word_pos_mapping()
        # self.clf = DecisionTreeClassifier()  # TODO: experiment with different models
        # self.clf = LogisticRegression()
        # self.clf = GaussianNB()
        # self.clf = SVC()
        # self.clf = KNeighborsClassifier()
        self.clf = RandomForestClassifier(n_estimators=3500, criterion='entropy')
        # self.clf = MLPClassifier(hidden_layer_sizes=(15, 15, 15), solver='lbfgs', max_iter=500)
        # self.clf = XGBClassifier()

        X = [self.extract_features(x) for x in trainX]
        self.clf.fit(X, trainY)

    def create_pos_dict(self):
        self.pos_dict = {}
        self.pos_ct = 0
        self.pos = load_wordlist('part-of-speech.list')
        for pos in self.pos:
            self.pos_dict[pos] = self.pos_ct
            self.pos_ct += 1

    def create_word_pos_mapping(self):
        self.word_pos_map = {}
        self.pos_dict = {}
        self.pos_ct = 0

        self.pos_list = load_wordlist('part-of-speech.histogram')
        for word in self.pos_list:
            word_entity = word.split(' ')
            freq, word, pos = word_entity[0], word_entity[1], word_entity[-1]
            if pos not in self.pos_dict:
                self.pos_dict[pos] = self.pos_ct
                self.pos_ct += 1
            word = word.lower()
            self.word_pos_map[word] = pos

    def extract_features(self, text):
        # numbers = sum(c.isalpha() for c in text) / len(text)
        # letters = sum(c.isalpha() for c in text) / len(text)
        # spaces = sum(c.isspace() for c in text) / len(text)
        # others = (len(text) - numbers - letters - spaces) / len(text)

        self.len_prev_line = -1
        words = text.split()

        # counting number of pos
        pos_counts = {}
        for pos in self.pos_dict.keys():
            pos_counts[pos] = 0
        for word in words:
            word = word.lower()
            if word in self.word_pos_map:
                try:
                    pos_counts[self.word_pos_map[word]] += 1
                except KeyError:
                    pass

        if self.len_prev_line == -1:
            self.bos = True
            self.len_prev_line = len(words)

        # check if the text is a mail
        try_find_address = False
        if re.match(
                '^From|^Article|^Path|^Newsgroups|^Subject|^Date|^Organization|^Lines|^Approved|^Message-ID|^References',
                words[0]):
            try_find_address = True

        features = [  # TODO: add features here
            len(text),
            len(text.strip()),
            len(words),
            # numbers,
            # letters,
            # spaces,
            # others,
            # quotation or article start
            sum(1 if re.match('^(>|:|\s*\S*\s*>|@)', word)  # quotation starts
                     or re.match('^.+(wrote|writes|said|told|says|tells):', word) else 0 for word in words),  # articles
            text.count(' '),  # number of spaces to detect blank lines
            # figures
            text.count('|') + text.count('-') + text.count('+') + text.count('_') + text.count('\\') + text.count('/'),
            sum(1 if w.isupper() else 0 for w in words) / len(words),  # uppercase chars ratio
            sum(1 if w.isnumeric() else 0 for w in words) / len(words),  # numeric chars ratio
            1 if try_find_address else 0,  # if any "headline" keyword found
            # len(re.sub('[\w]+', '', text)),  # number of non word chars (special chars) -- doesn't work well
            len(re.sub('[\w]+', '', text)),  # number of non word chars (special chars)
            sum(1 if re.match('^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', word)  # for emails
                     or re.match('^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$', word) else 0 for word in words),  # phone number
            # for tables, if len of words in current line matches prev line
            1 if self.bos or self.len_prev_line - 1 < len(words) < self.len_prev_line + 1 else 0,
            # text.count(''),
            *pos_counts.values(),
        ]
        self.bos = False
        self.len_prev_line = len(words)

        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)


def load_wordlist(file):
    with open(file) as fin:
        return set([x.strip() for x in fin.readlines()])


def load_data(file):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split('\t', 1)
            if arr[0] == '#BLANK#':
                continue
            X.append(arr[1])
            y.append(arr[0])
        return X, y


def lines2segments(trainX, trainY):
    segX = []
    segY = []
    for y, group in groupby(zip(trainX, trainY), key=lambda x: x[1]):
        if y == '#BLANK#':
            continue
        x = '\n'.join(line[0].rstrip('\n') for line in group)
        segX.append(x)
        segY.append(y)
    return segX, segY


def evaluate(outputs, golds):
    correct = 0
    for h, y in zip(outputs, golds):
        if h == y:
            correct += 1
    print(f'{correct} / {len(golds)}  {correct / len(golds)}')


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True)
    parser.add_argument('--test', required=True)
    parser.add_argument('--format', required=True)
    parser.add_argument('--output')
    parser.add_argument('--errors')
    parser.add_argument('--report', action='store_true')
    return parser.parse_args()


def main():
    args = parseargs()

    trainX, trainY = load_data(args.train)
    testX, testY = load_data(args.test)

    if args.format == 'segment':
        trainX, trainY = lines2segments(trainX, trainY)
        testX, testY = lines2segments(testX, testY)

    classifier = SegmentClassifier()
    classifier.train(trainX, trainY)
    outputs = classifier.classify(testX)

    if args.output is not None:
        with open(args.output, 'w') as fout:
            for output in outputs:
                print(output, file=fout)

    if args.errors is not None:
        with open(args.errors, 'w') as fout:
            for y, h, x in zip(testY, outputs, testX):
                if y != h:
                    print(y, h, x, sep='\t', file=fout)

    if args.report:
        print(classification_report(testY, outputs))
    else:
        evaluate(outputs, testY)


if __name__ == '__main__':
    main()
