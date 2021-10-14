from email.mime.multipart import MIMEMultipart # mime - padronização das estruturas dos emails
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from config import Config
import smtplib
import jinja2
import os

#https://stackoverflow.com/questions/17206728/attributeerror-nonetype-object-has-no-attribute-app
def render_without_request(template_name, **template_vars):
    env = jinja2.Environment( #usadas para armazenar a configuração e objetos globais
        loader=jinja2.PackageLoader('app','templates')
    )
    template = env.get_template(template_name)
    return template.render(**template_vars)

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
    if len(cc): msg['Cc'] = cc
    if len(bcc): msg['Bcc'] = bcc

    # Renderiza o html do email baseado em um template
    corpo = render_without_request( f'{template}.j2', entity=entity) # tive que fazer isso porque a thread de segundo plano está fora do ciclo de solicitação do Flask, e por isso não tem acesso a um contexto de solicitação.
    msg.attach(MIMEText(corpo, text_type))
    
    if len(path_document): attach_documents(msg, path_document) # Anexa documentos
    if len(images): attach_images(msg, images) # Anexa imagens

    # Conexão SMTP ao server e envio de mensagem
    server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) # Instância e encapsula uma conexão SMTP
    server.ehlo() # Identifique-se em um servidor ESMTP usando EHLO, o cliente informa ao servidor que uma transação pode ser iniciada. Isto significa que deste ponto em diante, o cliente pode enviar comandos que, se forem na ordem correta, permitem o envio de um email.
    server.starttls() # Coloca a conexão SMTP no modo TLS. Todos os comandos SMTP a seguir serão criptografados.
    server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD) # Conecta ao servidor com conta, no caso estamos usando host do gmail
    server.sendmail(msg['From'], msg['To'], msg.as_string()) # Envio do email
    server.quit() # Mata a conexão ao server smtp

def attach_documents(msg, paths):
    for path in paths:
        attachment = open(path, 'rb') # ex: path: 'C:\\Users\\lucas\\Desktop\\Lucas\\Faculdade\\teste.txt' / read_binary

        # Lê o arquivo no modo binário, 
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att) # Codifica o arquivo em base 64 (protocolo do e-mail)

        # Adiciona cabeçalho no tipo anexo de e-mail
        att.add_header('Content-Disposition', 'attachment') #; filename = {filename}
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
