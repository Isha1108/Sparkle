import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('18sXYVa_hqEAcZAuuzXplbqKcKsLj0dPZ80V5ZuNw9uI')
Worksheet= sh.worksheet('Sheet1')
list_of_lists = Worksheet.get_all_values()

student_name = 'Ronit Bhamere'
q1 = list_of_lists[0][1]
q2 = list_of_lists[0][2]
q3 = list_of_lists[0][3]
q4 = list_of_lists[0][4]
q5 = list_of_lists[0][5]
q6 = list_of_lists[0][6]
q7 = list_of_lists[0][7]
q8 = list_of_lists[0][8]
q9 = list_of_lists[0][9]
q10 = list_of_lists[0][10]
q11 = list_of_lists[0][11]
q12 = list_of_lists[0][12]
q13 = list_of_lists[0][13]
q14 = list_of_lists[0][14]
q15 = list_of_lists[0][15]

questions_list = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15]

for x in list_of_lists:
    if student_name in x[16]:
       a1 = x[1]
       a2 = x[2]
       a3 = x[3]
       a4 = x[4]
       a5 = x[5]
       a6 = x[6]
       a7 = x[7]
       a8 = x[8]
       a9 = x[9]
       a10 = x[10]
       a11 = x[11]
       a12 = x[12]
       a13 = x[13]
       a14 = x[14]
       a15 = x[15]
       student_id = x[18]

responses_of_parent = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15]      
print(responses_of_parent)