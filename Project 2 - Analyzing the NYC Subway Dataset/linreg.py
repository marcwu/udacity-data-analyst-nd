# This script was used to solve Section 2
# WARNING: running this script takes a lot of time!

import numpy as np
import pandas
import statsmodels.api as sm

def compute_r_squared(data, predictions):
    '''
    Given a list of original data points, and also a list of predicted data points,
    this function returns the coefficient of determination (R^2) for this data.
    '''
    r_squared = 1 - (sum((data - predictions)**2)) / (sum((data - np.mean(data))**2))
    
    return r_squared


def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    Return a tuple consisting of the the intercept and weights of the calcultated model    
    """
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    
    intercept = results.params[0]
    params = results.params[1:]
    
    return intercept, params


def predictions(dataframe, feature_list):
    '''
    Given a dataframe and list of features, build a linear regression model
    and return its predicted values
    '''
    dummy_vars = ['UNIT', 'conds']
    features = dataframe[[f for f in feature_list if f not in dummy_vars]]
    if 'UNIT' in feature_list:
        features = features.join(pandas.get_dummies(dataframe['UNIT'], prefix='unit'))
    if 'Hour' in feature_list:
        features = features.join(pandas.get_dummies(dataframe['Hour'], prefix='Hour'))

    values = dataframe['ENTRIESn_hourly']
    intercept, params = linear_regression(features, values)
    predictions = intercept + np.dot(features, params)

    return predictions




df = pandas.read_csv("turnstile_data_master_with_weather.csv")
y = df['ENTRIESn_hourly']

features = ['UNIT', 'Hour', 'meandewpti', 'meanpressurei', 'fog', 'rain', 'meanwindspdi', 'meantempi', 'precipi']

best_features = [] # we construct our feature list by adding one feature at a time (the one increasing R2 the most)
for i in range(len(features)):
    r2_list = []
    for feat in features: # compute R2 for all features which have not been already selected
        if feat not in best_features:
            pred = predictions(df, best_features + [feat])
            r_2 = compute_r_squared(y, pred)
            r2_list.append((feat, r_2))

    # sort the features from best to worst according to their R2 values
    # and add the best to the feature set
    r2_list_sorted = sorted(r2_list, key=lambda tup: tup[1], reverse=True)
    for t in r2_list_sorted:
        print(t[0] + " " + str(t[1]))
    best_feat = r2_list_sorted[0][0]
    print("Best feature in iteration " + str(i) + ": " + best_feat + ", R2: " + str(r2_list_sorted[0][1]))
    best_features.append(best_feat)

print("best features are: " + str(best_features))
