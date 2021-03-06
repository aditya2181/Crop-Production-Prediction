# -*- coding: utf-8 -*-
"""Crop_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_5yNSBNARPRSM-iucaI6ARSM5gSq1AFz

Importing the libraries.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""Importing the data."""

df = pd.read_csv("crop_production.csv")
df

"""**Data Exploration**"""

df.isnull().sum()

sum_maxp = df["Production"].sum()
df["percent_of_production"] = df["Production"].map(lambda x:(x/sum_maxp)*100)

df[:5]

"""**Data Visualization**"""

sns.lineplot(df["Crop_Year"],df["Production"])

plt.figure(figsize=(25,10))
sns.barplot(df["District_Name"],df["Production"])
plt.xticks(rotation=90)

sns.jointplot(df["Area"],df["Production"],kind='reg')

sns.barplot(df["Season"],df["Production"])

df.groupby("Season",axis=0).agg({"Production":np.sum})

df["Crop"].value_counts()[:5]

top_crop_pro = df.groupby("Crop")["Production"].sum().reset_index().sort_values(by='Production',ascending=False)
top_crop_pro[:5]

"""**Each type of crops required various area & various season.**

**1. Rice**
"""

rice_df = df[df["Crop"]=="Rice"]
print(rice_df.shape)
rice_df[:3]

sns.barplot("Season","Production",data=rice_df)

plt.figure(figsize=(13,10))
sns.barplot("District_Name","Production",data=rice_df)
plt.xticks(rotation=90)
plt.show()

top_rice_pro_dis = rice_df.groupby("District_Name")["Production"].sum().reset_index().sort_values(by='Production',ascending=False)
top_rice_pro_dis[:5]
sum_max = top_rice_pro_dis["Production"].sum()
top_rice_pro_dis["precent_of_pro"] = top_rice_pro_dis["Production"].map(lambda x:(x/sum_max)*100)
top_rice_pro_dis[:5]

plt.figure(figsize=(15,10))
sns.barplot("Crop_Year","Production",data=rice_df)
plt.xticks(rotation=45)
#plt.legend(rice_df['State_Name'].unique())
plt.show()

sns.jointplot("Area","Production",data=rice_df,kind="reg")

"""**Insights:**

From Data Visualization: Rice production is mostly depends on Season, Area, State(place).

**2. Wheat**
"""

wheat_df = df[df["Crop"]=="Wheat"]
print(wheat_df.shape)
wheat_df[:3]

plt.figure(figsize=(13,10))
sns.barplot("District_Name","Production",data=wheat_df)
plt.xticks(rotation=90)
plt.show()

top_wheat_pro_dis = wheat_df.groupby("District_Name")["Production"].sum().reset_index().sort_values(by='Production',ascending=False)
top_wheat_pro_dis[:5]
sum_max = top_wheat_pro_dis["Production"].sum()
top_wheat_pro_dis["precent_of_pro"] = top_wheat_pro_dis["Production"].map(lambda x:(x/sum_max)*100)
top_wheat_pro_dis[:5]

plt.figure(figsize=(15,10))
sns.barplot("Crop_Year","Production",data=wheat_df)
plt.xticks(rotation=45)
#plt.legend(wheat_df['State_Name'].unique())
plt.show()

sns.jointplot("Area","Production",data=wheat_df,kind="reg")

"""**Insights:**

**3. Sugarcane**
"""

sug_df = df[df["Crop"]=="Sugarcane"]
print(sug_df.shape)
sug_df[:3]

plt.figure(figsize=(13,8))
sns.barplot("District_Name","Production",data=sug_df)
plt.xticks(rotation=90)
plt.show()

top_sug_pro_dis = sug_df.groupby("District_Name")["Production"].sum().reset_index().sort_values(by='Production',ascending=False)
top_sug_pro_dis[:5]
sum_max = top_sug_pro_dis["Production"].sum()
top_sug_pro_dis["precent_of_pro"] = top_sug_pro_dis["Production"].map(lambda x:(x/sum_max)*100)
top_sug_pro_dis[:5]

plt.figure(figsize=(15,10))
sns.barplot("Crop_Year","Production",data=sug_df)
plt.xticks(rotation=45)
#plt.legend(rice_df['State_Name'].unique())
plt.show()

sns.jointplot("Area","Production",data=sug_df,kind="reg")

"""**Insighits:**

Sugarecane production is directly proportional to area.

And the production is high in some state only.

**Feature Selection**
"""

data = df.drop(["State_Name","Crop_Year"],axis=1)

data_dum = pd.get_dummies(data)
data_dum[:5]

