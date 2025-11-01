import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import os

def send_emails():
    # Email configuration
    sender_email = "[SENDER_EMAIL]"
    sender_password = "[SENDER_PASSWORD]"
    smtp_server = "[SMTP_SERVER]"
    smtp_port = [SMTP_PORT]
    
    # Email content
    subject = "[EMAIL_SUBJECT]"
    body = "[EMAIL_BODY_CONTENT]"
    
    # Attachment files
    attachments = ["[ATTACHMENT1_FILENAME]", "[ATTACHMENT2_FILENAME]", "[ATTACHMENT3_FILENAME]"]
    
    # Load recipients from CSV
    recipients = []
    with open('[CSV_FILENAME]', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  # Check if row is not empty
                recipients.append(row[0])
    
    print("Checking attachments...")
    for attachment in attachments:
        if os.path.exists(attachment):
            print(f"■ Found: {attachment}")
        else:
            print(f"■ Missing: {attachment}")
            return
    
    print(f"■ Loaded {len(recipients)} recipients from [CSV_FILENAME]")
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        print("■ Connected to SMTP server")
        
        print("\nSending emails...")
        successful_sends = 0
        failed_sends = 0
        
        for recipient in recipients:
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                # Attach files
                for attachment_path in attachments:
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
                
                # Send email
                server.send_message(msg)
                print(f"■ Sent email to {recipient}")
                successful_sends += 1
                
            except Exception as e:
                print(f"■ Failed to send to {recipient}: {str(e)}")
                failed_sends += 1
        
        # Close connection
        server.quit()
        
        # Print summary
        print(f"\n=== EMAIL SENDING SUMMARY ===")
        print(f"Successful: {successful_sends}")
        print(f"Failed: {failed_sends}")
        print(f"Total: {len(recipients)}")
        print("Email sending completed!")
        
    except Exception as e:
        print(f"■ SMTP connection failed: {str(e)}")

if __name__ == "__main__":
    send_emails()