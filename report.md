
# Credit Risk Assessment Project Report

## 1. Problem Understanding

The project aims to predict the risk of loan default. This is a binary classification problem where the target variable is `loan_status`, with 1 indicating a default and 0 indicating that the loan was paid off. It's a typical problem in the field of banking and finance, where predicting the likelihood of a loan default is crucial for decision-making. Machine Learning can help automate this process and potentially increase the accuracy of these predictions.

## 2. Data Preparation/Exploration

The dataset provided includes various personal, loan, and credit history features. The data exploration included checking for missing values, imputing these missing values, and analyzing the distribution of the target variable. Visualizations were also used to understand the distribution of categorical variables and the correlation between different features. For data preparation, the categorical variables were one-hot encoded or label encoded as appropriate.

## 3. Modelling

The data was split into a training set and a test set, with stratification to ensure that the proportion of the classes in the target variable remains consistent in both sets. This is particularly important given that the dataset is imbalanced. A RandomForestClassifier was used to model the data. This is an ensemble learning method that operates by constructing multiple decision trees at training time and outputting the class that is the mode of the classes output by individual trees. It's often a good starting point for classification problems due to its simplicity and performance.

## 4. Evaluation

The model's performance was evaluated using several metrics. The accuracy of the model was calculated, and a classification report was generated to show precision, recall, and F1-score for each class. The confusion matrix was also calculated and visualized. The model performed well, with an accuracy of approximately 93.51%. However, given that the dataset is imbalanced, metrics such as the F1-score may be more informative. The model had a high F1-score for class 0 (paid off), but a lower F1-score for class 1 (default), indicating that the model is better at predicting loans that will be paid off than those that will default.

## 5. Deployment

The trained model and the order of the columns in the data were saved using joblib. This allows the model to be loaded later and used to make predictions on new data. The final part of the code provided is for deploying the model in a Streamlit app. This app will take user inputs for various features, use the trained model to make a prediction, and then display this prediction in a user-friendly way.
