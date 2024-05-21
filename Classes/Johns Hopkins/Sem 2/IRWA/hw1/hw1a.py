import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# import spacy
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
from sklearn.metrics import classification_report

# nlp = spacy.load("en_core_web_sm")


class EOSClassifier:
    def train(self, trainX, trainY):
        # HINT!!!!!
        # (The following word lists might be very helpful.)
        self.abbrevs = load_wordlist('abbrevs')
        self.sentence_internal = load_wordlist("sentence_internal")
        self.timeterms = load_wordlist("timeterms")
        self.titles = load_wordlist("titles")
        self.places = load_wordlist("places")
        self.unlikely_proper_nouns = load_wordlist("unlikely_proper_nouns")
        self.pos_dict = {}
        self.pos_ct = 0

        # In this part of the code, we're loading a Scikit-Learn model.
        # We're using a DecisionTreeClassifier... it's simple and lets you
        # focus on building good features.
        # Don't start experimenting with other models until you are confident
        # you have reached the scoring upper bound.
        # self.clf = DecisionTreeClassifier()  # TODO: experiment with different models
        # self.clf = LogisticRegression()
        # self.clf = GaussianNB()
        # self.clf = SVC()
        # self.clf = KNeighborsClassifier()
        self.clf = RandomForestClassifier()
        # self.clf = XGBClassifier()
        X = [self.extract_features(x) for x in trainX]
        self.clf.fit(X, trainY)

    def extract_features(self, array):
        # Our model requires some kind of numerical input.
        # It can't handle the sentence as-is, so we need to quantify our them
        # somehow.
        # We've made an array below to help you consider meaningful
        # components of a sentence, for this task.
        # Make sure to use them!
        id, word_m3, word_m2, word_m1, period, word_p1, word_p2, word_3, left_reliable, right_reliable, num_spaces = array

        # context = ' '.join([word_m3, word_m2, word_m1, word_p1, word_p2])
        # context_pos = self.get_sent_pos(context)

        # pos_m1 = self.get_word_pos(word_m1)
        # pos_m2 = self.get_word_pos(word_m2)
        # pos_m3 = self.get_word_pos(word_m3)
        # pos_p1 = self.get_word_pos(word_p1)
        # pos_p2 = self.get_word_pos(word_p2)

        ct_unlikely = 0
        if word_m1 in self.unlikely_proper_nouns:
            ct_unlikely += 1
        if word_m2 in self.unlikely_proper_nouns:
            ct_unlikely += 1
        if word_m3 in self.unlikely_proper_nouns:
            ct_unlikely += 1
        if word_p1 in self.unlikely_proper_nouns:
            ct_unlikely += 1
        if word_p2 in self.unlikely_proper_nouns:
            ct_unlikely += 1

        # The "features" array holds a list of
        # values that should act as predictors.
        features = [  # TODO: add features here
            left_reliable,
            right_reliable,
            num_spaces,
            1 if word_m1.lower() in self.abbrevs else 0,
            1 if word_m1.lower() in self.titles else 0,
            1 if word_m1.lower() in self.timeterms else 0,
            1 if word_m1.lower() in self.places else 0,
            word_m1.count('.') + word_m2.count('.') + word_m3.count('.') + word_p1.count('.') + word_p2.count('.'),
            word_m1.count('.'),
            word_m2.count('.'),
            word_m3.count('.'),
            len(word_m1),
            len(word_p1),
            # word_p1.count('.'),
            # word_p2.count('.'),
            1 if '.' in word_p1 else 0,
            1 if '.' in word_p2 else 0,
            # *context_pos,
            # pos_m1,
            # pos_m2,
            # pos_m3,
            # pos_p1,
            # pos_p2,
            ct_unlikely,

            # ==========TODO==========
            # Make a note of the score you'll get with
            # only the features above (it should be around
            # 0.9). Use this as your baseline.
            # Now, experiment with adding your features.
            # What is a sign that period marks the end of a
            # sentence?
            # Hint: Simpler features will get you further than complex ones, at first.
            # We've given you some features you might want to experiment with below.
            # You should be able to quickly get a score above 0.95!

            len(word_m1),
            1 if word_p1.isupper() else 0,
            1 if word_m1.isupper() else 0,
        ]
        # We want to take some component(s) above and "translate" them to a numerical value.
        # For example, our 4th feature has a value of 1 if word_m1 is an abbreviation,
        # and 0 if not.

        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)

    '''
    def get_word_pos(self, word):
        pos_str = nlp(word)[0].pos_
        if pos_str not in self.pos_dict:
            self.pos_dict[pos_str] = self.pos_ct
            self.pos_ct += 1

        return self.pos_dict[pos_str]

    def get_sent_pos(self, context):
        pos_list = []
        sent_pos = nlp(context)
        for idx, word in enumerate(sent_pos):
            pos_str = sent_pos[idx].pos_
            if pos_str not in self.pos_dict:
                self.pos_dict[pos_str] = self.pos_ct
                self.pos_ct += 1

            pos_list.append(self.pos_dict[pos_str])
            print(word, pos_str)

        return pos_list
    '''


def load_wordlist(file):
    with open(file) as fin:
        return set([x.strip() for x in fin.readlines()])


def load_data(file):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split()
            X.append(arr[1:])
            y.append(arr[0])
        return X, y


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
    parser.add_argument('--output')
    parser.add_argument('--errors')
    parser.add_argument('--report', action='store_true')
    return parser.parse_args()


def main():
    args = parseargs()
    trainX, trainY = load_data(args.train)
    testX, testY = load_data(args.test)

    # Feature Scaling
    # sc = StandardScaler()
    # trainX = sc.fit_transform(trainX)
    # testX = sc.transform(testX)

    classifier = EOSClassifier()
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
