import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Complex Camera Stream Selector")
        self.geometry("1000x700")

        self.caps = {
            "서라운드 카메라": cv2.VideoCapture(0),
            "좌측 카메라": cv2.VideoCapture(1),
            "우측 카메라": cv2.VideoCapture(2),
            "후방 카메라": cv2.VideoCapture(3)
        }

        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="y", expand=False)

        button_names = ["서라운드 카메라", "좌측 카메라", "우측 카메라", "후방 카메라"]
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name,
                                command=lambda n=name: self.select_camera(n))
            button.pack(pady=10, fill="x", expand=True)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.left_video_label = ttk.Label(self.right_frame)
        self.right_video_label = ttk.Label(self.right_frame)

        self.current_camera = None
        self.is_split_screen = False

        self.update_video()

    def select_camera(self, selected_camera):
        if self.current_camera is None or self.current_camera == selected_camera:
            # If it's the first selection or re-selection of the same camera, show it full screen
            self.current_camera = selected_camera
            self.is_split_screen = False
            self.left_video_label.pack_forget()
            self.right_video_label.pack_forget()
            self.left_video_label.pack(fill="both", expand=True)
        else:
            # If a different camera is selected, split the screen
            self.right_video_label.pack(side="right", fill="both", expand=True)
            self.left_video_label.pack(side="left", fill="both", expand=True)
            self.is_split_screen = True
            self.current_camera = selected_camera

    def update_video(self):
        for label, cam_key in [(self.left_video_label, self.current_camera),
                               (self.right_video_label, self.previous_camera if self.is_split_screen else None)]:
            if cam_key and self.caps[cam_key].isOpened():
                ret, frame = self.caps[cam_key].read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = ImageTk.PhotoImage(Image.fromarray(frame))
                    label.img = img  # to prevent img from being garbage collected
                    label.configure(image=img)
        self.after(33, self.update_video)  # roughly 30 frames per second

    def on_closing(self):
        for cap in self.caps.values():
            cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()