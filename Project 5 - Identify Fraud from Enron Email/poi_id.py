#!/usr/bin/python

import sys
import pickle
import pprint
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline



### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = [
                 'poi',
                 ### financial features
                 'salary',
                 'deferral_payments',
                 'total_payments',
                 'loan_advances',
                 'bonus',
                 'restricted_stock_deferred',
                 'deferred_income',
                 'total_stock_value',
                 'expenses',
                 'exercised_stock_options',
                 'other',
                 'long_term_incentive',
                 'restricted_stock',
                 'director_fees',
                 ### email features
                 #'to_messages',
                 #'email_address',
                 #'from_poi_to_this_person',
                 #'from_messages',
                 #'from_this_person_to_poi',
                 #'shared_receipt_with_poi'
                 ### engineered features
                 'fraction_from_poi',
                 'fraction_to_poi'
                ]


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
# for each person and each feature calculate the total number of missing values
# and print it out in descending order
person_nan_counts = { person: 0 for person in data_dict }
feature_nan_counts = { feature: 0 for feature in data_dict['LAY KENNETH L'] }

for person in data_dict:
    for feature in data_dict[person]:
        if data_dict[person][feature] == 'NaN':
            person_nan_counts[person] += 1
            feature_nan_counts[feature] += 1

for dic in [person_nan_counts, feature_nan_counts]:
    print ''
    pprint.pprint( sorted(dic.items(), key=lambda x: x[1], reverse=True) )            




# Remove 3 identified outliers
outliers_to_remove = ['TOTAL', # not a person
                      'THE TRAVEL AGENCY IN THE PARK', # not a person
                      'LOCKHART EUGENE E'] # missing values for all features
for outlier in outliers_to_remove:
    data_dict.pop(outlier)





### Task 3: Create new feature(s)
def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
        In case of poi_messages or all_messages having "NaN" value, return 0.
    """
    fraction = 0.
    if poi_messages != 'NaN' and all_messages != 'Nan':
        fraction = float(poi_messages) / all_messages
    
    return fraction


# add two features as discussed in the lecture (Chapter 11: Feature Selection)
feat_tuple_1 = ('from_poi_to_this_person', 'to_messages', 'fraction_from_poi')
feat_tuple_2 = ('from_this_person_to_poi', 'from_messages', 'fraction_to_poi')
for person in data_dict:
    for poi_msg, all_msg, fraction_msg in [feat_tuple_1, feat_tuple_2]:
        poi_msg = data_dict[person][poi_msg]
        all_msg = data_dict[person][all_msg]
        data_dict[person][fraction_msg] = computeFraction(poi_msg, all_msg)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)






### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

#clf = GaussianNB()
#clf = DecisionTreeClassifier()
#clf = AdaBoostClassifier()
#clf = RandomForestClassifier()
#clf = LogisticRegression()



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

skb = SelectKBest()
ada = AdaBoostClassifier()
pipeline = Pipeline( [('skb', skb), ('clf', ada)])

parameters = {'skb__k': range(3,15),
              'clf__n_estimators': [3, 5, 10, 20, 50],
              'clf__learning_rate': [0.1, 0.5, 1., 2.],
              'clf__algorithm': ['SAMME', 'SAMME.R']}

sss = StratifiedShuffleSplit(n_splits=10, random_state = 42)

grid = GridSearchCV(estimator = pipeline, 
                    param_grid = parameters, 
                    scoring = 'f1', 
                    cv = sss)
grid.fit(features, labels)
print ''
print 'GridSearchCV Results:'
print grid.best_params_ # show parameter values


### SelectKBest: determine selected features and their scores and p-values
# Extract SelectKBest object from our pipeline
skb_optimal = grid.best_estimator_.named_steps['skb']
# Get a list of integer indices of the features selected by SelectKBest
skb_feature_indices = skb_optimal.get_support(indices=True)
# Create a 3-tuple of feature, score, and p-value
# format score and p-value for better readability
skb_results = [ ( features_list[i+1],
                  '{:.2f}'.format(skb_optimal.scores_[i]), 
                  '{:.3f}'.format(skb_optimal.pvalues_[i])
                ) for i in skb_feature_indices]
# sort list in descending order according to feature score value
skb_results = sorted(skb_results, key=lambda x: float(x[1]), reverse=True)

print ''
print 'SelectKBest Results (feature, score, p-value):'
pprint.pprint(skb_results) # show feature scores and p-values


clf = grid.best_estimator_



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
dump_classifier_and_data(clf, my_dataset, features_list)