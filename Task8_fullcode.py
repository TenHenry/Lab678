import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import json
import yaml
import xml.etree.ElementTree as ET

# Definicja klasy Worker do operacji asynchronicznych
class Worker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_path, output_path, input_extension, output_extension):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.input_extension = input_extension
        self.output_extension = output_extension

    def run(self):
        try:
            # Odczyt danych z pliku wejściowego
            if self.input_extension == 'json':
                data = self.read_json(self.input_path)
            elif self.input_extension in ['yaml', 'yml']:
                data = self.read_yaml(self.input_path)
            elif self.input_extension == 'xml':
                data = self.read_xml(self.input_path)
            else:
                raise ValueError("Unsupported input file format")

            # Zapis danych do pliku wyjściowego
            if self.output_extension == 'json':
                self.write_json(data, self.output_path)
            elif self.output_extension in ['yaml', 'yml']:
                self.write_yaml(data, self.output_path)
            elif self.output_extension == 'xml':
                self.write_xml(data, self.output_path)
            else:
                raise ValueError("Unsupported output file format")

            self.finished.emit(f"Finished converting {self.input_path} to {self.output_path}")
        except Exception as e:
            self.error.emit(str(e))

    # Funkcje pomocnicze do odczytu i zapisu plików
    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def read_yaml(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def read_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='unicode')

    def write_json(self, data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def write_yaml(self, data, file_path):
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def write_xml(self, data, file_path):
        tree = ET.ElementTree(ET.fromstring(data))
        tree.write(file_path)

# Definicja głównego okna aplikacji
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.input_path = QLineEdit(self)
        self.input_path.setPlaceholderText("Enter path of input file or browse...")
        layout.addWidget(self.input_path)

        self.browse_input = QPushButton("Browse Input File")
        self.browse_input.clicked.connect(self.browse_input_file)
        layout.addWidget(self.browse_input)
        
        self.output_path = QLineEdit(self)
        self.output_path.setPlaceholderText("Enter path of output file or browse...")
        layout.addWidget(self.output_path)

        self.browse_output = QPushButton("Browse Output File")
        self.browse_output.clicked.connect(self.browse_output_file)
        layout.addWidget(self.browse_output)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_files)
        layout.addWidget(self.convert_button)
        
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)")
        if filename:
            self.input_path.setText(filename)

    def browse_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)")
        if filename:
            self.output_path.setText(filename)

    def convert_files(self):
        input_path = self.input_path.text()
        output_path = self.output_path.text()
        input_extension = input_path.split('.')[-1]
        output_extension = output_path.split('.')[-1]
        self.worker = Worker(input_path, output_path, input_extension, output_extension)
        self.worker.finished.connect(self.update_status)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def show_error(self, message):
        self.status_label.setText(f"Error: {message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
