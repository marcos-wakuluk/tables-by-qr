import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class QRVideoGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Video Generator")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.file_label = QLabel("Seleccionar archivo base:")
        self.layout.addWidget(self.file_label)

        self.file_button = QPushButton("Seleccionar archivo")
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        self.num_label = QLabel("Cantidad de videos modificados:")
        self.layout.addWidget(self.num_label)

        self.num_input = QLineEdit(self)
        self.num_input.setStyleSheet("border: 2px solid #ccc; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.num_input)

        self.generate_button = QPushButton("Generar QRs")
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; border-radius: 5px; margin-top: 10px;")
        self.generate_button.clicked.connect(self.generate_qrs)
        self.layout.addWidget(self.generate_button)

        self.base_file = ""

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo base", "", "Video Files (*.mp4 *.avi *.mov)", options=options)
        if file_name:
            self.base_file = file_name

    def generate_qrs(self):
        num_videos_str = self.num_input.text()
        try:
            num_videos = int(num_videos_str)
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor ingresa un número válido de videos.")
            return

        if not self.base_file:
            QMessageBox.critical(self, "Error", "Por favor selecciona un archivo base.")
            return

        if num_videos <= 0:
            QMessageBox.critical(self, "Error", "Por favor ingresa una cantidad válida de videos.")
            return

        base_clip = VideoFileClip(self.base_file)
        for i in range(1, num_videos + 1):
            output_path = f"videoMesa{i}.mp4"
            txt_clip = TextClip(f"{i}", fontsize=70, color='black').set_duration(base_clip.duration).set_position(('right', 'top'), relative=True).set_opacity(0.8)
            final_clip = CompositeVideoClip([base_clip, txt_clip])
            final_clip.write_videofile(output_path, fps=24)

            qr = qrcode.make(output_path)
            qr.save(f"QRMesa{i}.png")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRVideoGenerator()
    window.show()
    sys.exit(app.exec_())
