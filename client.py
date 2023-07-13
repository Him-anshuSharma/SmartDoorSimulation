import tkinter as tk
from tkinter import filedialog
import socket
import os
from PIL import Image


def make_beep_sound():
    os.system('afplay /System/Library/Sounds/Glass.aiff')

def open_image(image_path):
    image = Image.open(image_path)
    image.show()

def check_image(image_path):
    root = tk.Tk()
    root.withdraw()

    # Open and display the selected image
    image = Image.open(image_path)
    image.show()

def client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the server IP address and specify the port
    server_ip = socket.gethostname()
    port = 1234

    # Connect to the server
    client_socket.connect((server_ip, port))
    
    # Receive file size from the server
    file_size_str = client_socket.recv(1024).decode()
    
    if file_size_str:
        os.system("clear")
        
        file_size = int(file_size_str)
    
        # Receive the image from the server
        image_data = client_socket.recv(file_size)
        image_path = "intruder_rcv.jpg"
        with open(image_path, 'wb') as file:
            file.write(image_data)
        print("Intruder Detected. Intruder Image saved at:", image_path)
        make_beep_sound()

        root = tk.Tk()
        root.title("Intruder Detected")

        label = tk.Label(root, text="Intruder Detected. Approve or Deny?", padx=20, pady=20)
        label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        def approve():
            # Send the approval to the server
            client_socket.send("Y".encode())
            root.destroy()

        def deny():
            # Send the denial to the server
            client_socket.send("N".encode())
            root.destroy()

        approve_button = tk.Button(button_frame, text="Approve", command=approve)
        approve_button.pack(side=tk.LEFT, padx=10)

        deny_button = tk.Button(button_frame, text="Deny", command=deny)
        deny_button.pack(side=tk.LEFT, padx=10)

        check_image_button = tk.Button(root, text="Check Image", command=lambda: check_image(image_path))
        check_image_button.pack(pady=10)

        root.mainloop()
    
    # Close the connection with the server
    client_socket.close()

if __name__ == '__main__':
    client()
