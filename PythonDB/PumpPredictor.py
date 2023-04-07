import pandas as pd
import numpy as np
from joblib.logger import PrintTime
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 
from sklearn import ensemble
import tensorflow as tf
from tensorflow import keras
from keras.utils import normalize
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, matthews_corrcoef
from sklearn.metrics import f1_score, roc_auc_score, roc_curve
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
import seaborn as sns
import pickle
from sklearn.metrics import precision_recall_curve
from imblearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn import model_selection
from scipy.stats import uniform, randint
from sklearn.tree import DecisionTreeClassifier

# Data Preprocessing 
df = pd.read_csv('PythonDB/EntireData.csv', index_col=0)
df = df.drop(columns=['Close_Time', 'Symbol', 'Open_Time'])
X = df.drop(columns='willPump')
feature_names = X.columns.tolist()
print(feature_names)
y = df['willPump']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y) # Stratifying ensures that the percentages of each stay the same. 
X_train = normalize(X_train, axis=1)
X_test = normalize(X_test, axis=1)




# Defining the models that I am choosing
modelsChosen = []
modelsChosen.append(('ANN', MLPClassifier()))
modelsChosen.append(('RF', ensemble.RandomForestClassifier()))
modelsChosen.append(('ADA', AdaBoostClassifier()))
modelsChosen.append(('SVC', SVC(probability = True)))

# Finding the optimal SMOTE strategy.
def findOptimalSMOTE():
    allScores = []
    for name, model in modelsChosen:
        grid = GridSearchCV(Pipeline(
            [('sampling', SMOTE()), ('classifier', model)]), 
            {'sampling__sampling_strategy':  np.linspace(0, 0.5, 10)}, 
            cv=3, 
            scoring='f1')
        grid.fit(X_train, y_train)
        print(f"Best {name} SMOTE sampling strategy: {grid.best_params_['sampling__sampling_strategy']}")
        allScores.append(grid.best_params_['sampling__sampling_strategy'])
    mean = sum(allScores) / len(allScores)
    print('Optimal Smote Sampling Strategy For Aggregate: ' + str(mean))
    return mean #Returning the mean score

# Apply SMOTE to the training data
X_train, y_train = SMOTE(random_state=0, sampling_strategy=0.25).fit_resample(X_train, y_train)

#Post-Smote Balance
print("------------Post-Cleaned balance of Classes ----- ")
print(y_train.value_counts())
print(y_test.value_counts())


# Utilities To Be Used
def statistics(y_test, y_predict):
    # Score, and details
    print("------------Confusion Matrix + Accuracy ----- ")
    print(confusion_matrix(y_test, y_predict)) # Confusion Matrix 
    print("Accuracy = " , accuracy_score(y_test, y_predict))
    print("Recall = " ,recall_score(y_test, y_predict))
    print("Precision = ",precision_score(y_test, y_predict))
    print("F1 Score = ",f1_score(y_test, y_predict))
    print("Matthews Coefficient = ", matthews_corrcoef(y_test, y_predict))


def add_ROC_Thresh_To_Plot(name, y_test, y_prob):
    # ROC Curve
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    plt.style.use('seaborn-whitegrid')
    plt.subplot(2, 2, 1)  # Create a subplot
    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.2f})")
    plt.xlabel("False Positive Rate", fontsize=20)
    plt.ylabel("True Positive Rate", fontsize=20)
    plt.legend(fontsize=18, loc='lower right')

    # Threshold-F1 Curve
    precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
    f1_score = 2 * (precision * recall) / (precision + recall)

    plt.subplot(2, 2, 2)  # Create a subplot
    plt.plot(thresholds, recall[:-1], label=f"Recall Score {name}")
    plt.xlabel("Threshold", fontsize=20)
    plt.ylabel("Precision", fontsize=20)
    plt.legend(fontsize=18, loc='upper right')

    plt.subplot(2, 2, 3)  # Create a subplot
    plt.plot(thresholds, precision[:-1],  label=f"Precision Score {name}")
    plt.xlabel("Threshold", fontsize=20)
    plt.ylabel("Precision", fontsize=20)
    plt.legend(fontsize=18, loc='lower right')

    plt.subplot(2, 2, 4)  # Create a subplot
    plt.plot(thresholds, f1_score[:-1], label=f"F1 Score {name}")
    plt.xlabel("Threshold", fontsize=20)
    plt.ylabel("F1 Score", fontsize=20)
    plt.legend(fontsize=18, loc='upper right')

    plt.tight_layout() 

