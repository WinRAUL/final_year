import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "ProjectDB"
)
myCursor = conn.cursor()


#for using regular expression
import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# Load EDA Pkgs
import pandas as pd
import numpy as np


# ML Pkgs
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.metrics import accuracy_score,hamming_loss,classification_report

# Multi Label Pkgs
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from skmultilearn.problem_transform import LabelPowerset
from skmultilearn.adapt import MLkNN



#for cleaning data
import neattext as nt
import neattext.functions as nfx

### Split Dataset into Train and Text
from sklearn.model_selection import train_test_split
# Feature engineering
from sklearn.feature_extraction.text import TfidfVectorizer


# Load Dataset
# df = pd.read_csv("/book2.csv")
myCursor.execute("select * from dataset")
d = myCursor.fetchall()
conn.close()
df = pd.DataFrame(d)
print(df)

df[0].apply(lambda x:nt.TextFrame(x).noise_scan())
# Explore For Noise
df[0].apply(lambda x:nt.TextExtractor(x).extract_stopwords())
# Explore For Noise
df[0].apply(nfx.remove_stopwords)

corpus = df[0].apply(nfx.remove_stopwords)

#bulinding features
tfidf = TfidfVectorizer()
# Build Features
Xfeatures = tfidf.fit_transform(corpus).toarray()
# Labels
y = df[range(1,10)]

#splitting data 
X_train,X_test,y_train,y_test = train_test_split(Xfeatures,y,test_size=0.3,random_state=42)


def build_model(model,mlb_estimator,xtrain,ytrain,xtest):
    # Create an Instance
    clf = mlb_estimator(model)
    clf.fit(xtrain,ytrain)
    return clf


# def randomForest_Model(classifier, xtrain, ytrain, xtest):
#   classifier.fit(xtrain, ytrain)
#   return classifier

def randomForest_Model(classifier):
  classifier.fit(X_train, y_train)
  return classifier

def accuracy_of_model(classifier_for_prediction, actual_val, xtest):
  predicted_val=classifier_for_prediction.predict(xtest)
  return accuracy_score(actual_val,predicted_val)

def hammingloss_of_model(classifier_for_prediction, actual_val, xtest):
  predicted_val=classifier_for_prediction.predict(xtest)
  return hamming_loss(actual_val, predicted_val)


binary_mulinomial = build_model(MultinomialNB(),BinaryRelevance,X_train,y_train,X_test)
binary_gauss= build_model(GaussianNB(),BinaryRelevance,X_train,y_train,X_test)
clf_chain_model = build_model(MultinomialNB(),ClassifierChain,X_train,y_train,X_test)
clf_labelP_model = build_model(MultinomialNB(),LabelPowerset,X_train,y_train,X_test)

#################################################################################

#################################################################################
from nltk.corpus import wordnet as wn
import re

def makelist(data):
  synonyms = []
  for kk in data:
    for syn in wn.synsets(kk):
        for i in syn.lemmas():
            synonyms.append(i.name())
  
  return synonyms

# make lists for each department
l1=["road", "roads", "path", "potholes", "highway"]
l1=list(set(l1+makelist(l1)))


l2=["water", "potable", "drinkable", "contamination"]
l2=list(set(l2+makelist(l2)))

l3=["utility poles", "electricity", "electric pole", "faulty wires", "energy", "wires", "electric"]
l3=list(set(l3+makelist(l3)))

l4=["sewers", "sewage", "clogging", "clogged sewers"]
l4=list(set(l4+makelist(l4)))

l5=["waste management", "garbage", "dustbins", "dustbin", "waste", "solid waste", "cleaning"]
l5=list(set(l5+makelist(l5)))

l6=["Construction of urban amenities(parks, gardens)", "parks", "gardens"]
l6=list(set(l6+makelist(l6)))

l7=["washrooms", "rest rooms", "toilets"]
l7=list(set(l7+makelist(l7)))

l8=["disposal", "dead", "foul smell", "dead bosy", "dead animals"]
l8=list(set(l8+makelist(l8)))

l9=["pest", "dengu", "mosquitos"]
l9=list(set(l9+makelist(l9)))

############################################################

categories = {"Roads": l1,
              "Sewers": l4,
              "Electricity": l3,
              "Water": l2,
              "waste": l5,
              "construction": l6,
              "Bathrooms": l7,
              "disposal": l8,
              "pest": l9
              }

def classify_complaint(complaint):
    arr=[]
    flag=False
    for category, keywords in categories.items():
        for keyword in keywords:
            if re.search(keyword, complaint, re.IGNORECASE):
                if flag==False:
                  arr.append(1)
                  flag=True
        if flag==False:
          arr.append(0)
        else:
          flag=False
    return arr