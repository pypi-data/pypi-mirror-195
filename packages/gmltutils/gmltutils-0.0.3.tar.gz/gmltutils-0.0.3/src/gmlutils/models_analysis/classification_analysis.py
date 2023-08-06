#import metrcis
from sklearn import metrics as mtrs
from scipy.stats import norm, binom_test
from statsmodels.stats import contingency_tables as cont_tab
import matplotlib.pyplot as plt
import numpy as np
from sklearn.inspection import permutation_importance
import pandas as pd


class Canalysis:
    """
    Class to calculate classification metrics analysis.
    """
    def __init__(self,model, X_train, y_train, X_test, y_test):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test


    def confusion_matrix(self, train_or_test, labels, sample_weight=None, normalize:bool=True):
        """
        Calculate confusion matrix and classification metrics.
        For Multiclass uses Macro average, for binary uses binary average.

        Parameters
        ----------
        train_or_test : str, optional
            Whether to calculate metrics on training or test set, by default 'train'
        labels : list
            List of labels. Vector of output categories
        sample_weight : list, optional
            Weights assigned to output samples in training process, by default None.
            ([int, int, ...])
        normalize : bool, optional
            normalize classification metrics when possible, by default True.

        Returns
        -------
        None
            Print confusion matrix and classification metrics
        """
        assert isinstance(train_or_test, str), 'train_or_test must be a string'
        assert train_or_test.lower() in ['train', 'test'], 'train_or_test must be either "train" or "test"'
        # Check if train or test
        if train_or_test.lower() == 'train':
            y_true = self.y_train
            y_pred = self.model.predict(self.X_train)
        elif train_or_test.lower() == 'test':
            y_true = self.y_test
            y_pred = self.model.predict(self.X_test)

        # Calculate confusion matrix
        print('Confusion Matrix and Statistics\n\t   Prediction')
        # if labels is None:
        #     labels = list(y_true.unique())
        cm = mtrs.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight, normalize=None)
        cm_df = pd.DataFrame(cm, columns=labels)
        cm_df = pd.DataFrame(labels, columns=['Reference']).join(cm_df)
        print(cm_df.to_string(index=False))
        # Calculate metrics depending on type of classification, multiclass or binary
        try:   
            if len(y_true.unique()) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'     
        except:
            if len(np.unique(y_true)) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'
                
        # Calculate accuracy
        acc = mtrs.accuracy_score(y_true, y_pred, normalize=normalize, sample_weight=sample_weight)
        # Calculate No Information Rate
        combos = np.array(np.meshgrid(y_pred, y_true)).reshape(2, -1)
        noi = mtrs.accuracy_score(combos[0], combos[1], normalize=normalize, sample_weight=sample_weight)
        # Calculate p-value Acc > NIR
        res = binom_test(cm.diagonal().sum(), cm.sum(), max(pd.DataFrame(cm).apply(sum,axis=1)/cm.sum()),'greater')
        # Calculate P-value mcnemar test
        MCN_pvalue = cont_tab.mcnemar(cm).pvalue
        # Calculate Kappa
        Kappa = mtrs.cohen_kappa_score(y_true, y_pred, labels=labels, sample_weight=sample_weight)
        # Obtain positive label
        pos_label = labels[0]
        # Calculate precision
        precision = mtrs.precision_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate recall 
        recall = mtrs.recall_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate F1 score
        F_score = mtrs.f1_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate balanced accuracy
        Balanced_acc = mtrs.balanced_accuracy_score(y_true, y_pred, sample_weight=sample_weight)
        if average == 'binary': # binary
            # Calculate sensitivity, specificity et al
            TP = cm[1,1]
            TN = cm[0,0]
            FP = cm[0,1]
            FN = cm[1,0]
            sens = TP / (TP + FN)
            spec = TN / (TN + FP)
            Prevalence = (TP + FN) / (TP + TN + FP + FN)
            Detection_rate = TP / (TP + TN + FP + FN)
            Detection_prevalence = (TP + FP) /  (TP + TN + FP + FN)
            
            
            # print all the measures
            out_str = '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Sensitivity: ' + str(round(sens,3)) + '\n' + \
            'Specificity: ' + str(round(spec,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Prevalence: ' + str(round(Prevalence,3)) + '\n' + \
            'Detection Rate: ' + str(round(Detection_rate,3)) + '\n' + \
            'Detection prevalence: ' + str(round(Detection_prevalence,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3)) + '\n' + \
            'Positive label: ' + str(pos_label) 
        else: # multiclass
                    # print all the measures
            out_str = '\n Overall Multiclass Score Using Macro' + '\n'  + \
            '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3))  + '\n' + '\n' + \
            'Individual Class Scores' 
            
            # Calculate metrics for each class
            for i in range(len(labels)):
                labels_index = [i for i in range(len(labels))]
                labels_index.remove(i)
                # Calculate sensitivity, specificity et al
                TP = cm[i,i]
                cm2=np.delete(cm,i,0)
                TN = np.delete(cm2,i,1).sum()
                FP = np.delete(cm[:,i],i).sum()
                FN = np.delete(cm[i],i).sum()
                rec = TP / (TP + FN)
                spec_2 = TN / (TN + FP)
                prec= TP / (TP + FP)
                # print all the measures
                out_str += '\n' + 'Class: ' + str(labels[i]) + '\n' + \
                'Recall: ' + str(round(rec,3)) + '\n' + \
                'Specificity: ' + str(round(spec_2,3)) + '\n' + \
                'Precision: ' + str(round(prec,3)) + '\n' + \
                'F1 Score: ' + str(round((2*prec*rec)/(prec+rec),3)) + '\n' 
        print(out_str)

    #generate a permutation importance plot
    def permutation_importance(self,n_repeats=10,random_state=None,figsize=(12, 4)):
        """
        Generate a permutation importance plot. Is used
        to determine the importance of each feature in the model.

        Parameters
        ----------
        n_repeats : int, optional
            Number of times to permute a feature. The default is 10.

        random_state : int, optional
            Random state for the permutation. The default is None.

        figsize : tuple, optional
            Size of the figure. The default is (12, 4).

        Returns
        -------
        None.
            Plot is generated.
        """
        assert n_repeats > 0, "n_repeats must be greater than 0 for permutation importance"
        assert random_state is None or isinstance(random_state, int), "random_state must be an integer or None"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        importances = permutation_importance(self.model, 
                                    self.X_train, self.y_train,
                                    n_repeats=n_repeats,
                                    random_state=random_state)
        
        fig = plt.figure(2, figsize=figsize) 
        plt.bar(self.X_train.columns, importances.importances_mean, yerr=importances.importances_std,color='black', alpha=0.5)
        plt.xlabel('Feature')
        plt.ylabel('Permutation Importance')
        plt.xticks(rotation=90)
        plt.grid()
        plt.show()
        

    