"""**Test Train Split**"""

x = data_dum.drop("Production",axis=1)
y = data_dum[["Production"]]
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.33, random_state=42)
print("x_train :",x_train.shape)
print("x_test :",x_test.shape)
print("y_train :",y_train.shape)
print("y_test :",y_test.shape)

x_train

x_test

y_train

y_test

"""**Model Creation**"""

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(x_train,y_train)
preds = model.predict(x_test)

from sklearn.metrics import r2_score
r = r2_score(y_test,preds)
print("R2score when we predict using Randomn forest is ",r)

"""**Prediction**"""

tst = df.drop(["State_Name","Crop_Year"],axis=1)
tst_dum = pd.get_dummies(tst)
tst_dum[:5]

y_test = tst_dum.copy()
print(x_train.shape)
print(y_test.shape)

def common_member(x_train,x_test): 
    a_set =  set(x_train.columns.tolist())
    b_set =  set(x_test.columns.tolist())
    if (a_set & b_set): 
        return list(a_set & b_set)

com_fea = common_member(x_train,tst_dum)
len(com_fea)

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(x_train[com_fea],y_train)
preds = model.predict(y_test[com_fea])

preds

df["production"] = preds

df[:10]

df.to_csv('Prediction.csv')

"""**Predicting the best crop.**"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

df=pd.read_csv('Crop_recommendation.csv')
df.head()

df.describe()

"""**Exploratory Data Analysis.**

Heatmap to check null/missing values.
"""

sns.heatmap(df.isnull(),cmap="coolwarm")
plt.show()

"""It is symmetrical and bell shaped, showing that trials will usually give a result near the average, but will occasionally deviate by large amounts. It's also fascinating how these two really resemble each other!"""

plt.figure(figsize=(12,5))
plt.subplot(1, 2, 1)
# sns.distplot(df_setosa['sepal_length'],kde=True,color='green',bins=20,hist_kws={'alpha':0.3})
sns.distplot(df['temperature'],color="purple",bins=15,hist_kws={'alpha':0.2})
plt.subplot(1, 2, 2)
sns.distplot(df['ph'],color="green",bins=15,hist_kws={'alpha':0.2})

"""A quick check if the dataset is balanced or not. If found imbalanced, we would have to downsample some targets which are more in quantity but so far everything looks good!"""

sns.countplot(y='label',data=df, palette="plasma_r")

"""A very important plot to visualize the diagonal distribution between two features for all the combinations!"""

sns.pairplot(df, hue = 'label')

"""During rainy season, average rainfall is high (average 120 mm) and temperature is mildly chill (less than 30'C).

Rain affects soil moisture which affects ph of the soil. Here are the crops which are likely to be planted during this season.

**1. Rice needs heavy rainfall (>200 mm) and a humidity above 80%. No wonder major rice production in India comes from East Coasts which has average of 220 mm rainfall every year!**

**2. Coconut is a tropical crop and needs high humidity therefore explaining massive exports from coastal areas around the country.**
"""

sns.jointplot(x="rainfall",y="humidity",data=df[(df['temperature']<30) & (df['rainfall']>120)],hue="label")

"""This graph correlates with average potassium (K) and average nitrogen (N) value (both>50).

These soil ingredients direcly affects nutrition value of the food. Fruits which have high nutrients typically has consistent potassium values
"""

sns.jointplot(x="K",y="N",data=df[(df['N']>40)&(df['K']>40)],hue="label")

"""Let's try to plot a specfic case of pairplot between `humidity` and `K` (potassium levels in the soil.)

sns.jointplot() can be used for bivariate analysis to plot between humidity and K levels based on Label type. It further generates frequency distribution of classes with respect to features.
"""

sns.jointplot(x="K",y="humidity",data=df,hue='label',size=8,s=30,alpha=0.7)

"""We can see ph values are critical when it comes to soil. A stability between 6 and 7 is preffered."""

sns.boxplot(y='label',x='ph',data=df)

"""Another interesting analysis where Phosphorous levels are quite differentiable when it rains heavily (above 150 mm)."""

sns.boxplot(y='label',x='P',data=df[df['rainfall']>150])

"""Further analyzing phosphorous levels.

When humidity is less than 65, almost same phosphor levels(approx 14 to 25) are required for 6 crops which could be grown just based on the amount of rain expected over the next few weeks.
"""

sns.lineplot(data = df[(df['humidity']<65)], x = "K", y = "rainfall",hue="label")

"""**DATA PRE-PROCESSING**"""

c=df.label.astype('category')
targets = dict(enumerate(c.cat.categories))
df['target']=c.cat.codes

