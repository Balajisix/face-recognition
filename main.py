import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os.path
import face_recognition
import numpy as np
import datetime

import dlib
from scipy.spatial import distance as dist
import imutils

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

    self.log_path = './log.txt'

    # this is for real-time capturing
    self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    self.detector = dlib.get_frontal_face_detector()

  # a function for adding a web cam fit into the label
  def add_webcam(self, label):
    # this is to not create an object so it's good to check whether the capture is created or not. A good sanity check
    if 'cap' not in self.__dict__:
      self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # the opencv helps to capture the video from the user

    self._label = label
    self.process_webcam()

  # this function helps to check the frames and sends to the label
  def process_webcam(self):
    ret, frame = self.cap.read()

    if not ret or frame is None:
        print("Warning: Could not read frame from webcam.")
        self._label.after(20, self.process_webcam)
        return

    self.most_recent_capture_arr = frame.copy()
    img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    self.most_recent_capture_pil = Image.fromarray(img_)

    imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
    self._label.imgtk = imgtk
    self._label.configure(image=imgtk)

    self._label.after(20, self.process_webcam)

  def login(self):
    unknown_img_path = './.tmp.jpg'

    # Capture a few frames for fresh data
    frames = []
    for _ in range(5):
        ret, frame = self.cap.read()
        if ret:
            frames.append(frame)

    if not frames:
        util.msg_box("Error", "Failed to capture image from webcam.")
        return

    selected_frame = frames[-1]
    self.most_recent_capture_arr = selected_frame.copy()

    cv2.imwrite(unknown_img_path, selected_frame)

    try:
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if len(unknown_encodings) == 0:
            util.msg_box("Error", "No face detected in captured image")
            os.remove(unknown_img_path)
            return
        elif len(unknown_encodings) > 1:
            util.msg_box("Security Alert", "Multiple faces detected!")
            os.remove(unknown_img_path)
            return

        unknown_encoding = unknown_encodings[0]

        # Check for blink
        blinked = self.detect_blink(selected_frame, self.predictor, self.detector)
        if not blinked:
            util.msg_box("Security check failed", "No blink detected. Please blink and try again.")
            return

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
            with open(self.log_path, 'a') as f:
                f.write('{}, {}\n'.format(matched_user, datetime.datetime.now()))
        else:
            util.msg_box("Login Failed", "No matching user found.")

    except Exception as e:
        if os.path.exists(unknown_img_path):
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
    if hasattr(self, 'most_recent_capture_arr') and self.most_recent_capture_arr is not None:
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    else:
        util.msg_box("Error", "No webcam frame found.")

  def start(self):
    self.main_window.mainloop()
    
  def accept_register_new_user(self):
    name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()

    if not name:
        util.msg_box("Error", "Please enter a name.")
        return

    # Capture a few frames to ensure it's up-to-date
    frames = []
    for _ in range(5):
        ret, frame = self.cap.read()
        if ret:
            frames.append(frame)
    
    if not frames:
        util.msg_box("Error", "Failed to capture image from webcam.")
        return

    selected_frame = frames[-1]
    self.register_new_user_capture = selected_frame.copy()

    blinked = self.detect_blink(selected_frame, self.predictor, self.detector)
    if not blinked:
        util.msg_box("Security Check Failed", "Please blink to prove you're human.")
        return

    rgb_img = cv2.cvtColor(selected_frame, cv2.COLOR_BGR2RGB)
    new_user_encodings = face_recognition.face_encodings(rgb_img)

    if not new_user_encodings:
        util.msg_box("Error", "No face detected. Please try again.")
        return

    new_encoding = new_user_encodings[0]

    for filename in os.listdir(self.db_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            existing_img_path = os.path.join(self.db_dir, filename)
            existing_image = face_recognition.load_image_file(existing_img_path)
            existing_encodings = face_recognition.face_encodings(existing_image)

            if existing_encodings:
                match = face_recognition.compare_faces([existing_encodings[0]], new_encoding)[0]
                if match:
                    util.msg_box("Already Registered", "Face already registered. Please login instead.")
                    self.register_new_user_window.destroy()
                    return

    cv2.imwrite(os.path.join(self.db_dir, f'{name}.jpg'), selected_frame)
    util.msg_box("Success", "User registered successfully!")
    self.register_new_user_window.destroy()

  # this function help the core logic of eye detection
  def detect_blink(self, frame, predictor, detector, blink_threshold=0.27, consecutive_frames=1):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray)

    if len(rects) == 0:
        print("No face detected")
        return False

    blink_count = 0
    for rect in rects:
        shape = predictor(gray, rect)
        shape = np.array([[p.x, p.y] for p in shape.parts()])
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        def eye_aspect_ratio(eye):
            A = dist.euclidean(eye[1], eye[5])
            B = dist.euclidean(eye[2], eye[4])
            C = dist.euclidean(eye[0], eye[3])
            return (A + B) / (2.0 * C)

        leftEAR = eye_aspect_ratio(left_eye)
        rightEAR = eye_aspect_ratio(right_eye)
        ear = (leftEAR + rightEAR) / 2.0

        print(f"EAR: {ear:.2f}")  # Debug print

        if ear < blink_threshold:
            blink_count += 1
        else:
            blink_count = 0

        if blink_count >= consecutive_frames:
            print("Blink detected!")
            return True

    return False

if __name__ == "__main__":
  app = App()
  app.start()