def print_important_features(model, name, feature_names, n_features=8):
    if name == "RF":
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        print(f"Top {n_features} important features for {name}:")
        for i in range(n_features):
            print(f"{i + 1}. {feature_names[indices[i]]}: {importances[indices[i]]}")
        print("\n")





# Optimal Hyperparameter Search
def optimisedParameterSearch():
    for name, model in modelsChosen:
        param_dist = {}
        if name == 'ADA':
            param_dist = {
                'base_estimator': [DecisionTreeClassifier(max_depth=d) for d in range(1, 6)],  # Base estimator with varying max_depth
                'n_estimators': randint(10, 200),  # Number of weak classifiers
                'learning_rate': uniform(0.01, 2),  # Learning rate
            }
        if name == 'ANN':
            param_dist = { 
                'hidden_layer_sizes': randint(1, 2),
                'activation': ['relu', 'tanh', 'logistic'],
                'alpha': uniform(0.0001, 1),
                'learning_rate': ['constant', 'adaptive'],
            }
        elif name == 'RF':
            param_dist = { 
                'n_estimators': randint(1, 250),
                'max_depth': randint(1, 20),
                'min_samples_split': randint(1, 20),
            }
        elif name == 'SVC':
            param_dist = {
                'C': [0.1, 1, 10, 100],
                'kernel': ['linear', 'rbf', 'poly'],
                'degree': [2, 3, 4],
                'class_weight': [None, 'balanced']
            }
        elif name == 'ADA':
            param_dist = {
                'base_estimator': [DecisionTreeClassifier(max_depth=d) for d in range(1, 6)],  # Base estimator with varying max_depth
                'n_estimators': randint(10, 200),  # Number of weak classifiers
                'learning_rate': uniform(0.01, 2),  # Learning rate
            }
        random_search = RandomizedSearchCV(
            model,
            param_distributions=param_dist,
            n_iter=10,
            cv=5,
            n_jobs=-1,
            verbose=2,
            scoring='f1'
        )
        random_search.fit(X_train, y_train)
        print(random_search.best_params_)
        print(name, model)
param_dist_ANN = {'activation': 'tanh', 'alpha': 0.33671252843202817, 'hidden_layer_sizes': 1, 'learning_rate': 'constant'}
param_dist_RF = {'max_depth': 18, 'min_samples_split': 7, 'n_estimators': 219}
param_dist_SVC = {'kernel': 'poly', 'degree': 3, 'class_weight': 'balanced', 'C': 100}
param_dist_ADA = {'base_estimator': DecisionTreeClassifier(max_depth=4), 'learning_rate': 1.393192327265517, 'n_estimators': 199}








# Recieving Tran And Testset Performance
def optimisedTrainSet():
    # ------------ Model Comparison Within Testing Set
    for name, model in modelsChosen:
        op_model = None
        if name == 'ANN':
            op_model = MLPClassifier(**param_dist_ANN)
        elif name == 'RF':
            op_model = ensemble.RandomForestClassifier(**param_dist_RF)     
        elif name == 'SVC':
            op_model =  SVC(probability = True, **param_dist_SVC)
        elif name == 'ADA':
            op_model =  AdaBoostClassifier(**param_dist_ADA)
        kfold = model_selection.StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        y_pred = model_selection.cross_val_predict(op_model, X_train, y_train, cv=kfold)
        y_prob = model_selection.cross_val_predict(op_model, X_train, y_train, cv=kfold, method='predict_proba')[:, 1]
        print('--------------------------------')
        print(f"Optimised Train Model: {name}")
        statistics(y_train, y_pred)
        add_ROC_Thresh_To_Plot(name, y_train, y_prob)
    plt.show()

def optimisedTestSet():
    # ------------ Model Comparison Within Testing Set
    for name, model in modelsChosen:
        op_model = None
        if name == 'ANN':
            op_model = MLPClassifier(**param_dist_ANN)
        elif name == 'RF':
            op_model = ensemble.RandomForestClassifier(**param_dist_RF)     
        elif name == 'SVC':
            op_model =  SVC(probability = True, **param_dist_SVC)
        elif name == 'ADA':
            op_model =  AdaBoostClassifier(**param_dist_ADA)
        op_model.fit(X_train, y_train)
        y_pred = op_model.predict(X_test)
        y_prob = op_model.predict_proba(X_test)[:, 1]
        print('--------------------------------')
        print(f"Optimised Test Model: {name}")
        statistics(y_test, y_pred)
        add_ROC_Thresh_To_Plot(name, y_test, y_prob)
        if name in ["RF"]:
                print_important_features(op_model, name, feature_names)
    plt.show()
optimisedTrainSet()