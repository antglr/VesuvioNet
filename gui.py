import sys
import subprocess
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QTabWidget, QMessageBox, QListWidget
)
from PyQt6.QtCore import QDateTime

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.updates_tab = QWidget()
        self.request_tab = QWidget()
        self.donation_tab = QWidget()
        self.communication_tab = QWidget()
        self.my_communication_tab = QWidget()
                
        # Add tabs
        self.tabs.addTab(self.updates_tab, "Updates")
        self.tabs.addTab(self.communication_tab, "Communications")
        self.tabs.addTab(self.request_tab, "Requests")
        self.tabs.addTab(self.my_communication_tab, "My Communication")
        self.tabs.addTab(self.donation_tab, "Donations")

        
        # Set up tabs
        self.setup_updates_tab()
        self.setup_communication_tab()
        self.setup_request_tab()
        self.setup_my_communication_tab()
        self.setup_donation_tab()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
        self.setWindowTitle("VesuvioNet")
        self.resize(500, 400)

    def setup_updates_tab(self):
        layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.run_button = QPushButton("Run Script")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)
        
        self.updates_tab.setLayout(layout)

    def run_script(self):
        try:
            if not os.path.exists('site_check.py'):
                raise FileNotFoundError("The script 'site_check.py' does not exist.")
            result = subprocess.run(['python', 'site_check.py'], capture_output=True, text=True)
            self.output_text.setText(result.stdout)
        except FileNotFoundError as fnf_error:
            self.output_text.setText(f"Error: {fnf_error}")
        except Exception as e:
            self.output_text.setText(f"Error running script: {e}")

    def setup_request_tab(self):
        layout = QVBoxLayout()
        
        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)
        
        self.username_entry = QLineEdit()
        layout.addWidget(self.username_entry)
        
        self.request_label = QLabel("Request:")
        layout.addWidget(self.request_label)
        
        self.request_entry = QTextEdit()
        layout.addWidget(self.request_entry)
        
        self.submit_button = QPushButton("Submit Request")
        self.submit_button.clicked.connect(self.submit_request)
        layout.addWidget(self.submit_button)
        
        self.request_tab.setLayout(layout)

    def submit_request(self):
        username = self.username_entry.text().strip()
        request_text = self.request_entry.toPlainText().strip()
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        if not username or not request_text:
            QMessageBox.warning(self, "Input Error", "Please enter both username and request.")
            return
        
        with open("requests.txt", "a") as file:
            file.write(f"[{timestamp}]\nUsername: {username}\nRequest: {request_text}\n{'-'*30}\n")
        
        QMessageBox.information(self, "Success", "Request submitted!")
        self.username_entry.clear()
        self.request_entry.clear()
        self.load_communications()
        self.load_my_communications()

    def setup_donation_tab(self):
        layout = QVBoxLayout()
        
        donation_text = """<b>Se puoi, contatta direttamente chi ha fatto una richiesta.</b><br>
        Se non puoi, e vuoi comunque contribuire, per favore dona e io reindirizzerò tutte le donazioni alla Croce Rossa.<br>
        <b>Per favore, considera di donare.</b><br>
        <i>Grazie!</i>"""
        
        donation_label = QLabel(donation_text, self)
        donation_label.setWordWrap(True)
        layout.addWidget(donation_label)
        
        self.donation_tab.setLayout(layout)

    def setup_communication_tab(self):
        layout = QVBoxLayout()
        
        self.communication_text = QTextEdit()
        self.communication_text.setReadOnly(True)
        layout.addWidget(self.communication_text)
        
        self.refresh_button = QPushButton("Refresh Requests")
        self.refresh_button.clicked.connect(self.load_communications)
        layout.addWidget(self.refresh_button)
        
        self.communication_tab.setLayout(layout)
        self.load_communications()

    def load_communications(self):
        if not os.path.exists("requests.txt"):
            self.communication_text.setText("No requests found.")
            return
        
        with open("requests.txt", "r") as file:
            self.communication_text.setText(file.read())

    def setup_my_communication_tab(self):
        layout = QVBoxLayout()
        
        self.my_username_label = QLabel("Enter Your Username:")
        layout.addWidget(self.my_username_label)
        
        self.my_username_entry = QLineEdit()
        layout.addWidget(self.my_username_entry)
        
        self.my_requests_list = QListWidget()
        layout.addWidget(self.my_requests_list)
        
        self.load_my_button = QPushButton("Load My Requests")
        self.load_my_button.clicked.connect(self.load_my_communications)
        layout.addWidget(self.load_my_button)
        
        self.delete_button = QPushButton("Delete Selected Request")
        self.delete_button.clicked.connect(self.delete_selected_request)
        layout.addWidget(self.delete_button)
        
        self.my_communication_tab.setLayout(layout)
    
    def load_my_communications(self):
        username = self.my_username_entry.text().strip()
        if not username:
            QMessageBox.warning(self, "Input Error", "Please enter your username.")
            return
        
        if not os.path.exists("requests.txt"):
            self.my_requests_list.clear()
            self.my_requests_list.addItem("No requests found.")
            return
        
        self.my_requests_list.clear()
        with open("requests.txt", "r") as file:
            requests = file.read().split("-"*30)  # Split by request separators
        
        for request in requests:
            match = re.search(r"Username: (\S+)\n", request)
            if match and match.group(1) == username:
                self.my_requests_list.addItem(request.strip())
    
    def delete_selected_request(self):
        selected_item = self.my_requests_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Input Error", "Please select a request to delete.")
            return
        
        request_to_delete = selected_item.text()
        
        with open("requests.txt", "r") as file:
            requests = file.read().split("-"*30)
        
        with open("requests.txt", "w") as file:
            file.writelines([req + "-"*30 for req in requests if req.strip() != request_to_delete])
        
        self.load_my_communications()
        QMessageBox.information(self, "Success", "Selected request has been deleted!")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
