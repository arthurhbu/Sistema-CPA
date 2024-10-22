import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def zip_markdown_files(output_filename, folder_path):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):  # Filtrar apenas arquivos .md
                    filepath = os.path.join(root, file)
                    zipf.write(filepath, os.path.relpath(filepath, folder_path))

# Exemplo de uso
# zip_markdown_files('relatorios.zip', 'pasta_dos_markdowns')



def enviar_email_com_anexo(arquivo_zip, destinatario_email, remetente_email, senha_remetente):
    # Configuração do email
    msg = MIMEMultipart()
    msg['From'] = remetente_email
    msg['To'] = destinatario_email
    msg['Subject'] = 'Relatórios Markdown'

    # Corpo do email
    body = 'Segue em anexo o arquivo com os relatórios em Markdown.'
    msg.attach(MIMEText(body, 'plain'))

    # Anexo
    attachment = open(arquivo_zip, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={arquivo_zip}')
    msg.attach(part)

    # Envio do email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente_email, senha_remetente)
        text = msg.as_string()
        server.sendmail(remetente_email, destinatario_email, text)
        server.quit()
        print(f'Email enviado com sucesso para {destinatario_email}')
    except Exception as e:
        print(f'Erro ao enviar o email: {e}')

# Exemplo de uso
remetente = 'seu_email@gmail.com'
senha = 'sua_senha'
destinatario = 'destinatario@example.com'

# enviar_email_com_anexo('relatorios.zip', destinatario, remetente, senha)
