import smtplib
def send_mail_founder(mail,name,number):
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.connect('smtp.gmail.com',587)
    s.starttls()
    email='vishnulatha006@gmail.com'
    password='yaebnksqpkudxyoq'
    s.login(email,password)
    message =f'The child you posted is lost by {name} and Phone Number is{number} '
    s.sendmail(email,mail,message)
    print("Sent")
    s.quit()

def send_mail_loser(mail,name,number):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.connect('smtp.gmail.com',587)
        s.starttls()
        email='vishnulatha006@gmail.com'
        password='yaebnksqpkudxyoq'
     
        s.login(email,password)
        message =f"Your child  is found by  {name} and Phone Number is{number} "
        s.sendmail(email,mail,message)
        print("Sent")
        s.quit()
        