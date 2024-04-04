import pandas as pd
import numpy as np
from connector_api_service import data_prep
from training import train_rfc, train_xgb

def predict_rfc(df_i : pd.DataFrame, df_t : pd.DataFrame):
    df_input = df_i.copy()
    df_training = df_t.copy()

    #get the flowNodeId out of the data
    flowNodeIds = df_input['flowNodeId']
    
    # data preparation using the function from connector_api_service.py
    df_input = data_prep(df_input)
    rfc = train_rfc(df_training)
    df_input = df_input.reindex(sorted(df_input.columns), axis=1)

    # prediction with the classifier from training.py and probability of correct classification for that prediction
    prediction_next = rfc[0].classes_
    probability_next = rfc[0].predict_proba(df_input)
    prediction_incident = rfc[1].predict(df_input)
    probability_incident = rfc[1].predict_proba(df_input)
    prediction_duration = rfc[2].predict(df_input)
    probability_duration = rfc[2].predict_proba(df_input)

    return [flowNodeIds, prediction_next, probability_next, prediction_incident, probability_incident, prediction_duration, probability_duration]

def predict_xgb(df_i : pd.DataFrame, df_t : pd.DataFrame):
    df_input = df_i.copy()
    df_training = df_t.copy()

    #get the flowNodeId out of the data
    flowNodeIds = df_input['flowNodeId']
    
    # data preparation using the function from connector_api_service.py
    df_input = data_prep(df_input)
    bst = train_xgb(df_training)
    df_input = df_input.reindex(sorted(df_input.columns), axis=1)

    next_encoder = bst[3]
    incident_encoder = bst[4]
    duration_encoder = bst[5]

    # prediction with the classifier from training.py and probability of correct classification for that prediction
    # encoding is reversed to get the actual predicted values
    prediction_next = next_encoder.inverse_transform(bst[0].classes_)
    probability_next = bst[0].predict_proba(df_input)
    prediction_incident = np.array(list(map(bool, bst[1].predict(df_input))))
    probability_incident = bst[1].predict_proba(df_input)
    prediction_duration = duration_encoder.inverse_transform(bst[2].predict(df_input))
    probability_duration = bst[2].predict_proba(df_input)

    return [flowNodeIds, prediction_next, probability_next, prediction_incident, probability_incident, prediction_duration, probability_duration]
