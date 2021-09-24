from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import Config
from app.email.server_smtp import ServerSMTP
from flask import render_template

class Mailer():

    def __init__(self, template: str, subject: str):
        self.email_msg = MIMEMultipart()
        self.email_body = template
        self.email_subject = subject

    
    def send_email(self,  entity):
        self.email_msg['From'] = Config.EMAIL_USER
        self.email_msg['To'] = entity.email
        self.email_msg['Subject'] = self.email_subject
        corpo = render_template( f"{self.email_body}.j2", entity=entity)
        self.email_msg.attach(MIMEText(corpo, 'html'))
        server_smtp = ServerSMTP()
        server_smtp.server.sendmail(self.email_msg['From'], self.email_msg['To'], self.email_msg.as_string())


    def attach_document(self, path):
        # ex: path: "C:\\Users\\lucas\\Desktop\\Lucas\\Faculdade\\teste.txt"
        attachment = open(path, 'rb') # read_binary

        # Lê o arquivo no modo binário, codifica o arquivo em base 64 (protocolo do e-mail)
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)

        # Adiciona cabeçalho no tipo anexo de e-mail
        att.add_header('Content-Disposition', 'attachment') #; filename = {filename}
        attachment.close()

        # vincula anexo no corpo do e-mail
        self.email_msg.attach(att)
