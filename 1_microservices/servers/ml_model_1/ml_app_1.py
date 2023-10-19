import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'QRadio App'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.model = None
        self.video_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create buttons
        upload_model_button = QPushButton('Upload Model', self)
        upload_model_button.setToolTip('Upload a machine learning model')
        upload_model_button.move(20, 20)
        upload_model_button.clicked.connect(self.upload_model)

        select_video_button = QPushButton('Select Video', self)
        select_video_button.setToolTip('Select a video file')
        select_video_button.move(20, 60)
        select_video_button.clicked.connect(self.select_video)

        predict_button = QPushButton('Predict', self)
        predict_button.setToolTip('Make predictions on the selected video')
        predict_button.move(20, 100)
        predict_button.clicked.connect(self.predict)

        # Create label to display predicted video
        self.label = QLabel(self)
        self.label.move(200, 20)
        self.label.resize(400, 400)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(upload_model_button)
        layout.addWidget(select_video_button)
        layout.addWidget(predict_button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.show()

    def upload_model(self):
        # Open file dialog to select model file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Upload Model", "","All Files (*);;H5 Files (*.h5)", options=options)
        if file_name:
            # Load model
            self.model = load_model(file_name)

    def select_video(self):
        # Open file dialog to select video file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select Video", "","All Files (*);;MP4 Files (*.mp4)", options=options)
        if file_name:
            self.video_path = file_name

    def predict(self):
        if self.model is None:
            print('Please upload a model')
            return
        if self.video_path is None:
            print('Please select a video')
            return

        # Open video file
        cap = cv2.VideoCapture(self.video_path)

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('predicted_video.mp4', fourcc, fps, (width, height))

        # Process video frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Preprocess frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224))
            frame = np.expand_dims(frame, axis=0)

            # Make prediction
            prediction = self.model.predict(frame)

            # Postprocess frame
            prediction = np.argmax(prediction)
            frame = cv2.putText(frame, str(prediction), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Write frame to video
            out.write(frame)

        # Release video reader and writer
        cap.release()
        out.release()

        # Display predicted video
        pixmap = QPixmap('predicted_video.mp4')
        self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
