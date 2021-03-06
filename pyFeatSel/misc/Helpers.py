import pandas as pd
import numpy as np
from itertools import chain, combinations


def create_k_fold_indices(len_data: int, k: int):
    '''
    custom function to create k fold subsets
    :param len_data: number of observations in data
    :param k: number of folds
    :return: return list of dictionaries which contain train, test and validation loc indices
    '''
    assert type(len_data) == int
    assert type(k) == int
    assert k > 0
    assert len_data > 0
    assert len_data > k

    indices = np.arange(len_data)

    indices_test = np.arange(len_data)
    np.random.shuffle(indices_test)

    test_groups = [indices_test[int(i*min((len_data/k), 0.2*len_data)):min(int((i+1)*min(len_data/k, 0.2*len_data)),
                                                                           len_data-1)] for i in range(k)]

    val_groups = []
    # shift test indices
    if k == 1:
        indices_val = np.arange(len_data)
        indices_val_filtered = np.array([i for i in indices_val if i not in test_groups[0]])
        np.random.shuffle(indices_val_filtered)
        val_groups += [indices_val_filtered[:int(0.2*len_data)]]
    else:
        for j in range(len(test_groups)):
            if j == 0:
                val_groups += [test_groups[len(test_groups)-1]]
            else:
                val_groups += [test_groups[j-1]]

    result = []
    for i in range(k):
        test = test_groups[i].tolist()
        val = val_groups[i].tolist()
        train = [int(i) for i in indices if i not in test + val]
        result += [{"test": test, "train": train, "val": val}]

    return result


def create_all_combinations(val: list):
    '''
    createa all possible combinations from a list of values
    :param ss:
    :return:
    '''
    assert type(val) == list
    assert len(val) > 0

    return chain(*map(lambda x: combinations(val, x), range(0, len(val) + 1)))

def threshold_base(preds: np.ndarray):
    '''
    chooses class based on given threshold
    :param preds: predictions of model
    :return: class 1/0
    '''
    return (preds > 0.5).astype(int)



if __name__=="__main__":
    indices = create_k_fold_indices(10, 2)
    print(indices)