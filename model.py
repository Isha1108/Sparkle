import pandas as pd
from sklearn.neighbors import KNeighborsClassifier 
import xgboost 
import numpy as np
import pickle
from decimal import Decimal
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
data_set= pd.read_excel('sih.xlsx')  
data_set.loc[(data_set.Y_var == 'No'), ['Y_var']] = 1
data_set.loc[(data_set.Y_var == 'Dyslexia'), ['Y_var']] = 2
data_set.loc[(data_set.Y_var == 'Dyscalculia'), ['Y_var']] = 3
x= data_set.iloc[:, :-1].values  
y= data_set.iloc[:, -1].values  
data_set_test= pd.read_excel('sih.xlsx')    
data_set_test.loc[(data_set_test.Y_var == 'No'), ['Y_var']] = 1
data_set_test.loc[(data_set_test.Y_var == 'Dyslexia'), ['Y_var']] = 2
data_set_test.loc[(data_set_test.Y_var == 'Dyscalculia'), ['Y_var']] = 3
#Extracting Independent and dependent Variable  
x_test= data_set_test.iloc[:, :-1].values  
y_test= data_set_test.iloc[:, -1].values  
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.20, random_state=0) 

def return_top_n_pred_prob_df(n, model, X_test, column_name):
    predictions = model.predict_proba(X_test)
    preds_idx = np.argsort(-predictions) 
    classes = pd.DataFrame(model.classes_, columns=['class_name'])
    classes.reset_index(inplace=True)
    top_n_preds = pd.DataFrame()
    for i in range(n):
        top_n_preds[column_name + '_prediction_{}_num'.format(i)] =     [preds_idx[doc][i] for doc in range(len(X_test))]
        top_n_preds[column_name + '_prediction_{}_probability'.format(i)] = [predictions[doc][preds_idx[doc][i]] for doc in range(len(X_test))]
        top_n_preds = top_n_preds.merge(classes, how='left', left_on= column_name + '_prediction_{}_num'.format(i), right_on='index')
        top_n_preds = top_n_preds.rename(columns={'class_name': column_name + '_prediction_{}'.format(i)})
        try: top_n_preds.drop(columns=['index', column_name + '_prediction_{}_num'.format(i)], inplace=True) 
        except: pass
    return top_n_preds

xg = xgboost.XGBClassifier(max_depth= 2, n_estimators=100)
xg.fit(x,y)    

xg3 = open('xg2.sav', 'wb') 

# source, destination 
pickle.dump(xg, xg3)  
xg3.close()