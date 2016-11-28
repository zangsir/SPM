# query by content module
import numpy as np
from saxpyFast import SAX
import sys


# given n, ts_data, ts_query, and dist measure, return the top n ranked similar ts to ts_query in ts_data


def euclid_dist(t1, t2):
    return np.sqrt(sum((t1 - t2) ** 2))


def compute_min_dist(ts1, ts2, word, alpha):
    s = SAX(windowSize=30, wordSize=word, alphabetSize=alpha)
    sax_ts1, pointers1 = s.to_letter_rep(ts1)
    sax_ts2, pointers2 = s.to_letter_rep(ts2)
    mindist = s.min_dist(sax_ts1[0], sax_ts2[0])
    return mindist


def compute_dist(ts1, ts2, dist_measure):
    if dist_measure == "euclidean":
        return euclid_dist(ts1, ts2)
    elif dist_measure == "mindist":
        return compute_min_dist(ts1, ts2, 15, 10)
    else:
        print "distance measure not found: error"
        sys.exit()


def qbc(ts_data, ts_query, dist_measure):
    all_dist = []
    dictx = {}
    labels = []
    for i in range(len(ts_data)):
        ts = ts_data[i][:-1]
        label = ts_data[i][-1]
        dist = compute_dist(ts, ts_query[:-1], dist_measure)
        #print 'dist:',dist
        dictx[i] = ts_data[i]
        all_dist.append(dist)
        labels.append(label)
    alld = np.array(ts_data)
    labelsd = np.array(labels)

    ind_sort = sorted(range(len(all_dist)), key=lambda k: all_dist[k])

    # print 'ind_sort:',ind_sort
    alld_sort = alld[ind_sort]
    labelsd_sort = labelsd[ind_sort]
    return alld_sort, dictx, labelsd_sort, sorted(all_dist)


def get_total_relevant(query_label, all_labels):
    total_relevant = np.sum(np.array(all_labels) == query_label)
    return total_relevant


def prec_recall(query_label, all_labels, N):
    """compute precision, recall, and F score for the top N ranked results. all_labels is ranked labels."""

    retrieved_labels = all_labels[:N]
    total_relevant = np.sum(np.array(all_labels) == query_label)
    # print "total relevant:",total_relevant
    true_positive = np.sum(np.array(retrieved_labels) == query_label)
    precision = float(true_positive) / N
    # print 'true pos:',true_positive
    if total_relevant != 0:
        recall = float(true_positive) / total_relevant
    else:
        recall = 0
    if precision + recall != 0:
        F1 = 2 * precision * recall / (precision + recall)
    else:
        F1 = 0
    return precision, recall, F1

# TODO: MAP and other eval
