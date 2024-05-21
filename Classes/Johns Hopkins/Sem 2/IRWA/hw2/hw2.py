import itertools
import re
from collections import Counter, defaultdict
from typing import Dict, List, NamedTuple

import numpy as np
from numpy.linalg import norm
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize


### File IO and processing

class Document(NamedTuple):
    doc_id: int
    author: List[str]
    title: List[str]
    keyword: List[str]
    abstract: List[str]

    def sections(self):
        return [self.author, self.title, self.keyword, self.abstract]

    def __repr__(self):
        return (f"doc_id: {self.doc_id}\n" +
                f"  author: {self.author}\n" +
                f"  title: {self.title}\n" +
                f"  keyword: {self.keyword}\n" +
                f"  abstract: {self.abstract}")


def read_stopwords(file):
    with open(file) as f:
        return set([x.strip() for x in f.readlines()])


stopwords = read_stopwords('common_words')

stemmer = SnowballStemmer('english')


def read_rels(file):
    """
    Reads the file of related documents and returns a dictionary of query id -> list of related documents
    """
    rels = {}
    with open(file) as f:
        for line in f:
            qid, rel = line.strip().split()
            qid = int(qid)
            rel = int(rel)
            if qid not in rels:
                rels[qid] = []
            rels[qid].append(rel)
    return rels


def read_docs(file):
    """
    Reads the corpus into a list of Documents
    """
    docs = [defaultdict(list)]  # empty 0 index
    category = ''
    with open(file) as f:
        i = 0
        for line in f:
            line = line.strip()
            if line.startswith('.I'):
                i = int(line[3:])
                docs.append(defaultdict(list))
            elif re.match(r'\.\w', line):
                category = line[1]
            elif line != '':
                for word in word_tokenize(line):
                    docs[i][category].append(word.lower())

    return [Document(i + 1, d['A'], d['T'], d['K'], d['W'])
            for i, d in enumerate(docs[1:])]


def stem_doc(doc: Document):
    return Document(doc.doc_id, *[[stemmer.stem(word) for word in sec]
                                  for sec in doc.sections()])


def stem_docs(docs: List[Document]):
    return [stem_doc(doc) for doc in docs]


def remove_stopwords_doc(doc: Document):
    return Document(doc.doc_id, *[[word for word in sec if word not in stopwords]
                                  for sec in doc.sections()])


def remove_stopwords(docs: List[Document]):
    return [remove_stopwords_doc(doc) for doc in docs]


### Term-Document Matrix


class TermWeights(NamedTuple):
    author: float
    title: float
    keyword: float
    abstract: float


def compute_doc_freqs(docs: List[Document]):
    """
    Computes document frequency, i.e. how many documents contain a specific word
    """
    freq = Counter()
    for doc in docs:
        words = set()
        for sec in doc.sections():
            for word in sec:
                words.add(word)
        for word in words:
            freq[word] += 1
    return freq


def compute_tf(doc: Document, doc_freqs: Dict[str, int], weights: TermWeights):
    """
    Computes term frequency, i.e. how many times terms appear in a doc d
    """
    vec = defaultdict(float)
    for word in doc.author:
        vec[word] += weights.author
    for word in doc.keyword:
        vec[word] += weights.keyword
    for word in doc.title:
        vec[word] += weights.title
    for word in doc.abstract:
        vec[word] += weights.abstract
    return dict(vec)  # convert back to a regular dict


def compute_tfidf(doc, doc_freqs, weights):
    term_freq = compute_tf(doc, doc_freqs, weights)
    for term in term_freq.keys():
        tf = term_freq[term]
        # N in numerator as it is constant across all words
        idf = 0 if doc_freqs[term] == 0 else 1 / doc_freqs[term]
        term_freq[term] *= idf
    return term_freq


