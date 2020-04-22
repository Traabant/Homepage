from scripts.myLog import MyLog as log

class Email():

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
        try:
            server = smtplib.SMTP_SSL("smtp.seznam.cz", 465)
            server.ehlo()
            # server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            # print ('successfully sent the mail')
            log('successfully sent the mail')
        except:
            log("failed to send mail")