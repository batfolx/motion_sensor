import smtplib
import datetime
import cv2
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from config import *

server = smtplib.SMTP("smtp.gmail.com", 587)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def init():
    server.starttls()
    server.login(email, password)


def capture_picture() -> list or None:
    """
    Returns the filename of the picture captures
    :return: A string of the filename, or None if something went wrong
    """
    filenames = []
    for i in range(2):
        ret, frame = capture.read()
        if not ret:
            return None
        
        filename = f'{time.time()}.jpg'
        cv2.imwrite(filename, frame)
        try:
            cv2.imshow('frame', frame)
            cv2.waitKey(5000)
        except:
            pass
        filenames.append(filename)
        print(f'wrote {filename} to disk')
    try:
        cv2.destroyAllWindows()
    except:
        pass
    return filenames



def send_text(filename):
    if filename is None:
        print("Could not send picture: Does not exist.")
        return

    now = datetime.datetime.now().strftime('%a, %b %d, %Y %-I:%M %p')
    pic = filename
    msg = MIMEMultipart()
    msg['From'] = "Victor"
    msg['To'] = ', '.join(numbers)
    msg["Subject"] = f"Motion has been detected at {now}."
    body = 'A motion has been detected. See picture attached'
    msg.attach(MIMEText(body, 'plain'))
    for i, f in enumerate(filename):
        with open(f, 'rb') as file:
            print(f'attached {f} to email')
            msg.attach(MIMEImage(file.read(), name=f'{i}.jpg'))

    
    server.sendmail('Dickass@lol.email.LOL!!!', numbers, msg.as_string())
    print("Successfully sent text message!")
