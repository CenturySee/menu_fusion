#!/usr/bin/python
#coding=utf8

import sys
import json
import numpy as np

class Metrics():
    def __init__(self):
	pass

    def purity(self, clusters, classes):
        """
        Calculate the purity score for the given cluster assignments and ground truth classes
        
        :param clusters: the cluster assignments array
        :type clusters: numpy.array
        
        :param classes: the ground truth classes
        :type classes: numpy.array
        
        :returns: the purity score
        :rtype: float
        """
    
        A = np.c_[(clusters,classes)]
        n_accurate = 0.
        for j in np.unique(A[:,0]):
            z = A[A[:,0] == j, 1]
            x = np.argmax(np.bincount(z))
            n_accurate += len(z[z == x])
	    #print ('z', z)
	    #print ('x', x)
	    #if z[z!=x]:
		#print ('z != x', z[z!=x])
        return n_accurate / A.shape[0]

    def impure_case(self, clusters, classes, feat_tup_ls):
	'''
        Get the purity case indexes for the given cluster assignments and ground truth classes
        
        :param clusters: the cluster assignments array
        :type clusters: numpy.array or list
        
        :param classes: the ground truth classes
        :type classes: numpy.array or list

        :param feat_tup_ls: the feature ls
	:type feat_tup_ls: list

        :returns: impure cases' index, impure cases feature_ls
        :rtype: dict
	'''
	if isinstance(clusters, list):
	    clusters = np.array(clusters)
	if isinstance(classes, list):
	    classes = np.array(classes)
	A = np.c_[(clusters, classes)]
	wrong_feat_ls, wrong_labels = [], set()
        for j in np.unique(A[:,0]):
            z = A[A[:,0] == j, 1]    # 预测类别j的样本的真实类别列表
	    ind_z = np.where(A[:, 0] == j)    # 预测类别为j的样本的下标
            x = np.argmax(np.bincount(z))    # z中类别最多的类别标号
#	    print 'j', j
#	    print 'x', x
#	    print 'z', z, z[0].shape
#	    print 'ind_z', ind_z, ind_z[0].shape
	    index_arr = np.where(z != x)    # z中类别非最多的类别标号的在z中的下标 即被分错类别的样本的原始下标
#	    print 'index_arr', index_arr
#	    for ind in index_arr[0]:
	    if len(z[z==x]) == z.shape[0]:
		continue
	    wrong_feat_ls_j = []    # 类别j的所有错误样本集合
	    for index in ind_z[0]:
#		index = ind_z[0][ind]    # 在原始数据中的下标
#		print 'index', index
#		print 'cluster, classes', clusters[index], classes[index]
		wrong_labels.add(clusters[index])
		wrong_feat_ls_j.append(feat_tup_ls[index])
	    if wrong_feat_ls_j:
		wrong_feat_ls.append(wrong_feat_ls_j)
	wrong_labels = list(wrong_labels)
#	print wrong_labels
#	print wrong_feat_ls
	res_dic = {'wrong_labels':wrong_labels, 'wrong_features':wrong_feat_ls}
	return res_dic


def test_metrics():
    metrics_obj = Metrics()
    clusters = [1,2,1,4,1,6]
    classes = [1,1,2,1,3,1]
    feat_tup_ls = ['a', 'b', 'c', 'd', 'e']
    wrong_dic = metrics_obj.impure_case(clusters, classes, feat_tup_ls)
    print json.dumps(wrong_dic, ensure_ascii=False).encode('utf8')
    purity = metrics_obj.purity(clusters, classes)
    print ('purity: {}'.format(purity) )
    purity = metrics_obj.purity(classes, clusters)
    print ('purity: {}'.format(purity) )

if __name__ == '__main__':
    test_metrics()
