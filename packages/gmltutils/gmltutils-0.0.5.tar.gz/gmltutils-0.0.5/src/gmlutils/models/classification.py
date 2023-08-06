import numpy as np
import pandas as pd
#MODELS
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
#PREPROCESSING
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
#OPTIMIZERS
from sklearn.model_selection import GridSearchCV
from .bayes import ModelOptimizer
#INFO
from .models_info import rf_default_params, xgb_default_params, lr_default_params, mlp_default_params, knn_default_params, dt_default_params
#import compute_sample_weight
from sklearn.utils.class_weight import compute_sample_weight



#---------------------------------------------------------------------------

def automatic_preprocessor(X_train,ordinal_cat_cols):
    """
    This function performs a preprocessor for the data. It automatically detects the categorical and numeric variables and performs the following steps:
        - Numeric variables: imputation by scaling. STANDARD SCALER
        - Categorical variables: imputation by encoding. ONE HOT ENCODER
        - Ordinal categorical variables: imputation by encoding. ORDINAL ENCODER

    Parameters
    ----------
    X_train : pandas dataframe
        Training data.
    ordinal_cat_cols : list, optional
        List of categorical variables that are ordinal.

    Returns
    -------
    preprocessor : sklearn preprocessor
        Preprocessor for the data. Used fo the pipelines for every model.

    """
    num_cols = X_train.select_dtypes(include=np.number).columns.values.tolist()
    cat_cols = X_train.select_dtypes(include=['category']).columns.values.tolist()

    if ordinal_cat_cols is None:
        cat_cols_onehot = cat_cols
        ordinal_cat_cols = []
    else:
        for col in ordinal_cat_cols:
            cat_cols.remove(col)
        cat_cols_onehot = cat_cols

    # Prepare the categorical variables by encoding the categories    
    categorical_transformer_onehot = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))])
    categorical_transformer_ordinal = Pipeline(steps=[('ordinal', OrdinalEncoder())])
    # Prepare the numeric variables by imputing by scaling
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat_onehot', categorical_transformer_onehot, cat_cols_onehot),
        ('cat_ordinal', categorical_transformer_ordinal, ordinal_cat_cols)])
    return preprocessor


def train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None):

    if bayes_pbounds is None :
        print("Grid search is running")
    #apply the grid search
        model_ = GridSearchCV(
            estimator = pipe, 
            param_grid = grid_params, 
            cv = 10, 
            n_jobs = n_jobs, 
            scoring = scoring
        )
        if sample_weight is not None :
            if sample_weight=='balanced' :
                sample_weights = compute_sample_weight(
                class_weight='balanced',
                y=y_train)
            else:
                sample_weights=sample_weight

            model_.fit(X_train, y_train, XGB__sample_weight=sample_weights)
        else :
            model_.fit(X_train, y_train)

    else:
        print("Bayesian search is running")
        optimizer = ModelOptimizer(scoring=scoring)
        params_bayes = optimizer.optimize_model(pbounds=bayes_pbounds, X_train_scale=X_train, 
                                    y_train=y_train, model=pipe, 
                                    int_params=bayes_int_params,n_iter=bayes_n_iter)
        hyper_params = { (k):(int(np.round(v, 0)) if k in bayes_int_params else round(v, 2)) for k, v in params_bayes.items()}
        model_ = pipe.set_params(**hyper_params)
        if sample_weight is not None :
            if sample_weight=='balanced' :
                sample_weights = compute_sample_weight(
                class_weight='balanced',
                y=y_train)
            else:
                sample_weights=sample_weight

            model_.fit(X_train, y_train, XGB__sample_weight=sample_weights)
        else:
            model_.fit(X_train, y_train)
    return model_


