import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb        

def train_rfc(df : list):
    #Splitting the data into features and labels
    features = df.drop(['nextFlowNodeId','nodeIncident', 'nodeDuration'], axis=1)
    labels_next = df['nextFlowNodeId']
    labels_incident = df['nodeIncident']
    labels_duration = df['nodeDuration']

    #training the classifiers for the different labels
    #print('Model for Next Flow Node:')
    rfc_next = rf_training(features, labels_next)
    #print('Model for Incident:')
    rfc_incident = rf_training(features, labels_incident)
    #print('Model for Duration:')
    rfc_duration = rf_training(features, labels_duration)
    return rfc_next, rfc_incident, rfc_duration

def train_xgb(df : list):
    #Splitting the data into features and labels
    features = df.drop(['nextFlowNodeId','nodeIncident', 'nodeDuration'], axis=1)
    labels_next = df['nextFlowNodeId']
    labels_incident = df['nodeIncident']
    labels_duration = df['nodeDuration']

    #training the classifiers for the different labels
    #print('Model for Next Flow Node:')
    nxt = xgb_training(features, labels_next)
    #print('Model for Incident:')
    inc = xgb_training(features, labels_incident)
    #print('Model for Duration:')
    dur = xgb_training(features, labels_duration)

    #classifiers that will be returned
    xgb_next = nxt[0]
    xgb_incident = inc[0]
    xgb_duration = dur[0]
    
    #encoders that will be returned
    next_encoder = nxt[1]
    incident_encoder = inc[1]
    duration_encoder = dur[1]

    return xgb_next, xgb_incident, xgb_duration, next_encoder, incident_encoder, duration_encoder

def rf_training(features, labels):
    #Splitting the data into training and test data
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=0)

    #Training the Random Forest Classifier
    rfc = RandomForestClassifier(n_estimators=200, max_depth=100, max_features=None, random_state=0)
    rfc.fit(X_train, y_train)

    # metrics for Random Forest 
    """
    #Predicting the labels for the test data
    y_pred_test = rfc.predict(X_test)
    val_acc = accuracy_score(y_test, y_pred_test)

    #Predicting the labels for the training data
    y_pred_train = rfc.predict(X_train)
    train_acc = accuracy_score(y_train, y_pred_train)
    print('Accuracy Random Forest: train acc: ', train_acc, ' val acc: ', val_acc)

    recall = recall_score(y_test, y_pred_test, average='micro')
    print('Recall Random Forest: ', recall)

    precision = precision_score(y_test, y_pred_test, average='micro')
    print('Precision Random Forest: ', precision)

    f1 = f1_score(y_test, y_pred_test, average='micro')
    print('F1 Score Random Forest: ', f1)
    print('\n')
    """

    return rfc

def xgb_training(features, labels):
    #Splitting the data into training and test data
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=0)

    encoder = None
    #Encoding labels is necessary for XGBoost
    if y_train.dtypes == 'object':
        encoder = LabelEncoder()
        y_train = encoder.fit_transform(y_train)
    elif y_train.dtypes == 'int64':
        encoder = LabelEncoder()
        y_train = encoder.fit_transform(y_train)

    #Training the XGBClassifier
    bst = xgb.XGBClassifier(enable_categorical=True)
    bst.fit(X_train, y_train)

    # metrics for XGBoost
    """
    #Predicting the labels for the test data
    y_pred_test = bst.predict(X_test)
    if encoder != None:
        y_pred_test = encoder.inverse_transform(y_pred_test)
    val_acc = accuracy_score(y_test, y_pred_test)

    #Predicting the labels for the training data
    y_pred_train = bst.predict(X_train)
    train_acc = accuracy_score(y_train, y_pred_train)
    print('accuracy XGBoost: train acc: ', train_acc, ' val acc: ', val_acc)

    recall = recall_score(y_test, y_pred_test, average='micro')
    print('Recall XGBoost: ', recall)

    precision = precision_score(y_test, y_pred_test, average='micro')
    print('Precision XGBoost: ', precision)

    f1 = f1_score(y_test, y_pred_test, average='micro')
    print('F1 Score XGBoost: ', f1)
    print('\n')
    """

    return bst, encoder