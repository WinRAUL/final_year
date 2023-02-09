from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from train import binary_gauss,binary_mulinomial,BinaryRelevance,clf_chain_model,clf_labelP_model,randomForest_Model,classify_complaint

# for random forest
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


# from numpy.core.overrides import array_function_from_dispatcher
def classifyComplain(complain):
  str_comp=complain
  tfidf = TfidfVectorizer()
  complain = tfidf.transform([complain])
  ans=[0,0,0,0,0,0,0,0,0]

   
  mod1=binary_mulinomial.predict(complain).A[0]
  mod2=binary_gauss.predict(complain).A[0]
  mod3=clf_chain_model.predict(complain).A[0]
  mod4=clf_labelP_model.predict(complain)
  
  # # Random forest

  rf = RandomForestClassifier(n_estimators=100, random_state=0)
  multi_target_forest = MultiOutputClassifier(rf, n_jobs=-1)
  randomforest_rf=randomForest_Model(multi_target_forest)
  mod5=randomforest_rf.predict(complain)
  # #with no parameters
  
  random_forest=RandomForestClassifier()
  randomforest_rf=randomForest_Model(random_forest) 
  mod6=randomforest_rf.predict(complain)
  
  
  customLab=classify_complaint(str_comp)

  
  for i in range(0,8):
    ans[i]=mod1[i]+mod2[i]+mod3[i]+mod5[0][i]+mod6[0][i]+customLab[i]
  return ans

ex="the roads are really bad"
ans=classifyComplain(ex)
print("ans")