class Classification:

    def __init__(self):
        pass

    def RandomForest_Classifier(self, X_train, y_train, ordinal_cat_cols=None,
                                scoring='accuracy', class_weight=None,
                                grid_params={'RFC__n_estimators': [100, 200],
                                            'RFC__max_depth': [None, 10, 20],
                                            'RFC__min_samples_split': [2, 5],
                                            'RFC__max_features': ['sqrt', None]},
                                bayes_pbounds=None,
                                bayes_int_params=None, 
                                bayes_n_iter=30,
                                criterion='gini',
                                random_state=None,
                                n_jobs=-1):
        """
        This function performs a Random Forest classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        balanced : str, optional
            If 'balanced', class weights are balanced. The default is None.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. The default is {'RFC__n_estimators': [100, 200], 'RFC__max_depth': [None, 10, 20],
                                                    'RFC__min_samples_split': [2, 5], 'RFC__max_features': ['sqrt', None]}.             
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        criterion : str, optional
            Criterion for splitting. The default is 'gini'.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach
        """
        print(" INFO: Agurments params must start as 'RFC__param'" + '\n' "INFO: Default params for Random Forest are: ", rf_default_params)

        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #RFC should be in every key of grid_param_grid
        assert all('RFC__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'RFC__'"
        if bayes_pbounds is not None:
            assert all('RFC__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'RFC__'"
            assert all('RFC__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'RFC__'"
        # Inputs of the model. Change accordingly to perform variable selection
    
        preprocessor = automatic_preprocessor(X_train, ordinal_cat_cols)
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('RFC', RandomForestClassifier(
                criterion = criterion,
                bootstrap = True,
                n_jobs = n_jobs,
                random_state = random_state,
                class_weight = class_weight))])

        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None)

        return model_
    
    def XGBoost_Classifier( self, X_train, y_train, ordinal_cat_cols=None,
                            scoring='accuracy', eval_metric='merror',
                            objective='multi:softmax', grid_params={},
                            bayes_pbounds=None, bayes_int_params=None, 
                            bayes_n_iter=30, random_state=None,
                            sample_weight=None, n_jobs=-1):  
        """
        This method performs a XGBoost classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        eval_metric : str, optional
            Evaluation metric. The default is 'merror'.
        
        objective : str, optional
            Objective function. The default is 'multi:softmax'.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. 
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.

        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        sample_weight : str, optional
            If 'balanced', class weights are balanced. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach or bayesian optimization

        """
        print(" INFO: Agurments params must start as 'XGB__param'" + '\n' "INFO: Default params for XGBoost  are: ", xgb_default_params)
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert sample_weight is None or sample_weight is 'balanced' or isinstance(sample_weight, compute_sample_weight) , "In case of balanced class weights, balanced must be 'balanced'"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #XGB should be in every key of grid_param_grid
        assert all('XGB__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'XGB__'"
        if bayes_pbounds is not None:
            assert all('XGB__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'XGB__'"
            assert all('XGB__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'XGB__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)

        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('XGB', XGBClassifier(
                                random_state=random_state,
                                n_jobs=n_jobs, 
                                verbosity=0,
                                eval_metric=eval_metric,
                                objective=objective))])
                                
        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=sample_weight)
        return model_
    
    def LogisticRegression_Classifier(self, X_train, y_train,  
                                      ordinal_cat_cols=None, scoring='accuracy',
                                    grid_params = {'LR__C': [0.1, 1, 10],
                                    'LR__penalty': ['l1', 'l2', 'elasticnet'],
                                    'LR__multi_class': ['ovr', 'multinomial'],   
                                    'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
                                    bayes_pbounds=None, bayes_int_params=None, 
                                    bayes_n_iter=30, random_state=None, class_weight=None, 
                                    n_jobs=-1 , tol=0.0001, max_iter=1000):
        """
        This method performs a Logistic Regression classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is 
            {'LR__C': [0.1, 1, 10], 'LR__penalty': ['l1', 'l2', 'elasticnet'],
            'LR__multi_class': ['ovr', 'multinomial'], 'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}.

        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        class_weight : str, optional
            If 'balanced', class weights will balanced. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 0.0001.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 1000.
        
        Returns
        -------
        model_ : trained model
            Trained model with grid seach or bayesian optimization

        """

        print(" INFO: Agurments params must start as 'LR__param'" + '\n' "INFO: Default params for Logistic Regression are: ", lr_default_params)
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #XGB should be in every key of grid_param_grid
        assert all('LR__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'LR__'"
        if bayes_pbounds is not None:
            assert all('LR__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'LR__'"
            assert all('LR__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LR__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)

        # param_grid = {'LR__C': [0.1, 1, 10], 'LR__penalty': ['l1', 'l2', 'elasticnet'], 'LR__multi_class': ['ovr', 'multinomial'], 'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}

        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('LR', LogisticRegression(
                                    max_iter=max_iter,
                                    tol=tol, #default 1e-4
                                    class_weight=class_weight, #is used to handle the imbalance dataset
                                    random_state=random_state,
                                    n_jobs=n_jobs, 
                                    verbose=0,
                                    warm_start=False,
                                    fit_intercept=True,
                                    intercept_scaling=1,
                                    dual=False))])

        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None)
        
        return model_
    
    def MLP_Classifier(self,X_train,y_train,ordinal_cat_cols=None, scoring='accuracy',
                       grid_params={'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
                        'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]},
                        bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30, 
                        random_state=None, n_jobs=-1, solver='lbfgs',
                        activation='logistic', tol=1e-4, max_iter=450, early_stopping=False,
                       learning_rate='constant',learning_rate_init=0.001,verbose=True):
        
        """
        This method performs a Multi Layer Perceptron classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
            'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]}.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.
        
        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        solver : str, optional
            The solver for weight optimization. The default is 'lbfgs'.
        
        activation : str, optional
            Activation function for the hidden layer. The default is 'logistic'.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 1e-4.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 450.

        early_stopping : bool, optional
            Whether to use early stopping to terminate training when validation score is not improving. The default is False.

        learning_rate : str, optional
            Learning rate schedule for weight updates. The default is 'constant'.
        
        learning_rate_init : float, optional
            The initial learning rate used. The default is 0.001.
        
        verbose : bool, optional
            Whether to print progress messages to stdout. The default is True.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """


        print(" INFO: Agurments params must start as 'MLP__param'" + '\n' "INFO: Default params for MultiLayer Perceptron are: ", mlp_default_params)
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #XGB should be in every key of grid_param_grid
        assert all('LR__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'MLP__'"
        if bayes_pbounds is not None:
            assert all('LR__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'MLP__'"
            assert all('LR__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'MLP__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor), 
                            ('MLP', MLPClassifier(solver=solver, # Update function
                                                    activation=activation, # Logistic sigmoid activation function
                                                    max_iter=max_iter, # Maximum number of iterations
                                                    tol=tol, # Tolerance for the optimization
                                                    random_state=random_state,
                                                    verbose = verbose,
                                                    early_stopping=early_stopping,
                                                    learning_rate=learning_rate,
                                                    learning_rate_init=learning_rate_init
                                                    ))]) # For replication


        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None)
        return model_
        


    #do the same for knn_classifier
    def KNN_Classifier(self,X_train,y_train,ordinal_cat_cols=None, scoring='accuracy',
                          grid_params={'KNN__n_neighbors': [3,10,25,60]},
                            bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30, 
                            random_state=None, n_jobs=-1):
          
        """
        This method performs a K-Nearest Neighbors classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.

        y_train : pandas dataframe
            Training set labels.

        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.

        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.

        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'KNN__n_neighbors': [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99],
            'KNN__weights': ['uniform','distance'],
            'KNN__algorithm': ['auto','ball_tree','kd_tree','brute'],
            'KNN__leaf_size': [10,20,30,40,50,60,70,80,90,100]}.

        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        p : int, optional
            Power parameter for the Minkowski metric. The default is 2.
        
        metric : str, optional
            The distance metric to use for the tree. The default is 'minkowski'.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """

        print(" INFO: Agurments params must start as 'KNN__param'" + '\n' "INFO: Default params for Random Forest are: ", knn_default_params)
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #XGB should be in every key of grid_param_grid
        assert all('KNN__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'KNN__'"
        if bayes_pbounds is not None:
            assert all('KNN__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'KNN__'"
            assert all('KNN__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'KNN__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('KNN', KNeighborsClassifier(n_jobs=n_jobs, random_state=random_state))])
        
        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None)

        return model_


    

    #do the same for a decision tree
    def Decision_Tree_Classifier(self,X_train,y_train,ordinal_cat_cols=None, scoring='accuracy',
                            grid_params={'DT__max_depth': [3,5,7,10],
                                'DT__min_samples_split': [2,3,4],
                                'DT__min_samples_leaf': [4,5,6],
                                'DT__max_features': ['auto','sqrt','log2',None]},
                                bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30, 
                                random_state=None, n_jobs=-1):
            
            """
            This method performs a Decision Tree classification model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'accuracy'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'DT__param'" + '\n' "INFO: Default params for Decision Tree are: ", dt_default_params)
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #XGB should be in every key of grid_param_grid
            assert all('DT__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'DT__'"
            if bayes_pbounds is not None:
                assert all('DT__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'DT__'"
                assert all('DT__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'DT__'"

            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('DT', DecisionTreeClassifier(random_state=random_state))])
            
            model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None)

            return model_
                                
    


        


    

    