def compute_boolean(doc, doc_freqs, weights):
    vec = defaultdict(float)
    for word in doc.author:
        vec[word] = 1
    for word in doc.keyword:
        vec[word] = 1
    for word in doc.title:
        vec[word] = 1
    for word in doc.abstract:
        vec[word] = 1
    return dict(vec)  # convert back to a regular dict


### Vector Similarity

def dictdot(x: Dict[str, float], y: Dict[str, float]):
    '''
    Computes the dot product of vectors x and y, represented as sparse dictionaries.
    '''
    keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
    return sum(x.get(key, 0) * y.get(key, 0) for key in keys)


def cosine_sim(x, y):
    '''
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    '''
    num = dictdot(x, y)
    if num == 0:
        return 0
    return num / (norm(list(x.values())) * norm(list(y.values())))


def dice_sim(x, y):
    num = 2 * dictdot(x, y)
    if num == 0:
        return 0
    summation = sum(x.values()) + sum(y.values())
    return num / summation


def jaccard_sim(x, y):
    num = 2 * dictdot(x, y)
    if num == 0:
        return 0
    den = sum(x.values()) + sum(y.values()) - num + 0.000001
    return num / den


def overlap_sim(x, y):
    num = dictdot(x, y)
    if num == 0:
        return 0
    den = min(sum(x.values()), sum(y.values()))
    return num / den


### Precision/Recall

def interpolate(x1, y1, x2, y2, x):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m * x + b


def precision_at(recall: float, results: List[int], relevant: List[int]) -> float:
    """
    This function should compute the precision at the specified recall level.
    If the recall level is in between two points, you should do a linear interpolation
    between the two closest points. For example, if you have 4 results
    (recall 0.25, 0.5, 0.75, and 1.0), and you need to compute recall @ 0.6, then do something like

    interpolate(0.5, prec @ 0.5, 0.75, prec @ 0.75, 0.6)

    Note that there is implicitly a point (recall=0, precision=1).

    `results` is a sorted list of document ids
    `relevant` is a list of relevant documents
    """
    recall_list = []
    precision_list = []
    recall_list.append(0)
    precision_list.append(1)

    count = 0
    num_ret = 0
    for doc in results:
        num_ret += 1
        if doc in relevant:
            count += 1
            precision_list.append(count / num_ret)
            recall_list.append(count / len(relevant))

    if recall in recall_list:
        index = recall_list.index(recall)
        return precision_list[index]
    else:
        recall_upperbound = max([i for i in recall_list if recall > i])
        index_upperbound = recall_list.index(recall_upperbound)
        precision_upperbound = precision_list[index_upperbound]

        recall_lowerbound = min([i for i in recall_list if recall < i])
        index_lowerbound = recall_list.index(recall_lowerbound)
        precision_lowerbound = precision_list[index_lowerbound]

        return interpolate(recall_lowerbound, precision_lowerbound, recall_upperbound, precision_upperbound, recall)


def mean_precision1(results, relevant):
    return (precision_at(0.25, results, relevant) +
            precision_at(0.5, results, relevant) +
            precision_at(0.75, results, relevant)) / 3


def mean_precision2(results, relevant):
    prec_sum = 0
    for i in range(1, 11):
        prec_sum += precision_at(i / 10, results, relevant)
    return prec_sum / 10


def norm_recall(results, relevant):
    num = sum(1 + results.index(relevant[i]) for i in range(len(relevant))) - sum(1 + i for i in range(len(relevant)))
    den = len(relevant) * (len(results) - len(relevant))
    return 1 - (num / den)


def norm_precision(results, relevant):
    num = sum(np.log(1 + results.index(relevant[i])) for i in range(len(relevant))) - sum(
        np.log(1 + i) for i in range(len(relevant)))
    den = (len(results) * np.log((len(results)))) - (
            (len(results) - len(relevant)) * np.log(len(results) - len(relevant))) - (
                  (len(relevant)) * np.log((len(relevant))))
    return 1 - (num / den)


### Extensions

