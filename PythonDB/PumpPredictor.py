import pandas as pd
import numpy as np

from joblib.logger import PrintTime
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 
from sklearn import ensemble
from xgboost import XGBClassifier

import tensorflow as tf
from tensorflow import keras
from keras.utils import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score, roc_curve
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
import seaborn as sns
import pickle

#Data cleaning before start
df = pd.read_csv('PythonDB/EntireData.csv', index_col=0)
df = df.drop(columns=['Close_Time', 'Symbol', 'Open_Time'])
XforFeature = df.drop(columns='willPump')
X = df.drop(columns='willPump')
y = df['willPump']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y) # Stratifying ensures that the percentages of each stay the same. 
#Post-Smote Balance
print("------------Post-Cleaned balance of Classes ----- ")
print(y_train.value_counts())
print(y_test.value_counts())

print(X_train)

#Normalising Dataset
X_train = normalize(X_train, axis=1)
X_test = normalize(X_test, axis=1)

def statistics(y_test, y_predict):
    # Score, and details
    print("------------Confusion Matrix + Accuracy ----- ")
    cm1 = confusion_matrix(y_test, y_predict)
    print(confusion_matrix(y_test, y_predict)) # Confusion Matrix 

    def generate_model_report(y_actual, y_predicted):
        print("Accuracy = " , accuracy_score(y_actual, y_predicted))
        print("Recall = " ,recall_score(y_actual, y_predicted))
        print("Precision = " ,precision_score(y_actual, y_predicted))
        print("F1 Score = " ,f1_score(y_actual, y_predicted))
        pass

    plt.figure(figsize=(6,4.5), facecolor='#131722') #Setting Background Colour
    ax = sns.heatmap(cm1, annot=True, cmap='icefire', linecolor='black', linewidths=1, fmt='g', cbar=False)
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ')
    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(["""Won't Pump""",'Will Pump'])
    ax.yaxis.set_ticklabels(["""Didn't Pump""",'Did Pump'])
    plt.show()
    print(generate_model_report(y_test, y_predict))

def NeuralNet():
    model = keras.models.Sequential([
        keras.layers.Dense(600, activation='relu', input_shape=(592,)),
        keras.layers.Dense(600, activation='relu', input_shape=(592,)),
        keras.layers.Dense(600, activation='relu', input_shape=(592,)),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=50, batch_size=128)
    y_predict = model.predict(X_test)
    y_predict = [int(round(x[0])) for x in y_predict]
    statistics(y_test, y_predict)

def RandomForrest():
    rf = ensemble.RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_predict = rf.predict(X_test)
    y_predict = [round(value) for value in y_predict]
    # Finding feature importance. 
    feat_importances = pd.Series(rf.feature_importances_, index=XforFeature.columns).sort_values(ascending=True)
    feat_importances.nlargest(50).plot(kind='barh')
    print(feat_importances)
    statistics(y_test, y_predict)
    return rf

def XGBoost():
    XGB = XGBClassifier()
    XGB.fit(X_train, y_train)
    y_predict = XGB.predict(X_test)
    y_predict = [round(value) for value in y_predict]
    # Finding feature importance. 
    feat_importances = pd.Series(XGB.feature_importances_, index=XforFeature.columns).sort_values(ascending=True)
    feat_importances.nlargest(50).plot(kind='barh')
    print(feat_importances)
    statistics(y_test, y_predict)
    return XGB

def export(model, name):
    pickle.dump(model, open(name + '.sav', 'wb'))

export(XGBoost(), 'XGBoost')
