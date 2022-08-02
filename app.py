# from crypt import methods
from os import access
from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask
from flask_mail import Mail
import speech_recognition as sr
import gspread
import pandas as pd
import pickle
import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
import pickle





app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sparkle'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'as1303879@gmail.com'
app.config['MAIL_PASSWORD'] = 'lincolnab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():

    if request.method == 'POST':
        print("gg")
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        print(email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM p_creds WHERE p_email = %s AND password = %s ', [email, password])
        # Fetch one record and return result

        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lex_test1 WHERE p_email = %s ', [email])
            solution = cursor.fetchone()
            if solution:
                session['loggedin'] = True
                session['p_email'] = account['p_email']
            # account exists and test taken, so redirect to profile page
                return redirect(url_for('student_profile'))
            else:
                session['loggedin'] = True
                session['p_email'] = account['p_email']
                return redirect(url_for('instructions'))
            # account exists and test NOT taken, so redirect to exam page page

    return render_template('signin.html')


# def sendmail(s_name, password, p_name, school, p_email, p_phone):
#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText

#     fromaddr = "kashyapahana20@gmail.com"
#     toaddr = str(p_email)

#     msg = MIMEMultipart()
#     msg['From'] = fromaddr
#     msg['To'] = toaddr
#     msg['Subject'] = " Your child's registration details "
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT s_id FROM p_creds WHERE p_email = %s ', [p_email])
#     s_id = cursor.fetchone()

#     body = "Name: " + str(s_name)+'\n' + "Password: " + str(password)+'\n' + "Registered Parent's Name: " + str(p_name)+'\n' + "School: " + str(
#         school)+'\n' + "Parent's registered email: " + str(p_email)+'\n' + "Mobile Number: " + str(p_phone)+'\n' + "Student's ID: " + str(s_id['s_id'])+'\n'
#     msg.attach(MIMEText(body, 'plain'))

#     server = smtplib.SMTP('smtp.gmail.com', port=587)
#     server.starttls()
#     server.login(fromaddr, "Kash@1108")

#     text = msg.as_string()
#     server.sendmail(fromaddr, toaddr, text)
#     print("hjsgcjydg")
#     server.quit()


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    s_id = 00000
    if request.method == 'POST':
        s_name = request.form['s_name']
        age = request.form['age']
        password = request.form['password']
        p_name = request.form['p_name']
        school = request.form['school']
        p_email = request.form['p_email']
        p_phone = request.form['p_phone']

        print(s_name, age, password, p_name, school, p_email, p_phone)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO p_creds(s_name, age, p_name, school, p_email, p_phone, password) VALUES(%s,%s,%s,%s,%s,%s,%s)', [
                       s_name, age, p_name, school, p_email, p_phone, password])
        mysql.connection.commit()
        # sendmail(s_name, password, p_name, school, p_email, p_phone)

        msg = 'Successfully registered! Please Sign-In'
        print('done')
        # student will be redirected for a test immediately
        return redirect(url_for('student_login'))

    return render_template('signup.html')


@app.route('/d_signup', methods=['GET', 'POST'])
def d_signup():
    if request.method == 'POST':
        d_name = request.form['d_name']
        d_password = request.form['d_password']
        d_email = request.form['mail']
        desi = request.form['Designation']
        d_no = request.form['num']
        d_school = request.form['d_school']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO d_creds VALUES(%s,%s,%s,%s,%s,%s)', [d_name,desi,d_email,d_no,d_password,d_school])
        mysql.connection.commit()
        return redirect(url_for('d_login'))
    return render_template('d_signup.html')


@app.route('/d_login', methods=['GET', 'POST'])
def d_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM d_creds WHERE d_pass = %s ', [password])
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['d_mail'] = account['d_mail']
            session['d_school'] = account['d_school']
            return redirect(url_for('dr_profile'))

    return render_template('d_login.html')


@app.route('/dr_landing')
def dr_landing():
    return render_template('dr_landing.html')


@app.route('/doctor-patient-profile')
def dpp():
    return render_template('doctor-patient-profile.html')


@app.route('/doctor-profile')
def dr_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT d_name,designation,d_mail,d_phone,d_school FROM d_creds WHERE d_mail = %s ', [session['d_mail']])
    account = cursor.fetchone()
    
    return render_template('doctor-profile.html',account=account)


@app.route('/student_profile')
def student_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_name,age,school FROM p_creds WHERE p_email = %s ', [session['p_email']])
    account = cursor.fetchone()
    return render_template('student_profile.html',name=account['s_name'],age=account['age'],school=account['school'])


