# -*- coding: utf-8 -*-
"""Fake News Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kC7CrE3lEYhp2cquhKAApNtWvKWkZCgb

Dataset Features:
1. id: unique ID for a News Article
2. title: the title of a News Article
3. author: author of the News Article
4. text: the text of the article, could be incomplete
5. label: a label that denotes whether the article is fake of real

1 : Fake News

0 : Real News

Import the Libraries
"""

import numpy as np
import pandas as pd
import re # will be used to remove regular expressions in a text
from nltk.corpus import stopwords # corpus is the content of the text, nltk = natural language toolkit
from nltk.stem.porter import PorterStemmer # stemming takes a word and removes prefix and suffix and return root word
from sklearn.feature_extraction.text import TfidfVectorizer # used to convert text data into numerical data 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

"""Downloading the stopwords"""

import nltk
nltk.download('stopwords')

"""Printing the stopwords in English Language"""

print(stopwords.words('english'))

"""Data Preprocessing"""

# Load Dataset into a pandas DataFrame
news_dataset = pd.read_csv('/content/train.csv')

news_dataset.shape

# Print the first 5 Rows of our dataset
news_dataset.head()

# Counting the Number of Missing values in the dataset
news_dataset.isnull().sum()

# Replacing the missing values with empty strings
news_dataset = news_dataset.fillna('')

# Merging the Author Name and News Title
news_dataset['content'] = news_dataset['author'] + ' ' +news_dataset['title']

print(news_dataset['content'])

"""Stemming 

Stemming is the process of reducing a word to its root word by removing its prefixes and suffixes

example:-
actor, actress, acting -> root word = act
"""

port_stem = PorterStemmer()

def stemming(content):
  # remove all number and punctuations from the content and replace by ' ' blank space
  stemmed_content =  re.sub('[^a-zA-Z]',' ', content)
  # convert everything to lower case
  stemmed_content = stemmed_content.lower()
  # convert everything in the content into a list
  stemmed_content = stemmed_content.split()
  # stemming each word in list if it isn't a stopword
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  # we are joining all the words back into a string from the list
  stemmed_content = ' '.join(stemmed_content)
  # return stemmed string
  return stemmed_content

# apply takes a function and applies it to all values of pandas series.
news_dataset['content'] = news_dataset['content'].apply(stemming)

"""Stemmed content"""

print(news_dataset['content'])

# Seperating the data and label
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(X)

print(Y)
#  1-> fake
#  0-> Real

Y.shape

"""Converting the textual data to Numerical Data"""

# tf = term frequency idf = inverse document frequency
vectorizer = TfidfVectorizer()
vectorizer.fit(X)
X = vectorizer.transform(X)

print(X)

"""Splitting Dataset into training and test data"""

# here stratify=Y is used to distribute the data equally among real and fake ones into both train and the test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

"""Training the Logistic Regression Model"""

model = LogisticRegression()

model.fit(X_train, Y_train)

"""Model Evaluation using Accuracy Score"""

# Accuracy Score for training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
print("Accuracy Score for training data =",training_data_accuracy)

# Accuracy Score for testing data
X_test_prediction = model.predict(X_test)
testing_data_accuracy = accuracy_score(X_test_prediction, Y_test)
print("Accuracy Score for testing data =",testing_data_accuracy)

"""Making a Predictive System for our model"""

X_new = X_test[0]
prediction = model.predict(X_new)
print(prediction)

if(prediction[0] == 0):
  print("The News is Real")
else:
  print("The News is Fake")

print(Y_test[0])