# TODO: put any extensions here


### Search

def experiment():
    docs = read_docs('cacm.raw')
    queries = read_docs('query.raw')
    rels = read_rels('query.rels')
    # docs = read_docs('news.raw')
    # queries = read_docs('news_query.raw')
    # rels = read_rels('news_query.rels')

    stopwords = read_stopwords('common_words')

    term_funcs = {
        'tf': compute_tf,
        'tfidf': compute_tfidf,
        'boolean': compute_boolean
    }

    sim_funcs = {
        'cosine': cosine_sim,
        'jaccard': jaccard_sim,
        'dice': dice_sim,
        'overlap': overlap_sim
    }

    permutations = [
        term_funcs,
        [False, True],  # stem
        [False, True],  # remove stopwords
        sim_funcs,
        [TermWeights(author=1, title=1, keyword=1, abstract=1),
         TermWeights(author=1, title=3, keyword=4, abstract=1),
         TermWeights(author=1, title=1, keyword=1, abstract=4)]
    ]

    print('term', 'stem', 'removestop', 'sim', 'termweights', 'p_0.25', 'p_0.5', 'p_0.75', 'p_1.0', 'p_mean1',
          'p_mean2', 'r_norm', 'p_norm', sep='\t')

    # This loop goes through all permutations. You might want to test with specific permutations first
    for term, stem, removestop, sim, term_weights in itertools.product(*permutations):
        processed_docs, processed_queries = process_docs_and_queries(docs, queries, stem, removestop, stopwords)
        doc_freqs = compute_doc_freqs(processed_docs)
        doc_vectors = [term_funcs[term](doc, doc_freqs, term_weights) for doc in processed_docs]

        metrics = []

        for query in processed_queries:
            query_vec = term_funcs[term](query, doc_freqs, term_weights)
            results = search(doc_vectors, query_vec, sim_funcs[sim])
            # results = search_debug(processed_docs, query, rels[query.doc_id], doc_vectors, query_vec, sim_funcs[sim])
            rel = rels[query.doc_id]

            metrics.append([
                precision_at(0.25, results, rel),
                precision_at(0.5, results, rel),
                precision_at(0.75, results, rel),
                precision_at(1.0, results, rel),
                mean_precision1(results, rel),
                mean_precision2(results, rel),
                norm_recall(results, rel),
                norm_precision(results, rel)
            ])

        averages = [f'{np.mean([metric[i] for metric in metrics]):.4f}'
                    for i in range(len(metrics[0]))]
        print(term, stem, removestop, sim, ','.join(map(str, term_weights)), *averages, sep='\t')

        # return  # TODO: just for testing; remove this when printing the full table


def process_docs_and_queries(docs, queries, stem, removestop, stopwords):
    processed_docs = docs
    processed_queries = queries
    if removestop:
        processed_docs = remove_stopwords(processed_docs)
        processed_queries = remove_stopwords(processed_queries)
    if stem:
        processed_docs = stem_docs(processed_docs)
        processed_queries = stem_docs(processed_queries)
    return processed_docs, processed_queries


def search(doc_vectors, query_vec, sim, with_score=False):
    results_with_score = [(doc_id + 1, sim(query_vec, doc_vec))
                          for doc_id, doc_vec in enumerate(doc_vectors)]
    results_with_score = sorted(results_with_score, key=lambda x: -x[1])
    if with_score:
        results = [(x[0], x[1]) for x in results_with_score]
        return results
    results = [x[0] for x in results_with_score]
    return results


def search_doc(doc_vectors, query_vec, sim):
    results_with_score = [(doc_id + 1, sim(query_vec, doc_vec), doc_vec)
                          for doc_id, doc_vec in enumerate(doc_vectors)]
    results_with_score = sorted(results_with_score, key=lambda x: -x[1])
    results = [(x[0], x[2]) for x in results_with_score]
    return results