@app.route('/student_profile1', methods=['GET', 'POST'])
def student_profile1():
    test = ''
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('18sXYVa_hqEAcZAuuzXplbqKcKsLj0dPZ80V5ZuNw9uI')
    Worksheet = sh.worksheet('Sheet1')
    list_of_lists = Worksheet.get_all_values()
    questions_list = []
    responses_of_parent = []

    # student_name = 'Ronit Bhamere'
    # q1 = list_of_lists[0][1]
    # q2 = list_of_lists[0][2]
    # q3 = list_of_lists[0][3]
    # q4 = list_of_lists[0][4]
    # q5 = list_of_lists[0][5]
    # q6 = list_of_lists[0][6]
    # q7 = list_of_lists[0][7]
    # q8 = list_of_lists[0][8]
    # q9 = list_of_lists[0][9]
    # q10 = list_of_lists[0][10]
    # q11 = list_of_lists[0][11]
    # q12 = list_of_lists[0][12]
    # q13 = list_of_lists[0][13]
    # q14 = list_of_lists[0][14]
    # q15 = list_of_lists[0][15]
    # dic = {}

    # questions_list = [q1, q2, q3, q4, q5, q6,
    #                   q7, q8, q9, q10, q11, q12, q13, q14, q15]

    # for x in list_of_lists:
    #     if student_name in x[16]:
    #         a1 = x[1]
    #         a2 = x[2]
    #         a3 = x[3]
    #         a4 = x[4]
    #         a5 = x[5]
    #         a6 = x[6]
    #         a7 = x[7]
    #         a8 = x[8]
    #         a9 = x[9]
    #         a10 = x[10]
    #         a11 = x[11]
    #         a12 = x[12]
    #         a13 = x[13]
    #         a14 = x[14]
    #         a15 = x[15]
    #         student_id = x[18]

    # responses_of_parent = [a1, a2, a3, a4, a5, a6,
    #                        a7, a8, a9, a10, a11, a12, a13, a14, a15]
    # dic = dict(zip(questions_list, responses_of_parent))

    # print(dic)

    # # st_name = 'Ronit'

    # # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # # cursor.execute('SELECT * FROM analysis WHERE st_name=%s', [st_name])
    # # ana = cursor.fetchall()

    # # print(ana)

    # if request.method == 'POST' and 't1' in request.form:
    #     t1 = request.form.getlist('t1')
    #     t2 = request.form.getlist('t2')
    #     print(t1, t2)
    #     test = t1[0]

    # s_id = 123

    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('INSERT INTO courses VALUES(%s,%s)', [s_id, test])
    # mysql.connection.commit()



    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM sample')
    # lis = cursor.fetchall()

    # list1 = []
    # for i in range(len(lis)):
    #     x = lis[i]
    #     list_h = []
    #     for key in x.values():
    #         list_h.append(key)
    #     list1.append(list_h)
    # print(list1)

    # loaded_model = pickle.load(open('xg2.sav', 'rb'))

    # for i in list1:
    #     test = [i]
    #     print(test)
    #     output = return_top_n_pred_prob_df(3, loaded_model, test, "test")
    #     l = output.values.tolist()

    #     disease1 = l[0][1]
    #     disease2 = l[0][3]
    #     disease3 = l[0][5]
    #     acc1 = str(round(l[0][0]*100, 3))
    #     acc2 = str(round(l[0][2]*100, 3))
    #     acc3 = str(round(l[0][4]*100, 3))

    #     if disease1 == 1:
    #         disease1 = 'No Disease '
    #     elif disease1 == 2:
    #         disease1 = "Dyslexia "
    #     elif disease1 == 3:
    #         disease1 = "Dyscalculia "

    #     print(" The Probability of " + disease1 + " is : " + acc1)

    #     if disease2 == 1:
    #         disease2 = 'No Disease '
    #     elif disease2 == 2:
    #         disease2 = "Dyslexia "
    #     elif disease2 == 3:
    #         disease2 = "Dyscalculia "
    #     print(" The Probability of " + disease2 + " is : " + acc2)

    #     if disease3 == 1:
    #         disease3 = 'No Disease '
    #     elif disease3 == 2:
    #         disease3 = "Dyslexia "
    #     elif disease3 == 3:
    #         disease3 = "Dyscalculia "
    #     print(" The Probability of " + disease3 + " is : " + acc3)

    #     print(disease1, acc1, disease2, acc2, disease3, acc3)

    #     if disease1 == "No Disease is Identified":
    #         print("No treatment required.")
    #     elif (disease1 == "Dyslexia" or "Dyscalculia") and (disease2 == "Dyslexia" or "Dyscalculia"):
    #         print(disease1, acc1, disease2, acc2)


    # return render_template('student_profile1.html', dic=dic, disease1=disease1, acc1=acc1, disease2=disease2, acc2=acc2)


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





