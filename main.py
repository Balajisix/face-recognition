import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os.path
import face_recognition
import numpy as np

import util

class App:
  def __init__(self):
    # this is the initial window
    self.main_window = tk.Tk()
    self.main_window.geometry("1200x520+350+100")

    # this is for the login button
    self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
    self.login_button_main_window.place(x=750, y=300)

    # this is for the register button
    self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'gray', self.register_new_user, fg='black')
    self.register_new_user_button_main_window.place(x=750, y=400)

    # this is for the web cam label
    self.webcam_label = util.get_img_label(self.main_window)
    self.webcam_label.place(x=10, y=0, width=700, height=500)

    # fit the webcam into the label
    self.add_webcam(self.webcam_label)

    self.db_dir = './db'
    if not os.path.exists(self.db_dir):
      os.mkdir(self.db_dir)


  # a function for adding a web cam fit into the label
  def add_webcam(self, label):
    # this is to not create an object so it's good to check whether the capture is created or not. A good sanity check
    if 'cap' not in self.__dict__:
      self.cap = cv2.VideoCapture(0) # the opencv helps to capture the video from the user

    self._label = label
    self.process_webcam()

  # this function helps to check the frames and sends to the label
  def process_webcam(self):
    ret, frame = self.cap.read()
    self.most_recent_capture_arr = frame

    img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
    # changes the format to Pillow
    self.most_recent_capture_pil = Image.fromarray(img_)

    imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
    self._label.imgtk = imgtk
    self._label.configure(image=imgtk)

    # to make the webcam like a live, calls every 20 seconds
    self._label.after(20, self.process_webcam)

  def login(self):
    unknown_img_path = './.tmp.jpg'
    cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

    try:
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            util.msg_box("Error", "No face detected in captured image.")
            os.remove(unknown_img_path)
            return

        unknown_encoding = unknown_encodings[0]

        matched_user = None
        for filename in os.listdir(self.db_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img_path = os.path.join(self.db_dir, filename)
                known_image = face_recognition.load_image_file(img_path)
                known_encodings = face_recognition.face_encodings(known_image)

                if known_encodings:
                    match = face_recognition.compare_faces([known_encodings[0]], unknown_encoding)[0]
                    if match:
                        matched_user = os.path.splitext(filename)[0]
                        break

        os.remove(unknown_img_path)

        if matched_user:
            util.msg_box("Login Success", f"Welcome, {matched_user}")
        else:
            util.msg_box("Login Failed", "No matching user found.")

    except Exception as e:
        os.remove(unknown_img_path)
        util.msg_box("Error", str(e))

  def register_new_user(self):
    self.register_new_user_window = tk.Toplevel(self.main_window)
    self.register_new_user_window.geometry("1200x520+370+120")

    # accept button
    self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
    self.accept_button_register_new_user_window.place(x=750, y=300)

    # try again button
    self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
    self.try_again_button_register_new_user_window.place(x=750, y=400)

    # a label for webcam
    self.capture_label = util.get_img_label(self.register_new_user_window)
    self.capture_label.place(x=10, y=0, width=700, height=500)

    self.add_img_to_label(self.capture_label)

    self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
    self.entry_text_register_new_user.place(x=750, y=150)

    self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Enter your \nusername to continue: ')
    self.text_label_register_new_user.place(x=750, y=70)

  def try_again_register_new_user(self):
    self.register_new_user_window.destroy()

  def add_img_to_label(self, label):
    imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    self.register_new_user_capture = self.most_recent_capture_arr.copy()

  def start(self):
    self.main_window.mainloop()
    
  def accept_register_new_user(self):
    name = self.entry_text_register_new_user.get(1.0, "end-1c")

    cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

    util.msg_box('Success', 'User registered successfully!!!')

    self.register_new_user_window.destroy()

if __name__ == "__main__":
  app = App()
  app.start()