def search_debug(docs, query, relevant, doc_vectors, query_vec, sim):
    results_with_score = [(doc_id + 1, sim(query_vec, doc_vec))
                          for doc_id, doc_vec in enumerate(doc_vectors)]
    results_with_score = sorted(results_with_score, key=lambda x: -x[1])
    results = [x[0] for x in results_with_score]

    print('Query:', query)
    print('Relevant docs: ', relevant)
    print()
    for doc_id, score in results_with_score[:10]:
        print('Score:', score)
        print(docs[doc_id - 1])
        print()


def top_20_docs():
    """
    Part 2 Question 1 - List top 20 retrieved docs from queries 6, 9, 22 by their number, title and similarity measure,
    with the relevant docs starred.
    """
    # docs = read_docs('cacm.raw')
    # queries = read_docs('query.raw')
    # relevant = read_rels('query.rels')
    docs = read_docs('news.raw')
    queries = read_docs('news_query.raw')
    relevant = read_rels('news_query.rels')
    # t_queries = []
    # for query in queries:
    #     if query.doc_id in [6, 9, 22]:
    #         t_queries.append(query)
    stopwords = read_stopwords('common_words')
    p_docs, p_queries = process_docs_and_queries(docs, queries, False, True, stopwords)
    doc_freqs = compute_doc_freqs(p_docs)
    term_weights = TermWeights(author=3, title=3, keyword=4, abstract=1)
    doc_vectors = [compute_tfidf(doc, doc_freqs, term_weights) for doc in p_docs]

    print('query_id', 'doc_id', 'title', 'similarity', 'relevant', sep='\t')
    for query in p_queries:
        all_rels = defaultdict(str)
        doc_title = defaultdict(list)
        doc_similarity = defaultdict(float)
        query_vec = compute_tfidf(query, doc_freqs, term_weights)
        results = search(doc_vectors, query_vec, cosine_sim, with_score=True)[:20]
        for result in results:
            doc_similarity[result[0]] = result[1]
        ret_doc = [result[0] for result in results]
        for doc in docs:
            if doc.doc_id in ret_doc:
                doc_title[doc.doc_id] = ' '.join(doc.title)
        rels = relevant[query.doc_id]
        for ret in ret_doc:
            all_rels[ret] = "True" if ret in rels else "False"
        for doc, rel in list(all_rels.items()):
            print(query.doc_id, doc, doc_similarity[doc], doc_title[doc], rel)


def top_10_docs():
    """
    Part 2 Question 2 - For the top 10 retrieved documents, show the terms on which the retrieval was based (those with
    non-zero weights for both query and retrieved document) along with these weights.
    """
    # docs = read_docs('cacm.raw')  # cacm.raw
    # queries = read_docs('query.raw')  # query.raw
    docs = read_docs('news.raw')
    queries = read_docs('news_query.raw')
    stopwords = read_stopwords('common_words')
    p_docs, p_queries = process_docs_and_queries(docs, queries, False, True, stopwords)
    doc_freqs = compute_doc_freqs(p_docs)
    term_weights = TermWeights(author=3, title=3, keyword=4, abstract=1)
    doc_vectors = [compute_tfidf(doc, doc_freqs, term_weights) for doc in p_docs]
    res_doc = {}
    res_query = {}

    for query in p_queries:
        query_vec = compute_tfidf(query, doc_freqs, term_weights)
        results = search_doc(doc_vectors, query_vec, cosine_sim)[:10]
        res_query[query.doc_id] = query_vec
        res_doc[query.doc_id] = []
        for doc_id, doc_vec in results:
            res_doc[query.doc_id].append([doc_id, doc_vec])

    print('query_id', 'doc_id', 'terms', 'doc_weight', 'query_weight', sep='\t')

    for query_id in res_query.keys():
        for doc_terms in res_doc[query_id]:
            for terms in doc_terms[1].keys():
                if doc_terms[1][terms] > 0 and res_query[query_id].get(terms, 0) > 0:
                    print(query_id, doc_terms[0], terms, doc_terms[1][terms], res_query[query_id].get(terms), sep='\t')


