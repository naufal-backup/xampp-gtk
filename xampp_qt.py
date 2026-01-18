#!/usr/bin/env python3

import sys
import os
import subprocess
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QGroupBox, QStatusBar, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon


class CommandThread(QThread):
    """Thread untuk menjalankan command XAMPP tanpa blocking UI"""
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, str)  # returncode, command
    
    def __init__(self, command, xampp_path='/opt/lampp/xampp'):
        super().__init__()
        self.command = command
        self.xampp_path = xampp_path
    
    def run(self):
        try:
            # Check if XAMPP is installed
            if not os.path.exists(self.xampp_path):
                self.error_signal.emit(f"XAMPP not found at {self.xampp_path}. Please install XAMPP first.")
                self.finished_signal.emit(1, self.command)
                return
            
            # Run xampp command with pkexec
            process = subprocess.Popen(
                ['pkexec', self.xampp_path, self.command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            if stdout:
                self.output_signal.emit(stdout)
            
            # Filter out egrep warnings
            if stderr:
                filtered_errors = '\n'.join([
                    line for line in stderr.split('\n') 
                    if 'egrep' not in line.lower() and line.strip()
                ])
                if filtered_errors:
                    self.error_signal.emit(f"Error: {filtered_errors}")
            
            self.finished_signal.emit(process.returncode, self.command)
            
        except Exception as e:
            self.error_signal.emit(f"Error executing command: {str(e)}")
            self.finished_signal.emit(1, self.command)


class ManagerThread(QThread):
    """Thread untuk menjalankan XAMPP Manager GUI"""
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, manager_path='/opt/lampp/manager-linux-x64.run'):
        super().__init__()
        self.manager_path = manager_path
    
    def run(self):
        try:
            # Check if manager exists
            if not os.path.exists(self.manager_path):
                self.error_signal.emit(f"XAMPP Manager not found at {self.manager_path}")
                return
            
            # Run manager with pkexec
            subprocess.Popen(
                ['pkexec', self.manager_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.output_signal.emit("✓ XAMPP Manager launched successfully")
            
        except Exception as e:
            self.error_signal.emit(f"Error launching manager: {str(e)}")


class XAMPPControlQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_thread = None
        
    def init_ui(self):
        self.setWindowTitle("XAMPP Control Panel (Qt)")
        self.setGeometry(100, 100, 700, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("XAMPP Control Panel")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Service Control Section
        service_group = QGroupBox("Service Control")
        service_layout = QVBoxLayout()
        
        # All Services
        all_label = QLabel("All Services:")
        all_label_font = QFont()
        all_label_font.setBold(True)
        all_label.setFont(all_label_font)
        service_layout.addWidget(all_label)
        
        all_btn_layout = QHBoxLayout()
        self.create_button(all_btn_layout, "Start All", "start")
        self.create_button(all_btn_layout, "Stop All", "stop")
        self.create_button(all_btn_layout, "Restart All", "restart")
        self.create_button(all_btn_layout, "Reload All", "reload")
        service_layout.addLayout(all_btn_layout)
        
        # Apache
        apache_label = QLabel("Apache:")
        apache_label.setFont(all_label_font)
        service_layout.addWidget(apache_label)
        
        apache_layout = QHBoxLayout()
        self.create_button(apache_layout, "Start", "startapache")
        self.create_button(apache_layout, "Stop", "stopapache")
        self.create_button(apache_layout, "Reload", "reloadapache")
        service_layout.addLayout(apache_layout)
        
        # MySQL
        mysql_label = QLabel("MySQL:")
        mysql_label.setFont(all_label_font)
        service_layout.addWidget(mysql_label)
        
        mysql_layout = QHBoxLayout()
        self.create_button(mysql_layout, "Start", "startmysql")
        self.create_button(mysql_layout, "Stop", "stopmysql")
        self.create_button(mysql_layout, "Reload", "reloadmysql")
        service_layout.addLayout(mysql_layout)
        
        # ProFTPD
        ftp_label = QLabel("ProFTPD:")
        ftp_label.setFont(all_label_font)
        service_layout.addWidget(ftp_label)
        
        ftp_layout = QHBoxLayout()
        self.create_button(ftp_layout, "Start", "startftp")
        self.create_button(ftp_layout, "Stop", "stopftp")
        self.create_button(ftp_layout, "Reload", "reloadftp")
        service_layout.addLayout(ftp_layout)
        
        service_group.setLayout(service_layout)
        main_layout.addWidget(service_group)
        
        # Tools Section
        tools_group = QGroupBox("Tools")
        tools_layout = QVBoxLayout()
        
        tools_row1 = QHBoxLayout()
        self.create_button(tools_row1, "Security Check", "security")
        self.create_button(tools_row1, "Enable SSL", "enablessl")
        self.create_button(tools_row1, "Disable SSL", "disablessl")
        tools_layout.addLayout(tools_row1)
        
        tools_row2 = QHBoxLayout()
        self.create_button(tools_row2, "Backup", "backup")
        self.create_button(tools_row2, "Enable OCI8", "oci8")
        self.create_button(tools_row2, "Control Panel", "panel")
        tools_layout.addLayout(tools_row2)
        
        tools_row3 = QHBoxLayout()
        manager_btn = QPushButton("XAMPP Manager GUI")
        manager_btn.clicked.connect(self.on_manager_clicked)
        tools_row3.addWidget(manager_btn)
        tools_layout.addLayout(tools_row3)
        
        tools_group.setLayout(tools_layout)
        main_layout.addWidget(tools_group)
        
        # Web Access Section
        web_group = QGroupBox("Web Access")
        web_layout = QHBoxLayout()
        
        self.create_web_button(web_layout, "Open phpMyAdmin", "http://localhost/phpmyadmin")
        self.create_web_button(web_layout, "Open Localhost", "http://localhost")
        self.create_web_button(web_layout, "XAMPP Dashboard", "http://localhost/dashboard")
        
        web_group.setLayout(web_layout)
        main_layout.addWidget(web_group)
        
        # Output area
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
        
        # Initial message
        self.append_output("XAMPP Control Panel Ready\n")
    
    def create_button(self, layout, label, command):
        """Create a command button"""
        btn = QPushButton(label)
        btn.clicked.connect(lambda: self.on_command_clicked(command))
        layout.addWidget(btn)
        return btn
    
    def create_web_button(self, layout, label, url):
        """Create a web access button"""
        btn = QPushButton(label)
        btn.clicked.connect(lambda: self.on_web_clicked(url))
        layout.addWidget(btn)
        return btn
    
    def append_output(self, text):
        """Append text to output area"""
        self.output_text.append(text.rstrip())
        # Auto-scroll to bottom
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_command_clicked(self, command):
        """Handle command button click"""
        self.statusbar.showMessage(f"Executing: xampp {command}")
        self.append_output(f"\n==> Running: xampp {command}")
        
        # Create and start thread
        self.current_thread = CommandThread(command)
        self.current_thread.output_signal.connect(self.append_output)
        self.current_thread.error_signal.connect(self.append_output)
        self.current_thread.finished_signal.connect(self.command_finished)
        self.current_thread.start()
    
    def on_web_clicked(self, url):
        """Handle web button click"""
        self.statusbar.showMessage(f"Opening: {url}")
        self.append_output(f"\n==> Opening browser: {url}")
        try:
            webbrowser.open(url)
            self.append_output("✓ Browser opened successfully")
        except Exception as e:
            self.append_output(f"✗ Error opening browser: {e}")
    
    def on_manager_clicked(self):
        """Handle manager button click"""
        self.statusbar.showMessage("Launching XAMPP Manager GUI")
        self.append_output("\n==> Launching XAMPP Manager GUI")
        
        # Create and start thread
        manager_thread = ManagerThread()
        manager_thread.output_signal.connect(self.append_output)
        manager_thread.error_signal.connect(self.append_output)
        manager_thread.start()
    
    def command_finished(self, returncode, command):
        """Handle command completion"""
        if returncode == 0:
            self.append_output("✓ Command completed successfully")
            self.statusbar.showMessage(f"Success: xampp {command}")
        elif returncode == 126:
            self.append_output("✗ Authentication cancelled or permission denied")
            self.statusbar.showMessage(f"Cancelled: xampp {command}")
        else:
            self.append_output(f"✗ Command failed with exit code {returncode}")
            self.statusbar.showMessage(f"Failed: xampp {command}")


def main():
    app = QApplication(sys.argv)
    
    # Set application style (optional)
    app.setStyle('Fusion')
    
    window = XAMPPControlQt()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
