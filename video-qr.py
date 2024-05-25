import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
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
        self.layout.addWidget(self.info_label)

        self.scan_button = QPushButton("Iniciar escaneo de QR")
        self.scan_button.clicked.connect(self.start_scanning)
        self.layout.addWidget(self.scan_button)

        self.qr_code_data = ""
        self.is_scanning = False

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRScannerWindow()
    window.show()
    sys.exit(app.exec_())
