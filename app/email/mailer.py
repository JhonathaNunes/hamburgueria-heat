from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from config import Config
import smtplib
import jinja2
import os
from threading import Thread


def render_without_request(template_name, **template_vars):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('app', 'templates')
    )
    template = env.get_template(template_name)
    return template.render(**template_vars)


def attach_documents(msg, paths):
    for path in paths:
        attachment = open(path, 'rb')

        # Lê o arquivo no modo binário
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)

        # Adiciona cabeçalho no tipo anexo de e-mail
        att.add_header('Content-Disposition', 'attachment')
        attachment.close()

        # Vincula anexo no corpo do e-mail
        msg.attach(att)


def attach_images(msg, images):
    count = 1
    for image in images:

        attachment = open(os.path.join('app/static/images/', image), 'rb')
        msgImage = MIMEImage(attachment.read())
        attachment.close()

        msgImage.add_header('Content-ID', f'<image{count}>')
        msg.attach(msgImage)

        count = count + 1


def send_mail(params: dict):
    # Parâmetros obrigatórios
    sender = params.get('sender')
    to = params.get('to')
    subject = params.get('subject')
    template = params.get('template')
    text_type = params.get('text_type')

    # Parâmetros opcionais
    cc = params.get('cc', [])
    bcc = params.get('bcc', [])
    images = params.get('images', [])
    entity = params.get('entity', {})
    path_document = params.get('path_document', [])

    # Prepara a mensagem a ser enviada
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject

    if len(cc):
        msg['Cc'] = cc

    if len(bcc):
        msg['Bcc'] = bcc

    # Renderiza o html do email baseado em um template
    corpo = render_without_request(f'{template}.j2', entity=entity)
    msg.attach(MIMEText(corpo, text_type))

    if len(path_document):
        attach_documents(msg, path_document)
    if len(images):
        attach_images(msg, images)

    # Conexão SMTP ao server e envio de mensagem
    server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


class EmailThread(Thread):
    def __init__(self, params: dict):
        self.params = params
        Thread.__init__(self)
    
    def run(self) -> None:
        send_mail(self.params)
