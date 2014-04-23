import csv
import itertools
class featureSelection:
    def seqFwdSearch(self, trainData, trainFeatureList, trainLabel, totalK, creterionFunc):
        featureList = []
        featureNoList = []
        k = 0
        d = len(trainData)
        if totalK > d:
            totalK = d
        
        while True:
            maxJ = creterionFunc(featureList + trainFeatureList[0], trainLabel)
            bestFeatureNo = 0
            featureNo = 0
            for feature in trainFeatureList[1: ]:
                if featureNo in featureNoList:
                    continue
                jValue = creterionFunc(featureList + feature, trainLabel)
                if jValue > maxJ:
                    maxJ = jValue
                    bestFeatureNo = featureNo
                featureNo = featureNo + 1
            featureNoList.append(bestFeatureNo)
            featureList.append(trainFeatureList[bestFeatureNo])
            if len(featureNoList) == totalK:
                break
        return featureNoList
        
    
    def exhSearch(self, trainData, trainFeatureList, trainLabel, totalK, creterionFunc):
        featureList = []
        featureNoList = []
        n = len(trainFeatureList)
        combinationList = self.getCombinations(n, totalK)
        featureNoList = combinationList[0]
        featureList = [trainFeatureList[featureNo] for featureNo in featureNoList]
        maxJ = creterionFunc(featureList, trainLabel)
        for combination in combinationList[1 : ]:
            featureList = [trainFeatureList[featureNo] for featureNo in combination]
            jValue = creterionFunc(featureList, trainLabel)
            if jValue > maxJ:
                featureNoList = combination
                maxJ = jValue    
        return featureNoList
    
    def getCombinations(n, totalK):
        return list(itertools.combinations(range(n), topK))
    
    def loadData(self, fileName):
        data = []
        labels = []
        dataID = []
        featureName = []
        featureDict = []
        with open(fileName, 'r') as file:
            rowNum = 0
            for line in file:
                dataList = line.split()
                if rowNum != 0:
                    dataID.append(dataList[0])
                    data.append([float(x) for x in dataList[1 : len(dataList) - 1]])
                    labels.append(dataList[-1])
                else:
                    featureName = dataList[1 : len(dataList) - 1]
                rowNum = rowNum + 1
        
        featureNo = 0        
        for feature in featureName:
            featureData = []
            for sample in data:
                featureData.append(sample[featureNo])
            featureDict.append(featureData)
            featureNo = featureNo + 1
        print len(featureDict)
        print featureDict[0]
        print featureDict[-1]
        
        return dataID, data, labels, featureName, featureDict
    
    def simple_crit_func(self, feat_sub):
        """ Returns sum of numerical values of an input list. """ 
        return sum(feat_sub)
    
    def seq_forw_select(self, features, max_k, criterion_func, print_steps=False):
        """
        Implementation of a Sequential Forward Selection algorithm.
    
        Keyword Arguments:
            features (list): The feature space as a list of features.
            max_k: Termination criterion; the size of the returned feature subset.
            criterion_func (function): Function that is used to evaluate the
                performance of the feature subset.
            print_steps (bool): Prints the algorithm procedure if True.
    
        Returns the selected feature subset, a list of features of length max_k.

        """
    
        # Initialization
        feat_sub = []
        k = 0
        d = len(features)
        if max_k > d:
            max_k = d
    
        while True:
        
            # Inclusion step
            if print_steps:
                print('\nInclusion from feature space', features)
            crit_func_max = criterion_func(feat_sub + [features[0]])
            best_feat = features[0]
            for x in features[1:]:
                crit_func_eval = criterion_func(feat_sub + [x])
                if crit_func_eval > crit_func_max:
                    crit_func_max = crit_func_eval
                    best_feat = x
            feat_sub.append(best_feat)
            if print_steps:
                print('include: {} -> feature subset: {}'.format(best_feat, feat_sub))
            features.remove(best_feat)
        
            # Termination condition
            k = len(feat_sub)
            if k == max_k:
                break
                
        return feat_sub