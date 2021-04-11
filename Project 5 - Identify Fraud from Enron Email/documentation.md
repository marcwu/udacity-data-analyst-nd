# Intro to Machine Learning Final Project
## Identify Fraud from Enron Email


### Marc Wu
#### Submission Date: November 21, 2016



**1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?**

The Enron scandal is the largest case of corporate fraud in American history, which eventually led to the company's bankruptcy.
In the course of the investigations, Enron's Email Corpus and financial data was made public, revealing internal and confidential information about the company.

Our goal for this project is to create a predictive model from the Enron data set. The model should identify person of interest (POI), i.e. persons which were involved in the fraud. Due to the sheer size of the data set, manual investigation is too cumbersome and too time consuming to perform. With Machine Learning we are able to process tens of thousands of emails efficiently and automatically. Another major advantage is the fact, that Machine Learning helps us to build predictive models without explicitly specifying the model itself.

The data set comprises 21 features: 14 financial features, 6 email features, and a POI label for supervised learning.
The total number of data points is 146. We have a skewed distribution of POI labels:

Label   | Count | Relative Frequency
------- | ----- | ------------------
POI     | 18    | 12.33%
non-POI | 128   | 87.67%

Let's have a look at the number of missing values (indicated by 'NaN') for each feature:

Feature                         | 'NaN' Count  | % of Missing Values
------------------------------- | ------------ | ----------------------------
'loan_advances'                 | 142          | 97.26%
'director_fees'                 | 129          | 88.36%
'restricted_stock_deferred'     | 128          | 87.67%
'deferral_payments'             | 107          | 73.29%
'deferred_income'               | 97           | 66.44%
'long_term_incentive'           | 80           | 54.79%
'bonus'                         | 64           | 43.84%
'to_messages'                   | 60           | 41.10%
'from_messages'                 | 60           | 41.10%
'from_poi_to_this_person'       | 60           | 41.10%
'from_this_person_to_poi'       | 60           | 41.10%
'shared_receipt_with_poi'       | 60           | 41.10%
'other'                         | 53           | 36.30%
'salary'                        | 51           | 34.93%
'expenses'                      | 51           | 34.93%
'exercised_stock_options'       | 44           | 30.14%%
'email_address'                 | 35           | 23.97%
'total_payments'                | 21           | 14.38%
'total_stock_value'             | 20           | 13.70%
'poi'                           | 0            | 0%


I also investigated if there are persons with many missing feature values. The table below lists the ten persons with the highest 'NaN' count.

Person                          | 'NaN' Count
------------------------------- | -----------
'LOCKHART EUGENE E'             | 20
'GRAMM WENDY L'                 | 18
'THE TRAVEL AGENCY IN THE PARK' | 18
'WROBEL BRUCE'                  | 18
'WHALEY DAVID A'                | 18
'SAVAGE FRANK'                  | 17
'GILLIS JOHN'                   | 17
'SCRIMSHAW MATTHEW'             | 17
'WAKEHAM JOHN'                  | 17
'CLINE KENNETH W'               | 17

I decided to remove the person 'LOCKHART EUGENE E' from the data set since all corresponding input feature entries are missing. I was also thinking about removing other persons with a high 'NaN' count, but ultimately refrained from doing so, since our data set is small.

In addition to that, I identified two outliers 'TOTAL' and 'THE TRAVEL AGENCY IN THE PARK' which were removed, because they clearly do not represent actual persons.



**2. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.**

The feature selection process was done via GridSearchCV combined with SelectKBest testing values of k ranging from 3 up to 15.
It turned out that 11 features gave the best performance for the final model:

Feature                         | Score        | p-Value
------------------------------- | ------------ | ----------------------------
'exercised_stock_options'       | 24.82        | 0.000
'total_stock_value'             | 24.18        | 0.000
'bonus'                         | 20.79        | 0.000
'salary'                        | 18.29        | 0.000
'fraction_to_poi'               | 16.41        | 0.000
'deferred_income'               | 11.46        | 0.001
'long_term_incentive'           | 9.92         | 0.002
'restricted_stock'              | 9.21         | 0.003
'total_payments'                | 8.77         | 0.004
'loan_advances'                 | 7.18         | 0.008
'expenses'                      | 6.09         | 0.015

I did not employ feature scaling, because AdaBoost (our algorithm of choice) uses decision trees as base learners.
Tree-based algorithms are not affected by feature scaling, because they partition the data according to proportions of labels.

Two features were engineered:

