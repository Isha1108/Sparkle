import smtplib

# def sendmail():
    
#     sender = 'ishampatel01@gmail.com'
#     receivers = ['isha.mp@somaiya.edu']

#     message = """From: From Person <from@fromdomain.com>
#     To: To Person <to@todomain.com>
#     Subject: SMTP e-mail test

#     This is a test e-mail message.
#     """    
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message)         
#     print ("Successfully sent email")
# sendmail()

def send_link():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = "kashyapahana20@gmail.com"
    toaddr = "isha.mp@somaiya.edu"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = " Hi "

    body = "test"
    msg.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(fromaddr, "Kash@1108")

    text = msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    server.quit()

send_link()