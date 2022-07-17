import pickle
import numpy as np
import pandas as pd
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier 
import xgboost as xgb
import numpy as np
import pickle
from decimal import Decimal
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
def return_top_n_pred_prob_df(n, model, X_test, column_name):
    predictions = model.predict_proba(X_test)
    preds_idx = np.argsort(-predictions)
    classes = pd.DataFrame(model.classes_, columns=['class_name'])
    classes.reset_index(inplace=True)
    top_n_preds = pd.DataFrame()
    for i in range(n):
        top_n_preds[column_name + '_prediction_{}_num'.format(
            i)] = [preds_idx[doc][i] for doc in range(len(X_test))]
        top_n_preds[column_name + '_prediction_{}_probability'.format(
            i)] = [predictions[doc][preds_idx[doc][i]] for doc in range(len(X_test))]
        top_n_preds = top_n_preds.merge(
            classes, how='left', left_on=column_name + '_prediction_{}_num'.format(i), right_on='index')
        top_n_preds = top_n_preds.rename(
            columns={'class_name': column_name + '_prediction_{}'.format(i)})
        try:
            top_n_preds.drop(
                columns=['index', column_name + '_prediction_{}_num'.format(i)], inplace=True)
        except:
            pass
    return top_n_preds

loaded_model = pickle.load(open('xg2.sav', 'rb')) 

test = np.zeros([1,22],dtype = int)
test[0][0] = 2
test[0][1] = 1
test[0][2] = 1
test[0][3] = 1
test[0][4] = 2
test[0][5] = 2
test[0][6] = 2
test[0][7] = 1
test[0][8] = 2
test[0][9] = 2
test[0][10] = 2
test[0][11] = 2
test[0][12] = 2
test[0][13] = 2
test[0][14] = 2
test[0][15] = 50
test[0][16] = 60
test[0][17] = 0
test[0][18] = 1
test[0][19] = 1
test[0][20] = 0
test[0][21] = 1


output=return_top_n_pred_prob_df(3,loaded_model,test,"test")
l = output.values.tolist()

disease1 = l[0][1]
disease2 = l[0][3]
disease3 = l[0][5]
acc1 = str(round(l[0][0]*100, 3))
acc2 = str(round(l[0][2]*100, 3))
acc3 = str(round(l[0][4]*100, 3))

if disease1 == 1:
  disease1 = 'No Disease is Identified'
elif disease1 == 2:
  disease1 = "Dyslexia is Identified"
elif disease1 == 3:
  disease1 = "Dyscalculia is Identified" 


print(" The Probability of " + disease1 + " is : " + acc1)

if disease2 == 1:
  disease2 = 'No Disease is Identified'
elif disease2 == 2:
  disease2 = "Dyslexia is Identified"
elif disease2 == 3:
  disease2 = "Dyscalculia is Identified"
print(" The Probability of " + disease2 + " is : " + acc2)  

if disease3 == 1:
  disease3 = 'No Disease is Identified'
elif disease3 == 2:
  disease3 = "Dyslexia is Identified"
elif disease3 == 3:
  disease3 = "Dyscalculia is Identified"
print(" The Probability of " + disease3 + " is : " + acc3) 

print(disease1, acc1, disease2, acc2 ,disease3, acc3)

if disease1 == "No Disease is Identified":
    print("No treatment required.")
elif (disease1 == "Dyslexia" or "Dyscalculia") and (disease2 == "Dyslexia" or "Dyscalculia") :
    print(disease1, acc1, disease2, acc2)
    
    