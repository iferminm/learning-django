# -*- encoding: utf-8 -*-
from django.conf import settings
import smtplib as smtp


class Mailer():

    def __construct_mail_text(self, student_name, student_email, subject, text):
        message = u"""From: Israel Fermin <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s

Gracias
        """ % (settings.DEFAULT_FROM_EMAIL, student_name, student_email, student_name, text)

        return message

    def send_mail(self, student_name, student_mail, subject, text):
        from_address = settings.DEFAULT_FROM_EMAIL
        passwd = settings.DEFAULT_FROM_EMAIL_PASS

        message = self.__construct_mail_text(student_name, student_mail, subject, text)
        mail_server = smtp.SMTP(settings.DEFAULT_EMAIL_HOST, settings.DEFAULT_EMAIL_PORT)
        mail_server.starttls()
        mail_server.login(from_address, passwd)
        mail_server.sendmail(from_address, student_mail, message)
        mail_server.quit()