@app.route('/student_list')
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_creds WHERE school=%s', [session['d_school']])
    lis = cursor.fetchall()
    

    # list1 = []
    # for i in range(len(lis)):
    #     x = lis[i]
    #     list_h = []
    #     for key in x.values():
    #         list_h.append(key)
    #     list1.append(list_h)
    # print(list1)

    # loaded_model = pickle.load(open('xg2.sav', 'rb'))

    # for i in list1:
    #     test = [i]
    #     print(test)
    #     output = return_top_n_pred_prob_df(3, loaded_model, test, "test")
    #     l = output.values.tolist()

    #     disease1 = l[0][1]
    #     disease2 = l[0][3]
    #     disease3 = l[0][5]
    #     acc1 = str(round(l[0][0]*100, 3))
    #     acc2 = str(round(l[0][2]*100, 3))
    #     acc3 = str(round(l[0][4]*100, 3))

    #     if disease1 == 1:
    #         disease1 = 'No Disease is Identified'
    #     elif disease1 == 2:
    #         disease1 = "Dyslexia is Identified"
    #     elif disease1 == 3:
    #         disease1 = "Dyscalculia is Identified"

    #     print(" The Probability of " + disease1 + " is : " + acc1)

    #     if disease2 == 1:
    #         disease2 = 'No Disease is Identified'
    #     elif disease2 == 2:
    #         disease2 = "Dyslexia is Identified"
    #     elif disease2 == 3:
    #         disease2 = "Dyscalculia is Identified"
    #     print(" The Probability of " + disease2 + " is : " + acc2)

    #     if disease3 == 1:
    #         disease3 = 'No Disease is Identified'
    #     elif disease3 == 2:
    #         disease3 = "Dyslexia is Identified"
    #     elif disease3 == 3:
    #         disease3 = "Dyscalculia is Identified"
    #     print(" The Probability of " + disease3 + " is : " + acc3)

    #     print(disease1, acc1, disease2, acc2, disease3, acc3)

    #     if disease1 == "No Disease is Identified":
    #         print("No treatment required.")
    #     elif (disease1 == "Dyslexia" or "Dyscalculia") and (disease2 == "Dyslexia" or "Dyscalculia"):
    #         print(disease1, acc1, disease2, acc2)

            

    return render_template('student_list.html',lis=lis)


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/speechr')
def speechr():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)

    paragraph_string = para_list[0][1]

    r = sr.Recognizer()

    paragraph = paragraph_string.lower()
    punc = '''!()-[]{};:'",<>./?@#$%^&*~'''

    for ele in paragraph:
        if ele in punc:
            paragraph = paragraph.replace(ele, "")

    paragraph = paragraph.split()
    print(paragraph)
    text = ''
    text_og = ''
    # For Identification of Dyslexia. Small paragraph will be given.
    # Paragraph to be mentioned in paragraph_string variable coming from database.
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        try:
            text_og = str(r.recognize_google(audio_data, language="en-IN"))
            text = text_og.lower()
            text = text.split(" ")
        except:
            pass
    print(text)
    count = 0
    """for i in range(len(text)):
        if text[i] in paragraph:
            print(text[i])
            count = count+1
    print("Count : " + str(count))"""

    import itertools
    for (a, b) in zip(paragraph, text):
        if a == b:
            print(a, b)
            count += 1
    print(count)
    accuracy = 100 * (count/len(paragraph))
    accuracy = round(accuracy, 2)

    print('Analysis')
    print('Text given to student to read: ', paragraph_string)
    print('Text spoken by the Student : ', text_og)
    print('Accuracy Percentage of right words: ', accuracy)
    # print('Number of right words spoken: {right} and number of wrong words spoken: {wrong}'.format(right = len(right_words_spoken_list), wrong = len(wrong_words_spoken_list)))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test1 VALUES(%s,%s,%s,%s)',
                   [session['p_email'], paragraph_string, text_og, accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test1'))


@app.route('/speechr1')
def speechr1():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)

    paragraph_string = para_list[1][1]

    r = sr.Recognizer()

    paragraph = paragraph_string.lower()
    punc = '''!()-[]{};:'",<>./?@#$%^&*~'''

    for ele in paragraph:
        if ele in punc:
            paragraph = paragraph.replace(ele, "")

    paragraph = paragraph.split()
    print(paragraph)
    text = ''
    text_og = ''
    # For Identification of Dyslexia. Small paragraph will be given.
    # Paragraph to be mentioned in paragraph_string variable coming from database.
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=20)
        print("Recognizing...")
        # convert speech to text
        try:
            text_og = str(r.recognize_google(audio_data, language="en-IN"))
            text = text_og.lower()
            text = text.split(" ")
        except:
            pass
    print(text)
    count = 0
    for i in range(len(text)):
        if text[i] in paragraph:
            print(text[i])
            count = count+1
    print("Count : " + str(count))

    # import itertools
    # for (a,b) in zip(paragraph, text):
    #     if a==b:
    #         print (a,b)
    #         count+=1
    # print(count)
    accuracy = 100 * (count/len(paragraph))
    accuracy = round(accuracy, 2)

    print('Analysis')
    print('Text given to student to read: ', paragraph_string)
    print('Text spoken by the Student : ', text_og)
    print('Accuracy Percentage of right words: ', accuracy)
    # print('Number of right words spoken: {right} and number of wrong words spoken: {wrong}'.format(right = len(right_words_spoken_list), wrong = len(wrong_words_spoken_list)))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test2 VALUES(%s,%s,%s,%s)',
                   [session['p_email'], paragraph_string, text_og, accuracy])
    mysql.connection.commit()
    return redirect(url_for('common_test'))