def most_similar():
    """
    Part 2 Question 3 - List the top 20 documents that are most similar to Documents 239, 1236 and 2740, giving number,
    title and similarity measure.
    """
    # docs = read_docs('cacm.raw')
    docs = read_docs('news.raw')
    t_queries = []
    for doc in docs:
        if doc.doc_id in [239, 1236, 2740]:
            t_queries.append(doc)
    stopwords = read_stopwords('common_words')
    p_docs, p_queries = process_docs_and_queries(docs, t_queries, False, True, stopwords)
    doc_freqs = compute_doc_freqs(p_docs)
    term_weights = TermWeights(author=3, title=3, keyword=4, abstract=1)
    doc_vectors = [compute_tfidf(doc, doc_freqs, term_weights) for doc in p_docs]

    print('query_id', 'doc_id', 'title', 'similarity', 'relevant', sep='\t')
    for query in p_queries:
        doc_title = defaultdict(list)
        doc_similarity = defaultdict(float)
        query_vec = compute_tfidf(query, doc_freqs, term_weights)
        results = search(doc_vectors, query_vec, cosine_sim, with_score=True)[1:21]
        for result in results:
            doc_similarity[result[0]] = result[1]
        ret_doc = [result[0] for result in results]
        for doc in docs:
            if doc.doc_id in ret_doc:
                doc_title[doc.doc_id] = ' '.join(doc.title)
        for doc, sim in list(doc_similarity.items()):
            print(query.doc_id, doc, sim, doc_title[doc])


def top_20_docs_from_input():
    more_queries = True
    queries = []
    doc_id_ct = 1
    while more_queries:
        query = input("Enter the query you would like to look up: ")
        queries.append(Document(doc_id=doc_id_ct, author=[], title=[], abstract=word_tokenize(query), keyword=[]))
        doc_id_ct += 1
        continue_next = input("Would you like to enter more queries? Y/N: ")
        if continue_next in ['N', 'n', 'No', 'no', 'NO']:
            more_queries = False
        elif continue_next in ['Y', 'y', 'Yes', 'YES', 'yes']:
            more_queries = True
        else:
            print("Invalid input. Please try again.")

    # docs = read_docs('cacm.raw')
    # relevant = read_rels('query.rels')
    docs = read_docs('news.raw')
    relevant = read_rels('news_query.rels')
    stopwords = read_stopwords('common_words')
    p_docs, p_queries = process_docs_and_queries(docs, queries, True, True, stopwords)
    doc_freqs = compute_doc_freqs(p_docs)
    term_weights = TermWeights(author=3, title=3, keyword=4, abstract=1)
    doc_vectors = [compute_tfidf(doc, doc_freqs, term_weights) for doc in p_docs]

    all_result = []
    all_rels = defaultdict(str)
    for query in p_queries:
        query_vec = compute_tfidf(query, doc_freqs, term_weights)
        results = search(doc_vectors, query_vec, cosine_sim)[:20]
        rels = relevant[query.doc_id]
        for res in results:
            all_rels[res] = "True" if res in rels else "False"
        all_result.append(results)
    list_result = []
    for res in all_result:
        r_result = []
        for doc in docs:
            if doc.doc_id in res:
                r_result.append(doc)
        list_result.append(r_result)
    print('query_id', 'doc_id', 'title', 'similarity', 'relevant', sep='\t')
    count = 1
    for res in list_result:
        for ind_res in res:
            print(count, ind_res.doc_id, ' '.join(ind_res.title), 'cosine', all_rels[ind_res.doc_id])
        count += 1


if __name__ == '__main__':
    # experiment()
    # top_20_docs()
    # top_10_docs()
    # most_similar()
    top_20_docs_from_input()