Feature                   | Definition
------------------------- | -------
'fraction_from_poi'       | % of emails that were sent from POIs to this person.
'fraction_to_poi'         | % of emails sent from this person to POIs.

I assume that there is more email communication between POIs than between a POI and non-POI.
Therefore, a high percentage should indicate that someone is more likely to be a POI.


Different combinations of my engineered features were added to the feature list to measure the effect on the final model.
My baseline feature list consisted of all 14 financial features.

Metric              | Both     | only 'fraction_from_poi' | only 'fraction_to_poi' | None
------------------- | ---------| ------------------------ | ---------------------- | ----
Accuracy            | 0.84080  | 0.82680                  | 0.84080                | 0.83547
Precision           | 0.42701  | 0.27620                  | 0.42701                | 0.30976
Recall              | 0.56750  | 0.18450                  | 0.56750                | 0.19050
F1                  | 0.48733  | 0.22122                  | 0.48733                | 0.23591

The results confirm the findings of SelectKBest.
'fraction_to_poi' increases the model's performance, in contrast to 'fraction_from_poi', which even makes the model perform worse.


**3. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?**

I decided to use AdaBoost, because it had the best out-of-the-box model performance for this particular data set.

My initial assessment included four more classifiers.
All were tested with default parameters and with my initial feature list (comprising all financial features together with my two engineered features).


The performance comparison is shown in this table:

Algorithm           | Precision | Recall  | F1
------------------- | --------- | --------|--------
Naive Bayes         | 0.25385   | 0.42850 | 0.31882
Decision Tree       | 0.26003   | 0.26900 | 0.26444
AdaBoost            | 0.40589   | 0.33750 | 0.36855
Random Forest       | 0.41467   | 0.13000 | 0.19794
Logistic Regression | 0.15565   | 0.17550 | 0.16498


**4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).**

Parameter tuning is the process of selecting the best parameters for the machine learning algorithm resulting in the optimal model.
Poor choice of parameters can lead to long running times, high degrees of bias/variance, and therefore poor predictive performance of the model.

Parameter tuning was done automatically via GridSearchCV.
Three parameters were involved for AdaBoost:

Parameter           | Possible Values      | Optimal Value
------------------- | -------------------- | --------
'n_estimators'      | 3, 5, 10, 50, 100    | 5
'learning_rate'     | 0.1, 0.5, 1.0, 2.0   | 1.0
'algorithm'         | 'SAMME', 'SAMME.R'   | 'SAMME'


I was quite surprised that tuning improved the performance substantially.

Algorithm           | Precision | Recall  | F1
------------------- | --------- | --------|--------
AdaBoost            | 0.40589   | 0.33750 | 0.36855
AdaBoost (tuned)    | 0.44507   | 0.55100 | 0.49240

**5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?**

Proper validation ensures that our generated model has predictive power and generalizes the data set well.
It is done by subsetting the given data into a training set to construct our model and a test set to assess (validate) the performance of the model.

There is an inherent trade-off between both sets.
We want to maximize the size of each data set to get the best learning result and the best validation.

When splitting the data we need to ensure that both training and test sets are representative of the whole population.
Otherwise, skewed sets would result in skewed models and results.
A classic mistake is to split the data set without shuffling it beforehand.
In the case of somehow sorted data (e.g. all POIs first, then followed by non-POIs) this can lead to meaningless results.

I used StratifiedShuffleSplit which creates multiple folds of train/test splits.
The fact that tester.py uses it for the final evaluation of the model is one reason.
In addition to that, the fraction of POI labels is preserved for each fold, which is another advantage, since our class labels are imbalanced.



**6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance.**

Accuracy is not a good metric for this data set, because we have imbalanced class labels (very few POIs).
Therefore, the simplest model which always predicts non-POI would achieve high Accuracy.
For this reason I optimized for Precision and Recall by using the F1 metric which represents the weighted average of both.

The performance for my final model as calculated by tester.py:

Metric              | Value
------------------- | -------
Accuracy            | 0.84853
Precision           | 0.44507
Recall              | 0.55100
F1                  | 0.49240

Precision gives a percentage of how often someone is really a POI when the model predicts that he is a POI.
In other words, 44% of the time when someone is predicted by my final model as POI, he is indeed a POI.
Recall on the other hand is the fraction of POIs in the data set being identified by the model.
Thus, the model catches 55% of all POIs in the data set.


Confusion Matrix      | actual POI | actual non-POI
--------------------- | ---------- | -------------
**predicted POI**     | 1102       | 1374
**predicted non-POI** | 898        | 11626