y=df.target
X=df[['N','P','K','temperature','humidity','ph','rainfall']]

"""Correlation visualization between features. We can see how Phosphorous levels and Potassium levels are highly correlated."""

sns.heatmap(X.corr())

"""**FEATURE SCALING**

Feature scaling is required before creating training data and feeding it to the model.

As we saw earlier, two of our features (temperature and ph) are gaussian distributed, therefore scaling them between 0 and 1 with MinMaxScaler.
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)

# we must apply the scaling to the test set as well that we are computing for the training set
X_test_scaled = scaler.transform(X_test)

"""**MODEL SELECTION**

KNN Classifier for Crop prediction.
"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)
knn.score(X_test_scaled, y_test)

"""Confusion Matrix."""

from sklearn.metrics import confusion_matrix
mat=confusion_matrix(y_test,knn.predict(X_test_scaled))
df_cm = pd.DataFrame(mat, list(targets.values()), list(targets.values()))
sns.set(font_scale=1.0) # for label size
plt.figure(figsize = (12,8))
sns.heatmap(df_cm, annot=True, annot_kws={"size": 12},cmap="terrain")

"""Let's try different values of n_neighbors to fine tune and get better results."""

k_range = range(1,11)
scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train_scaled, y_train)
    scores.append(knn.score(X_test_scaled, y_test))

plt.xlabel('k')
plt.ylabel('accuracy')
plt.scatter(k_range, scores)
plt.vlines(k_range,0, scores, linestyle="dashed")
plt.ylim(0.96,0.99)
plt.xticks([i for i in range(1,11)]);

"""Classification using Support Vector Classifer (SVC).

"""

from sklearn.svm import SVC

svc_linear = SVC(kernel = 'linear').fit(X_train_scaled, y_train)
print("Linear Kernel Accuracy: ",svc_linear.score(X_test_scaled,y_test))

svc_poly = SVC(kernel = 'rbf').fit(X_train_scaled, y_train)
print("Rbf Kernel Accuracy: ", svc_poly.score(X_test_scaled,y_test))

svc_poly = SVC(kernel = 'poly').fit(X_train_scaled, y_train)
print("Poly Kernel Accuracy: ", svc_poly.score(X_test_scaled,y_test))

"""Let's try to increase SVC Linear model accuracy by parameter tuning.

GridSearchCV can help us find the best parameters.
"""

from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

parameters = {'C': np.logspace(-3, 2, 6).tolist(), 'gamma': np.logspace(-3, 2, 6).tolist()}
# 'degree': np.arange(0,5,1).tolist(), 'kernel':['linear','rbf','poly']

model = GridSearchCV(estimator = SVC(kernel="linear"), param_grid=parameters, n_jobs=-1, cv=4)
model.fit(X_train, y_train)

print(model.best_score_ )
print(model.best_params_ )

"""POINTS TO BE HIGHLIGHTED

1. Interestingly liner kernel also gives satisfactory results but fine tuning increases the computation and might be inefficient in some cases
2. The accuracy can be increased in poly kernel by tweaking parameters but might lead to intensive overfitting.
3. RBF has better result than linear kernel.
4. Poly kernel so far wins by a small margin.

Classifying using decision tree.
"""

from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
clf.score(X_test,y_test)

"""Let's visualize the import features which are taken into consideration by decision trees."""

plt.figure(figsize=(10,4), dpi=80)
c_features = len(X_train.columns)
plt.barh(range(c_features), clf.feature_importances_)
plt.xlabel("Feature importance")
plt.ylabel("Feature name")
plt.yticks(np.arange(c_features), X_train.columns)
plt.show()

"""Classification using Random Forest."""

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(max_depth=4,n_estimators=100,random_state=42).fit(X_train, y_train)

print('RF Accuracy on training set: {:.2f}'.format(clf.score(X_train, y_train)))
print('RF Accuracy on test set: {:.2f}'.format(clf.score(X_test, y_test)))

"""**Classification report**

Let's use yellowbrick for classification report as they are great for visualizing in a tabular format.
"""

from yellowbrick.classifier import ClassificationReport
classes=list(targets.values())
visualizer = ClassificationReport(clf, classes=classes, support=True,cmap="Blues")

visualizer.fit(X_train, y_train)  # Fit the visualizer and the model
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()

"""Classification using Gradient Boosting."""

from sklearn.ensemble import GradientBoostingClassifier
grad = GradientBoostingClassifier().fit(X_train, y_train)
print('Gradient Boosting accuracy : {}'.format(grad.score(X_test,y_test)))