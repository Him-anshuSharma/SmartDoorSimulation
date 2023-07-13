import socket
import cv2
import os
import time
import ssl
import os
from email. message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(file_path):
    # SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'himanshu.personaluse@gmail.com'
    smtp_password = os.environ["EMAIL_PASSWORD"]
    print(f"pass: {smtp_password}")

    # Sender and recipient details
    sender_email = 'himanshu.personaluse@gmail.com'
    recipient_email = 'sharmanshu0103@gmail.com'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Intruder'

    # Attach the file
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        message.attach(part)

    # Create the SMTP connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
        print('Email sent successfully!')


def make_doorbell_sound():
    os.system('afplay bell.aiff')

def server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the local machine name and specify a port
    host = socket.gethostname()
    port = 1234

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(host, port))

    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print("Client connected: {}".format(addr))

    os.system("clear")
    # Receive data from the client
    data = input("Idle doorbell\n")
    if data == 'D':
        print("Doorbell Pressed. Clicking Picture....")
        make_doorbell_sound()

        # Capture an image
        camera_port = 0 
        ramp_frames = 30 
        camera = cv2.VideoCapture(camera_port)
        def get_image():
            _, im = camera.read()
            return im 
        for _ in range(ramp_frames):
            _ = camera.read()
        camera_capture = get_image()

        # Save the image
        image_path = "intruder.jpg"
        cv2.imwrite(image_path, camera_capture)
        del(camera)
        print("Image saved at:", image_path)

        send_email_with_attachment(image_path)

        #send image size
        file_size = os.path.getsize(image_path)
        file_size_str = str(file_size)
        client_socket.send(file_size_str.encode())

        # Send the image to the client
        with open(image_path, 'rb') as file:
            image_data = file.read()
            client_socket.sendall(image_data)


        print("Sent")
        # Receive approval/denial from the client
        approval = client_socket.recv(1024).decode()

        if approval == 'Y':
            print("Approved. Unlocking Door!")
        else:
            print("Denied. Please step back!")
        time.sleep(5)

    # Close the connection with the client
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    server()
