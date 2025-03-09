# import traceback
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# class EmailService:
#     def send_email(self, to_email, user_uid, sent_otp):
#
#         message = MIMEMultipart()
#         message['From'] = settings.get('SMTP','USERNAME')
#         message['To'] = to_email
#         message['Subject'] = MAIL_TEMPLETE['signup_subject']
#
#
#         # Attach the HTML content to the email
#         html_content = MAIL_TEMPLETE['signup_tempelate'].replace('{{ OTP }}', str(sent_otp)).replace('{{uid}}',user_uid).replace('{{ emailId }}', to_email)
#         message.attach(MIMEText(html_content, 'html'))
#
#         # Connect to the SMTP server
#         with smtplib.SMTP(configure.get('SMTP','SERVER'),configure.getint('SMTP','PORT')) as server:
#             server.starttls()
#             server.login(configure.get('SMTP','USERNAME'), configure.get('SMTP','PASSWORD'))
#             print("Sending Mail")
#             # Send the email
#             server.sendmail(configure.get('SMTP','USERNAME'), to_email, message.as_string())
#         return {"status":"success","message":"mail sent successful"}
#
