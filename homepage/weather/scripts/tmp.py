def send_email(user, pwd, recipient, subject, body):
    """
    Sends email to recipients, log to log file if email was send or not

    """
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # try:
    server = smtplib.SMTP_SSL("smtp.seznam.cz", 465)
    server.ehlo()
    # server.starttls()
    server.login(user, pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print('successfully sent the mail')
# except:
    print("failed to send mail")


user = 'siba.robot@seznam.cz'
password = 'lplojiju321'
subject = "Nove udalosti MS"
recipient = [
        "david.siba@gmail.com",
    ]

send_email(user,password,recipient,"test","test")
