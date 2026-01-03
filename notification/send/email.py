import smptplib, os , json
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message['mp3_fid']
        sender_address = os.getenv("GMAIL_ADDRESS")
        sender_password = os.getenv("GMAIL_PASSWORD")
        receiver_address = message['username']
        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is ready for download.")
        msg['Subject'] = 'Your mp3 file is ready'
        msg['From'] = sender_address
        msg['To'] = receiver_address

        session = smptplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()
        print(f"Notification email sent to {receiver_address}")
    except Exception as e:
        print("Failed to send notification email:", e)
        return "failed to send notification email", 500