@app.route('/student_test')
def student_test():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)

    paragraph_string = str(para_list[0][1])

    return render_template('student_test.html',para_list=para_list)


@app.route('/Thankyou', methods=['GET', 'POST'])
def Thankyou():
    if request.method == 'POST' and 'q1' in request.form:
        option = request.form['q1']
        if option == 7:
            score += 1
    print(score)

    return render_template('Thankyou.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')


@app.route('/common_test', methods=['GET', 'POST'])
def common_test():
    score = 0
    if request.method == 'POST' and 'q1' in request.form and 'q2' in request.form and 'q3' in request.form:
        option1 = request.form['q1']
        option2 = request.form['q2']
        option3 = request.form['q3']
        
        
        if option1 == "yes":
            score += 1
        if option2 == "yes":
            score += 1
        if option3 == "yes":
            score += 1
        print("Score:"+str(score))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO cal_test VALUES(%s,%s,%s,%s,%s)',
                   [session['p_email'], option1, option2, option3, score])
        mysql.connection.commit()
        return redirect(url_for('student_profile'))
    
    return render_template('common_test.html')



@app.route('/student_test1')
def student_test1():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)

    paragraph_string = str(para_list[1][1])
    return render_template('student_test1.html',para_list=para_list)


@app.route('/p_login', methods=['GET', 'POST'])
def p_login():
    if request.method == 'POST':
       
        # Create variables for easy access
        p_email = request.form['p_email']
        p_pass = request.form['password']
       
        # Check if account exists using MySQL

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM p_creds WHERE p_email = %s ', [p_email])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['p_name']=account['p_name']
            session['s_name']=account['s_name']
            session['p_email']=account['p_email']            
            return redirect(url_for('parent_profile'))
            # account exists and test NOT taken, so redirect to exam page page
    return render_template('p_login.html')

@app.route('/parent_profile', methods=['GET','POST'])
def parent_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_creds WHERE p_email=%s', [session['p_email']])
    para = cursor.fetchone()
    
    return render_template('parent_profile.html',para=para)

@app.route('/parent_diag_test1', methods=['GET','POST'])
def parent_dys_test():
    if request.method=="POST":
        q1=request.form['q1']
        q2=request.form['q2']
        q3=request.form['q3']
        q4=request.form['q4']
        q5=request.form['q5']
        q6=request.form['q6']
        q7=request.form['q7']
        q8=request.form['q8']
        q9=request.form['q9']
        q10=request.form['q10']
        q11=request.form['q11']
        q12=request.form['q12']
        q13=request.form['q13']
        q14=request.form['q14']
        q15=request.form['q15']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO dys_parent_test(p_email,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'],q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15])
        mysql.connection.commit()
        return redirect(url_for('parent_profile'))
    return render_template('Questionaire.html')

@app.route('/<s_name>')
def s_name(s_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_name,school,p_email FROM p_creds WHERE s_name=%s',[s_name])
    account=cursor.fetchone()

    cursor.execute('SELECT * FROM dys_parent_test WHERE p_email=%s',[account['p_email']])
    account1 =cursor.fetchone()
    for i in account1:
        if account1[i]==0:
            account1[i]="Poor"
        elif account1[i]==1:
            account1[i]="Good"
        elif account1[i]==2:
            account1[i]="Excellent"
    # account1 = account1.values()
    # account1.replace(0,"Poor")
    # account1.replace(1,"Good")
    # account1.replace(2,"Excellent")
    # print(account1['dict_values'])

    print('aaaaaaaaaaaaaaaaaaa')
    print(account1)
    return render_template('student_profile1.html',account=account, account1=account1)

if __name__ == "__main__":
    app.run(debug=True)