import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dotenv
import os
from source.logs import init_log, logging_msg
import datetime


####################################################################################################
####################################################################################################
####################################################################################################

############
### INIT ###
############
def init()->bool:
    log_prefix = '[email | init]'
    try:
        dotenv.load_dotenv('.env', override=True)
        init_log()

        logging_msg(f"{log_prefix} OK")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    

####################################################################################################
####################################################################################################
####################################################################################################

def scan_logs()->str:
    log_prefix = '[email | scan_logs]'
    try:
        logging_msg(f"{log_prefix} START")

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file = f'./logs/{today}.log'
        if not os.path.exists(log_file):
            return f"{log_prefix} No log file for today."

        with open(log_file, 'r') as file:
            lines = file.readlines()

        non_info_logs = [line for line in lines if 'INFO' not in line]
        return ''.join(non_info_logs)
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return ""


def send_email()->bool:
    log_prefix = '[email | send_email]'
    try:
        logging_msg(f"{log_prefix} START")

        email = os.getenv('EMAIL_HOST_USER')
        password = os.getenv('EMAIL_HOST_PASSWORD')
        receiver = os.getenv('RECEIVER_EMAIL')

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = receiver
        msg['Subject'] = f"Logs for {datetime.datetime.now().strftime('%Y-%m-%d')}"

        body = scan_logs()
        if body:
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, receiver, text)
            server.quit()

            logging_msg(f"{log_prefix} OK")
        
            return True
        
        else:
            return False
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'ERROR')
        return False


####################################################################################################
####################################################################################################
####################################################################################################

############
### MAIN ###
############
def main()->bool:
    log_prefix = '[email | main]'
    try:
        if init():
            DEBUG = os.getenv('DEBUG')
            
            if send_email():
                logging_msg(f"{log_prefix} ALL OK", 'WARNING')
            
        logging_msg(f"{log_prefix} END")
        return True
    
    except Exception as e:
        logging_msg(f"{log_prefix} Error: {e}", 'CRITICAL')
        return False