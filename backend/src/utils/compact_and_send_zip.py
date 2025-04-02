import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def zip_markdown_files(database_name: str, zip_name_file: str) -> None:
    '''
    Transforma os arquivos zips em markdowns para que possam ser enviados via email.
    
    :param outputFilename: Nome do arquivo zip que será gerado
    :type: str
    :param folderPath: Nome do caminho para os arquivos markdowns
    :type: str
    '''
    try:
        folderPath = f'./relatorio/markdowns/{database_name}'
        
        if not os.path.exists(folderPath):
            raise Exception(f'Pasta {folderPath} não existe')
        
        output_dir = './relatorio/markdowns/zip_temp_files'
        os.makedirs(output_dir, exist_ok=True)
        
        if not zip_name_file:
            zip_name_file = f'{database_name}.zip'
        
        outputFilename = os.path.join(output_dir, zip_name_file)
        
        with zipfile.ZipFile(outputFilename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            root_name = os.path.basename(folderPath.rstrip(os.sep))  
            for root, dirs, files in os.walk(folderPath):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith('.zip'):
                        continue
                    if not os.path.isfile(file_path):
                        continue
                    arcname = os.path.relpath(file_path, os.path.dirname(folderPath))
                    zipf.write(file_path, arcname)
                    
        return {'Success': True}
    except Exception as e:
        return {'Success': False, 'Error': f'Ocorreu um erro ao tentar compactar a pasta contendo os relatórios markdown: {e}' }


def send_email_zip(arquivo_zip, destinatario_email, remetente_email, senha_remetente):
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
        server = smtplib.SMTP('smtp.uem.br', 25)
        server.starttls()
        # server.login(remetente_email, senha_remetente)
        text = msg.as_string()
        server.sendmail(remetente_email, destinatario_email, text)
        server.quit()
        print(f'Email enviado com sucesso para {destinatario_email}')
    except Exception as e:
        print(f'Erro ao enviar o email: {e}')

