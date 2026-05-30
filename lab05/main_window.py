import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox)
from PySide6.QtCore import QTimer
import multiprocessing
from lab5.worker import worker_process


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertor Text -> HTML")
        self.resize(650, 450)


        self.input_queue = multiprocessing.Queue()
        self.output_queue = multiprocessing.Queue()
        self.worker = multiprocessing.Process(
            target=worker_process,
            args=(self.input_queue, self.output_queue)
        )
        self.worker.start()


        self.init_ui()


        self.timer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)  # Verifică la fiecare 100ms

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)


        top_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Introdu calea către fișierul text...")
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_file)

        top_layout.addWidget(self.path_input)
        top_layout.addWidget(self.browse_btn)
        main_layout.addLayout(top_layout)


        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Rezultatul HTML va apărea aici...")
        self.text_display.setReadOnly(True)
        main_layout.addWidget(self.text_display)


        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.convert_btn = QPushButton("Convert to HTML (via Worker)")
        self.convert_btn.clicked.connect(self.send_to_worker)

        bottom_layout.addWidget(self.convert_btn)
        main_layout.addLayout(bottom_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Deschide fișier text", "",
                                                   "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.path_input.setText(file_path)

    def send_to_worker(self):
        file_path = self.path_input.text()
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Eroare", "Fișierul specificat nu există!")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.input_queue.put(content)
        except Exception as e:
            QMessageBox.warning(self, "Eroare", f"Nu am putut citi fișierul:\n{e}")

    def check_queue(self):

        while not self.output_queue.empty():
            result = self.output_queue.get()
            self.text_display.setPlainText(result)


            try:
                out_path = self.path_input.text() + ".html"
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(result)
            except:
                pass

    def closeEvent(self, event):

        self.input_queue.put("STOP")
        self.worker.join()
        super().closeEvent(event)