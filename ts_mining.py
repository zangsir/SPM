from ts_clust_modules import *
from qbc import *
import matplotlib.pyplot as plt

#after I reimplemented saxpyFast, the main module we are using is qbc, not ts_clust_modules

# read syllable sized pitch files from syl_csv_norm
# ts_path='syl_csv_norm/'


def run_kmeans_euclid(data, num_run=10):
    # data[,-1] is the label
    print 'Euclidean | data size:', len(data)
    ts_data = np.delete(data, -1, axis=1)
    best_accuracy = 0
    for run in range(num_run):
        print "run:", run
        centroids, assignments, costLog = k_means_clust_euclid(ts_data, 4, 30)
        # get labels
        data_np = np.array(data)
        labels = data_np[:, -1, None]
        # print labels
        accuracy = computeAccuracy_cmn(assignments, labels)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_cost = costLog
    print "best accuracy:", best_accuracy
    # print "Objective Functions:",best_cost
    # plt.plot(best_cost,'^-')
    # total_cost_log.append(best_cost)
    # total_accuracy_log.append(best_accuracy)


def run_kmeans_SAX(data, labels, num_run=10):
    # data[,-1] is the label
    print 'SAX | data size:', len(data)
    ts_data = data
    best_accuracy = 0
    for run in range(num_run):
        print "run:", run
        word, alpha, num_iter, num_clust = 15, 10, 30, 4
        centroids, assignments, costLog = k_means_clust_mindist(ts_data, num_clust, num_iter, word, alpha)
        accuracy = computeAccuracy_cmn(assignments, labels)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_cost = costLog
    print "best accuracy:", best_accuracy
    # print "Objective Functions:",best_cost
    # plt.plot(best_cost,'^-')
    # total_cost_log.append(best_cost)
    # total_accuracy_log.append(best_accuracy)


def get_data(file):
    """returns a data object similar to the outcome of np.genfromtxt()"""
    f = open(file, 'r').read().split('\n')
    data_vec = []
    labels = []
    for line in f:
        if line != '':
            l = line.split(',')
            ld = l[:-1]
            lf = [float(i) for i in ld]
            data_vec.append(np.array(lf))
            # print l[-1]
            labels.append(l[-1])
    return np.array(data_vec), labels


def compute_MAP_score(Q, data, dist_measure):
    """Q is the set of queries """
    query_result_log = []
    #print "len Q:",len(Q)
    #print "len data:",len(data)
    for query in Q:
        counter = 0
        query_label = query[-1]
        top_ranked, label_dict, labels_ranked, all_dist = qbc(data, query, dist_measure)
        total_rel = get_total_relevant(query_label, labels_ranked)
        max_N = total_rel
        Ns = range(1, max_N)
        precision_log = []
        for N in Ns:
            #print N
            counter += 1
            prec, rec, f1 = prec_recall(query_label, labels_ranked, N)
            #if counter % 5 == 0:
                #print "RESULTS:", prec, rec, f1
            precision_log.append(prec)
        #print precision_log
        average_precision = np.mean(precision_log)
        query_result_log.append(average_precision)
    #print query_result_log
    MAP = np.mean(query_result_log)
    return MAP


def qbc_explore(data):
    """use some test samples to explore qbc behavior and plot some results"""
    test_size = 100
    data_rand = random.sample(data, test_size)

    data_query = random.choice(data)
    data_query = ts
    query_label = data_query[-1]
    #print query_label,

    top_ranked, label_dict, labels_ranked, all_dist = qbc(data_rand, data_query, "euclidean")
    total_rel = get_total_relevant(query_label, labels_ranked)
    max_N = total_rel
    Ns = range(1, max_N)

    # Ns = [2 * total_rel if total_rel < 10 else total_rel]
    #print total_rel
    # one thought is using number of expected tones for this tone category in the dataset.
    # such as near 25% for tone 1 if tone 1 is indeed 0.25 of the total data set.
    f1_log = []
    for N in Ns:
        prec, rec, f1 = prec_recall(query_label, labels_ranked, N)
        print "RESULTS:", prec, rec, f1
        f1_log.append(f1)
        # try to return top N ranked, where N is the num of instances in the data set that has query label
        # plot F1 scores by N (num_top_ranked), and by distance:
        # plt.plot(Ns,f1_log,'bo-')
        # plt.plot(all_dist[10:max_N],f1_log)
        # plt.show()
        # run_kmeans_SAX(data_orig_rand,labels)


def qbc_test(data,dist_measure,SEED):
    test_size = 200
    query_size = 50
    #set hard seed to get desired result
    SEED=2531
    
    random.seed(SEED)
    data_rand = random.sample(data, test_size)
    Q = random.sample(data, query_size)
    print "SEED used:",SEED
    print compute_MAP_score(Q, data_rand, dist_measure)


def main():
    print "+++++++++++++++++++"
    ##unigram_unsmoothed
    fileName_30 = 'downsample_syl_noneut.csv'
    ##unigram NYC newly preprocessed data
    #fileName_30 = '../csv/unigrams/downsample_syl_noneut_NYC_np.csv'

    #fileName_30 = '../csv/unigrams/downsample_syl_whole_meta_30_NYC_np.csv'
    #fileName_30 = '../csv/unigrams/downsample_syl_whole_meta_30_old_np.csv'


    ##unigram_smoothed w/gaussian(10,5)
    #fileName_30 = '../csv/unigrams/downsample_syl_noneut_10_5.csv'
    ##bigrams and trigrams unsmoothed, NEED TO SET QBC TO 60
    #fileName_30 = '../csv/ngrams_np_style/downsample_syl_2_np.csv'
    ##bigrams and trigrams smoothed, NEED TO SET QBC TO 60
    #fileName_30 = '../csv/ngrams_np_style/downsample_syl_2_smooth_np.csv'
    ##use 30point bigrams (above are all N*30 points), SET QBC TO 30
    #fileName_30 = '../csv/ngrams_np_style/downsample_syl_2_30p_np.csv'

    
    # file_orig='../syl_norm.csv' #for sax
    print "data:",fileName_30
    #note we're reading ts data as it is, so the last col of the file (label) should be able to be cast as numeric. later,it will take the last col as the label. 
    data = np.genfromtxt(fileName_30, delimiter=',')
    # data_orig,labels=get_data(file_orig)
    # data_orig has original dimensions for each time series, and data has only 30 points
    test = True
    dist_measure1 = 'euclidean'
    dist_measure2 = 'mindist'


    if test:
        SEED = random.randint(1,5000)
        print "seed:",SEED
        print dist_measure1
        qbc_test(data,dist_measure1,SEED)
        print '====================='
        import time
        start_time = time.time()


        print dist_measure2
        qbc_test(data,dist_measure2,SEED)
        print("--- %s seconds ---" % (time.time() - start_time))

    else:
        # run_kmeans_euclid(data)
        # run_kmeans_SAX(data_orig,labels)
        print compute_MAP_score(data, data, "mindist")


if __name__ == '__main__':
    main()
    # currently, this SAX module is not working because of the variable
    # length input (original) which is still #used in the distance computation in
    # kmeans_mindist. However, at this point, it is not very meaningful to reimplement
    # this because it is not likely to work well as a evaluation strategy.
    # We should keep the original for the 30 point version and we'll go
    # ahead and implement query by content
    # evaluation for cmn data set.
