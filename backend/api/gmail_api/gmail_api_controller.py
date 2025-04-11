import smtplib 
import threading
import base64
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_credentials() -> Credentials:
    '''
    Função para validar ou criar as credencias token.json para poder utilizar a API do gmail.
    
    '''
    
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            raise (f"Error loading credentials: {str(e)}")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: 
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                prompt='consent', 
                include_granted_scopes='true'
            )

            flow.run_local_server(port=8080)
            creds = flow.credentials
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def send_email_via_gmail_api(sender_email: str, receiver_email: str, subject: str, message: str) -> None:
    '''
    Função para enviar um email via API gmail.
    
    Args:
        sender (str): Email do remetente, mas atualmente não é necessário.
        receiver_email (str): Email do destinatário.
        subject (str): Assunto referente do email.
        message (str): Mensagem que será enviada no email.
    Returns:
        None: A função não retorna nenhum valor.
    Raises:
        Exception: Lança uma exceção se ocorrer algum erro durante a execução.    
    '''
    
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        
        msg = MIMEText(message)
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        
        resultado = service.users().messages().send(
            userId='me',
            body={'raw': raw_msg}
        ).execute()
        
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
    
    
