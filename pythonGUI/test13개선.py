import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Camera Stream Selector")
        self.geometry("800x600")

        # 카메라 초기화
        self.caps = {
            "Surround Camera": cv2.VideoCapture(0),
            "Left Camera": cv2.VideoCapture('http://192.168.120.30:8080/video'),
            "Right Camera": cv2.VideoCapture(2),
            "Backup Camera": cv2.VideoCapture(3)
        }

        self.check_cameras()  # 카메라 상태 확인과 필요한 경우 에러 처리

        # 왼쪽 명령 버튼 프레임
        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side="left", fill="both", expand=False)

        # 카메라 선택 버튼 생성
        button_names = ["Surround Camera", "Left Camera", "Right Camera", "Backup Camera"]
        for name in button_names:
            button = ttk.Button(self.left_frame, text=name, command=lambda n=name: self.select_camera(n))
            button.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # 비디오 표시 프레임
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # 비디오 라벨
        self.video_label = ttk.Label(self.right_frame)
        self.video_label.pack(fill="both", expand=True)

        self.current_camera = None

        self.update_video()

    def check_cameras(self):
        remove_list = []
        for key, cap in self.caps.items():
            if not cap.isOpened():
                print(f"Warning: {key} camera did not initialize correctly.")
                remove_list.append(key)
        for key in remove_list:
            del self.caps[key]

    def select_camera(self, selected_camera):
        if selected_camera in self.caps:
            self.current_camera = selected_camera

    def update_video_frame(self, label, camera_name):
        cap = self.caps.get(camera_name)
        if cap and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.putText(frame, camera_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                label.imgtk = img
                label.configure(image=img)

    def update_video(self):
        if self.current_camera:
            self.update_video_frame(self.video_label, self.current_camera)
        self.after(30, self.update_video)  # 화면 갱신 간격을 30ms로 조정

    def on_closing(self):
        for cap in self.caps.values():
            if cap.isOpened():
                cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()