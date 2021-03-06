#note:
'''
select all visit containing return items and add two more var to training data: 
(1)number of items returned per visit.
(2)number of distinct finelinenumber returned per visit.
peformance for logistic is the same, for naive bayes, improved accuracy f1 score from 0.43 to 0.45

'''
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
from copy import deepcopy

train= pd.read_csv('H:\\01_self study_flash drive\\AAAschulich\\beyond_schulich\\practice\\weclouddata\\applied_ml\project1\walmart\\train_data.csv')

#dataset col names:
names=list(train.columns.values)


#covert col names to lowercase
new_names=[]
for item in names:
  new_names.append(item.lower())

names=deepcopy(new_names)

train.columns=names

#convert deptdesc to str
train['departmentdescription']=train.departmentdescription.astype(str)


#number of rows for training data: 647,054
len(train.loc[:,'finelinenumber'])

#number of triptype: 38
len(set(train.loc[:,names[0]]))

#number of visitnumber: 95,674
len(set(train.loc[:,names[1]]))

#number of upc code: 101,843
len(set(train.loc[:,names[3]]))

#number of finelinenumber: 9,324
len(set(train.loc[:,names[6]]))

#number of dept:69
len(set(train.loc[:,names[5]]))

#show all col
pd.options.display.max_columns = 100
train.head(5)

#remove return (negative scancount) items and treat them separately
no_return_bool=train.scancount>=0
return_bool=train.scancount<0

train_return=train[return_bool]
train=train[no_return_bool]

#transform dataset into: transaction based data(i.e. one row is one visitnumber)

#type per visit
triptype_agg=train.loc[:,['triptype','visitnumber']]
triptype_agg.drop_duplicates(inplace=True)

#count by upc per visit
upc_agg=train.groupby(['visitnumber']).upc.agg({'upc_count':'nunique'})


#number of items bought per visit
scancount_agg=train.groupby(['visitnumber']).scancount.agg({'item_sum':'sum'})

#number of filelinenumber per visit
finelinenumber_agg=train.groupby(['visitnumber']).finelinenumber.agg({'finelinenumber_count':'nunique'})


#weekday of the visit
weekday_agg=train.loc[:,['weekday','visitnumber']]
weekday_agg.drop_duplicates(inplace=True)


#whether purchased a certain dept per visit
dept_agg=train.groupby(['visitnumber','departmentdescription']).departmentdescription.agg(['count'])
dept_agg2=dept_agg.unstack()


#join features together named t.

t=dept_agg2.merge(finelinenumber_agg,left_on='visitnumber',right_on='visitnumber',how='inner')
t=t.merge(upc_agg,left_on='visitnumber',right_on='visitnumber',how='inner')
t=t.merge(scancount_agg,left_on='visitnumber',right_on='visitnumber',how='inner')
t=t.merge(weekday_agg, left_on='visitnumber', right_on='visitnumber',how='inner')
t=t.merge(triptype_agg,left_on='visitnumber', right_on='visitnumber',how='inner')

#check structure:
t.loc[0:15,]



#modify col names:

col_names=[]
for item in t.columns:
  if item[0]=='count':
    col_names.append(item[1])
  else:
    col_names.append(item[0])

dict={0:'visitnumber',70:'finelinenumber_count',71:'upc_count',72:'item_sum',73:'weekday',74:'triptype'}

for key in dict:
  col_names[key]=dict[key]


t.columns=col_names




#deal with train_return dataset:
#number of items returned
scancount_agg_return=train_return.groupby(['visitnumber']).scancount.agg({'upc_sum_return':'sum'}) *-1
#number of distinct finelinenumber returned
finelinenumber_agg_return=train_return.groupby(['visitnumber']).finelinenumber.agg({'dist_fineline_return':'nunique'})

#merge with train dataset without return:
t=t.merge(scancount_agg_return,left_on='visitnumber', right_on='visitnumber',how='left')
t=t.merge(finelinenumber_agg_return,left_on='visitnumber', right_on='visitnumber',how='left')



#repalce NaN with 0.
t.fillna(0,inplace=True)

#dummy var
categorical_features = ['weekday']
t2= pd.get_dummies(t,columns=categorical_features, drop_first=True)



#target and predictor variable split.
y=t2['triptype']
X=t2.drop('triptype', axis=1, inplace=False)

#training and validation
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0,stratify=y)

#scaling variables
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)


#logistic
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(class_weight='balanced',multi_class='ovr')
lr.fit(X_train,y_train)
#print(lr.coef_)
#print(lr.intercept_)

#logistic predction
from sklearn.metrics import classification_report, accuracy_score

y_pred_logistic= lr.predict(X_test)
print('Testing performance')
print(classification_report(y_test, y_pred_logistic))
accuracy = accuracy_score(y_test, y_pred_logistic)*100
print(f"classification accuracy: {round(accuracy,2)}")



#naive bayes
##since naive bayes not allow negative, have to skip the scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0,stratify=y)

from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB()
nb=mnb.fit(X_train,y_train)

#naive bayes prediction
y_pred_nb=nb.predict(X_test)
classification_report(y_test,y_pred_nb,digits=2)
accuracy = accuracy_score(y_test, y_pred_nb)*100
print(f"classification accuracy: {round(accuracy,2)}")

#decision tree
from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree
#import pydotplus

#scaling variables
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

classifier = DecisionTreeClassifier(max_depth=5)  
classifier.fit(X_train, y_train)  

#decision tree prediction
y_pred_tree=classifier.predict(X_test)
classification_report(y_test,y_pred_tree,digits=2)
accuracy = accuracy_score(y_test, y_pred_tree)*100
print(f"classification accuracy: {round(accuracy,2)}")











#model performance checking (cross entropy):

def cross_entropy_eva(y_real_prob, y_pred_prob):
  sum_value=0
  e=math.exp(1)
  for i in range(0,len(y_real_prob)):
    if y_pred_prob[i]==0:
      temp_prob=0.0001
    else:
      temp_prob=y_pred_prob[i]
    sum_value=sum_value+(  math.log(temp_prob,e)) *-1
  sum_value=sum_value/y_real_prob[0]
  return sum_value
  print(f'cross entropy is {sum_value}')
    
    
#get y_pred_prob list for logistic:

dict_position={}
pred=lr.predict_proba(X_test)
k=0
for item in lr.classes_:
  dict_position[item]=k
  k=k+1

i=-1
pred_prob_list=[]
for row in pred:
  i=i+1
  pred_prob=row[dict_position[  list(y_test)[i]]]
  pred_prob_list.append(pred_prob)
#print(pred_prob_list)

cross_entropy_eva(y_real_prob=list(y_test), y_pred_prob=pred_prob_list)
#logistic cross entropy: 692

#naive bayes cross entropy
pred=mnb.predict_proba(X_test)
#print(mnb.classes_)
i=-1
pred_prob_list=[]
for row in pred:
  i=i+1
  pred_prob=row[dict_position[  list(y_test)[i]]]
  pred_prob_list.append(pred_prob)
cross_entropy_eva(y_real_prob=list(y_test), y_pred_prob=pred_prob_list)
#naive bayes cross entropy: 5,051


#decision tree cross entropy
pred=classifier.predict_proba(X_test)
i=-1
pred_prob_list=[]
for row in pred:
  i=i+1
  pred_prob=row[dict_position[  list(y_test)[i]]]
  pred_prob_list.append(pred_prob)
cross_entropy_eva(y_real_prob=list(y_test), y_pred_prob=pred_prob_list)
#decision tree cross entropy: 983







 