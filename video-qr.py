import sys
import qrcode
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class QRScannerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escáner de Código QR")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.info_label = QLabel("Esperando escaneo de QR...", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.info_label)

        self.scan_button = QPushButton("Iniciar escaneo de QR")
        self.scan_button.setFont(QFont("Arial", 12))
        self.scan_button.clicked.connect(self.start_scanning)
        self.layout.addWidget(self.scan_button)

        self.generate_qr_button = QPushButton("Generar QR")
        self.generate_qr_button.setFont(QFont("Arial", 12))
        self.generate_qr_button.clicked.connect(self.generate_qr_codes)
        self.layout.addWidget(self.generate_qr_button)

        self.qr_code_data = ""
        self.is_scanning = False

        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
            QLabel {
                color: #333;
                margin: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def start_scanning(self):
        self.is_scanning = True
        self.qr_code_data = ""
        self.info_label.setText("Escaneando...")

    def keyPressEvent(self, event):
        if self.is_scanning:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.is_scanning = False
                self.info_label.setText(f"QR Data: {self.qr_code_data}")
                self.show_qr_info(self.qr_code_data)
            else:
                self.qr_code_data += event.text()

    def show_qr_info(self, qr_data):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Información del QR")
        msg_box.setText(f"Datos del QR: {qr_data}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        self.play_video(qr_data)

    def generate_qr_codes(self):
        number, ok = QInputDialog.getInt(self, "Generar QR", "Cantidad de archivos QR a generar:", min=1)
        if ok:
            for i in range(number):
                mesa_numero = f"Mesa{i + 1}"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(mesa_numero)
                qr.make(fit=True)

                img = qr.make_image(fill='black', back_color='white')
                img.save(f"{mesa_numero}.png")

            QMessageBox.information(self, "Generar QR", f"Se generaron {number} archivos QR.")

    def play_video(self, qr_data):
        video_path = f"{qr_data}.mov"
        video_capture = cv2.VideoCapture(video_path)
        if not video_capture.isOpened():
            QMessageBox.critical(self, "Error", f"No se pudo abrir el video: {video_path}")
            return

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            cv2.imshow('Video Reproducido', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRScannerWindow()
    window.show()
    sys.exit(app.exec_())
