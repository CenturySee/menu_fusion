#!/usr/bin/python
#encoding=utf8

class SimpleCluster():
    '''
    简单聚类器
    '''
    def __init__(self):
        pass

    def cluster(self, feature_ls):
	'''
	简单聚类器
	input: feature_ls    [[src, id, brand_name, food, norm_food], [...]]
	output: label_ls  [0, 1, 0, 4, 10, ...]
	'''
	label_ls = []
	if not feature_ls:
	    return label_ls
	# 特征聚类
	class_dic = {}
	max_class_ind = 0
	for ii, feat_tup in enumerate(feature_ls):
	     src, _id, brand_name, food, n_food = feat_tup
	     if n_food in class_dic:
		 label_ls.append(class_dic[n_food])
	     else:
		 class_dic[n_food] = max_class_ind
		 label_ls.append(max_class_ind)
		 max_class_ind += 1
	return label_ls


def test_simple_cluster():
    cluster = SimpleCluster()
    feat_ls = [[0, 1,2,3,4], [0, 1,2,3,3], [0, 1,2,3,4], [0, 1,2,3,3]]
    label_ls = cluster.cluster(feat_ls)
    print (label_ls)

if __name__ == '__main__':
    test_simple_cluster()
