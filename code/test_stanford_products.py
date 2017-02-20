from util import *
from eval_metric import *

def get_recall(dists, test_label_vector, data_label_vector, top_count):
    num_query = dists.shape[0]
    correct_radio = np.zeros((6, num_query))
    sort_matrix = np.argsort(dists)
    for i in xrange(num_query):
        labels_sorted = data_label_vector[sort_matrix[i,:]].flatten()
        labels = labels_sorted[0:top_count]
        correct_count = np.zeros((6, 1))
        for j in xrange(top_count):
            if labels[j] == test_label_vector[i]:
                if (j < 1) :
                    correct_count[0] = correct_count[0] + 1
                if (j < 10) :
                    correct_count[1] = correct_count[1] + 1
                if (j < 100) :
                    correct_count[2] = correct_count[2] + 1
                if (j < 1000) :
                    correct_count[3] = correct_count[3] + 1
        correct_radio[0][i] = (correct_count[0] > 0)
        correct_radio[1][i] = (correct_count[1] > 0)
        correct_radio[2][i] = (correct_count[2] > 0)
        correct_radio[3][i] = (correct_count[3] > 0)
    ave_precision = np.mean(correct_radio, axis = 1)
    print 'stanford online products mean recall@ 1 : %f' % (ave_precision[0])
    print 'stanford online products mean recall@ 10 : %f' % (ave_precision[1])
    print 'stanford online products mean recall@ 100 : %f' % (ave_precision[2])
    print 'stanford online products mean recall@ 1000 : %f' % (ave_precision[3])

def eval(query_lmdb_path, query_label_file, data_lmdb_path, data_label_file, data_cnt, feature_dim, top_cnt):
    pre_mode = 1# 0 : no process 1 : L2 norm 2 : binarize
    query_label_vector = pickle.load(open(query_label_file, 'rb'))
    data_label_vector = pickle.load(open(data_label_file, 'rb'))
    data_feature_vector = load_lmdb(data_lmdb_path, data_cnt, feature_dim, pre_mode)
    # distance computation method
    dists = compute_distances_self(data_feature_vector)
    np.fill_diagonal(dists, float("inf"))
    get_recall(dists, query_label_vector, data_label_vector, top_cnt)


def eval_HDC(query_lmdb_path_1, query_lmdb_path_2, query_lmdb_path_3, query_label_file,
         data_lmdb_path_1, data_lmdb_path_2, data_lmdb_path_3, data_label_file,
         data_cnt, feature_dim, top_cnt):
    pre_mode = 1# 0 : no process 1 : L2 norm 2 : binarize
    query_label_vector = pickle.load(open(query_label_file, 'rb'))
    data_label_vector = pickle.load(open(data_label_file, 'rb'))
    data_feature_vector_1 = load_lmdb(data_lmdb_path_1, data_cnt, feature_dim, pre_mode)
    data_feature_vector_2 = load_lmdb(data_lmdb_path_2, data_cnt, feature_dim, pre_mode)
    data_feature_vector_3 = load_lmdb(data_lmdb_path_3, data_cnt, feature_dim, pre_mode)
    data_feature_vector = np.concatenate((data_feature_vector_1, data_feature_vector_2,
                                          data_feature_vector_3), axis=1)
    dists = compute_distances_self(data_feature_vector)
    np.fill_diagonal(dists, float("inf"))
    get_recall(dists, query_label_vector, data_label_vector, top_cnt)