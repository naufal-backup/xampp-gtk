#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import subprocess
import threading
import webbrowser
import os

class XAMPPControl(Gtk.Window):
    def __init__(self):
        super().__init__(title="XAMPP Control Panel")
        self.set_default_size(600, 500)
        
        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.set_child(vbox)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<b><big>XAMPP Control Panel</big></b>")
        title.set_margin_top(5)
        title.set_margin_bottom(5)
        vbox.append(title)
        
        # Separator
        separator1 = Gtk.Separator()
        separator1.set_margin_top(5)
        separator1.set_margin_bottom(5)
        vbox.append(separator1)
        
        # Service Control Section
        service_frame = Gtk.Frame(label="Service Control")
        service_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        service_box.set_margin_top(10)
        service_box.set_margin_bottom(10)
        service_box.set_margin_start(10)
        service_box.set_margin_end(10)
        service_frame.set_child(service_box)
        
        # All Services buttons
        all_label = Gtk.Label()
        all_label.set_markup("<b>All Services:</b>")
        all_label.set_halign(Gtk.Align.START)
        service_box.append(all_label)
        
        all_btn_box = Gtk.Box(spacing=5)
        all_btn_box.set_margin_top(5)
        all_btn_box.set_margin_bottom(5)
        self.create_button(all_btn_box, "Start All", "start")
        self.create_button(all_btn_box, "Stop All", "stop")
        self.create_button(all_btn_box, "Restart All", "restart")
        self.create_button(all_btn_box, "Reload All", "reload")
        service_box.append(all_btn_box)
        
        separator2 = Gtk.Separator()
        separator2.set_margin_top(5)
        separator2.set_margin_bottom(5)
        service_box.append(separator2)
        
        # Apache buttons
        apache_label = Gtk.Label()
        apache_label.set_markup("<b>Apache:</b>")
        apache_label.set_halign(Gtk.Align.START)
        service_box.append(apache_label)
        
        apache_box = Gtk.Box(spacing=5)
        apache_box.set_margin_top(5)
        apache_box.set_margin_bottom(5)
        self.create_button(apache_box, "Start", "startapache")
        self.create_button(apache_box, "Stop", "stopapache")
        self.create_button(apache_box, "Reload", "reloadapache")
        service_box.append(apache_box)
        
        # MySQL buttons
        mysql_label = Gtk.Label()
        mysql_label.set_markup("<b>MySQL:</b>")
        mysql_label.set_halign(Gtk.Align.START)
        service_box.append(mysql_label)
        
        mysql_box = Gtk.Box(spacing=5)
        mysql_box.set_margin_top(5)
        mysql_box.set_margin_bottom(5)
        self.create_button(mysql_box, "Start", "startmysql")
        self.create_button(mysql_box, "Stop", "stopmysql")
        self.create_button(mysql_box, "Reload", "reloadmysql")
        service_box.append(mysql_box)
        
        # ProFTPD buttons
        ftp_label = Gtk.Label()
        ftp_label.set_markup("<b>ProFTPD:</b>")
        ftp_label.set_halign(Gtk.Align.START)
        service_box.append(ftp_label)
        
        ftp_box = Gtk.Box(spacing=5)
        ftp_box.set_margin_top(5)
        ftp_box.set_margin_bottom(5)
        self.create_button(ftp_box, "Start", "startftp")
        self.create_button(ftp_box, "Stop", "stopftp")
        self.create_button(ftp_box, "Reload", "reloadftp")
        service_box.append(ftp_box)
        
        vbox.append(service_frame)
        
        # Additional Tools Section
        tools_frame = Gtk.Frame(label="Tools")
        tools_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        tools_box.set_margin_top(10)
        tools_box.set_margin_bottom(10)
        tools_box.set_margin_start(10)
        tools_box.set_margin_end(10)
        tools_frame.set_child(tools_box)
        
        tools_btn_box = Gtk.Box(spacing=5)
        self.create_button(tools_btn_box, "Security Check", "security")
        self.create_button(tools_btn_box, "Enable SSL", "enablessl")
        self.create_button(tools_btn_box, "Disable SSL", "disablessl")
        tools_box.append(tools_btn_box)
        
        tools_btn_box2 = Gtk.Box(spacing=5)
        self.create_button(tools_btn_box2, "Backup", "backup")
        self.create_button(tools_btn_box2, "Enable OCI8", "oci8")
        self.create_button(tools_btn_box2, "Control Panel", "panel")
        tools_box.append(tools_btn_box2)
        
        tools_btn_box3 = Gtk.Box(spacing=5)
        manager_btn = Gtk.Button(label="XAMPP Manager GUI")
        manager_btn.connect("clicked", self.on_manager_clicked)
        tools_btn_box3.append(manager_btn)
        manager_btn.set_hexpand(True)
        tools_box.append(tools_btn_box3)
        
        vbox.append(tools_frame)
        
        # Web Access Section
        web_frame = Gtk.Frame(label="Web Access")
        web_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        web_box.set_margin_top(10)
        web_box.set_margin_bottom(10)
        web_box.set_margin_start(10)
        web_box.set_margin_end(10)
        web_frame.set_child(web_box)
        
        web_btn_box = Gtk.Box(spacing=5)
        self.create_web_button(web_btn_box, "Open phpMyAdmin", "http://localhost/phpmyadmin")
        self.create_web_button(web_btn_box, "Open Localhost", "http://localhost")
        self.create_web_button(web_btn_box, "XAMPP Dashboard", "http://localhost/dashboard")
        web_box.append(web_btn_box)
        
        vbox.append(web_frame)
        
        # Output area
        output_frame = Gtk.Frame(label="Output")
        output_scroll = Gtk.ScrolledWindow()
        output_scroll.set_vexpand(True)
        
        self.output_text = Gtk.TextView()
        self.output_text.set_editable(False)
        self.output_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.output_buffer = self.output_text.get_buffer()
        
        output_scroll.set_child(self.output_text)
        output_frame.set_child(output_scroll)
        vbox.append(output_frame)
        
        # Status bar
        self.statusbar = Gtk.Label()
        self.statusbar.set_halign(Gtk.Align.START)
        self.statusbar.set_margin_top(5)
        self.statusbar.set_margin_bottom(5)
        self.statusbar.set_margin_start(5)
        self.statusbar.set_margin_end(5)
        vbox.append(self.statusbar)
        
        self.append_output("XAMPP Control Panel Ready\n")
        self.update_status("Ready")

    def create_button(self, container, label, command):
        btn = Gtk.Button(label=label)
        btn.connect("clicked", self.on_command_clicked, command)
        btn.set_hexpand(True)
        container.append(btn)
        return btn
    
    def create_web_button(self, container, label, url):
        btn = Gtk.Button(label=label)
        btn.connect("clicked", self.on_web_clicked, url)
        btn.set_hexpand(True)
        container.append(btn)
        return btn
    
    def update_status(self, message):
        self.statusbar.set_text(message)

    def append_output(self, text):
        end_iter = self.output_buffer.get_end_iter()
        self.output_buffer.insert(end_iter, text)
        # Auto-scroll to bottom
        mark = self.output_buffer.create_mark(None, end_iter, False)
        self.output_text.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def on_command_clicked(self, widget, command):
        self.update_status(f"Executing: xampp {command}")
        self.append_output(f"\n==> Running: xampp {command}\n")
        
        # Run command in thread to avoid blocking UI
        thread = threading.Thread(target=self.run_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def on_web_clicked(self, widget, url):
        self.update_status(f"Opening: {url}")
        self.append_output(f"\n==> Opening browser: {url}\n")
        try:
            webbrowser.open(url)
            self.append_output(f"✓ Browser opened successfully\n")
        except Exception as e:
            self.append_output(f"✗ Error opening browser: {e}\n")
    
    def on_manager_clicked(self, widget):
        self.update_status("Launching XAMPP Manager GUI")
        self.append_output(f"\n==> Launching XAMPP Manager GUI\n")
        
        # Run manager in thread to avoid blocking UI
        thread = threading.Thread(target=self.run_manager)
        thread.daemon = True
        thread.start()
    
    def run_manager(self):
        try:
            manager_path = "/opt/lampp/manager-linux-x64.run"
            # Check if manager exists
            if not os.path.exists(manager_path):
                GLib.idle_add(self.append_output, f"✗ XAMPP Manager not found at {manager_path}\n")
                GLib.idle_add(self.update_status, "Manager not found")
                return
            
            # Run manager with pkexec for proper permissions
            process = subprocess.Popen(
                ['pkexec', manager_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            GLib.idle_add(self.append_output, f"✓ XAMPP Manager launched successfully\n")
            GLib.idle_add(self.update_status, "Manager launched")
            
        except Exception as e:
            GLib.idle_add(self.append_output, f"✗ Error launching manager: {e}\n")
            GLib.idle_add(self.update_status, "Manager launch failed")

    def run_command(self, command):
        try:
            # Run xampp command with sudo (will prompt for password if needed)
            xampp_path = '/opt/lampp/xampp'
            
            # Check if XAMPP is installed
            if not os.path.exists(xampp_path):
                GLib.idle_add(self.command_error, f"XAMPP not found at {xampp_path}. Please install XAMPP first.", command)
                return
            
            process = subprocess.Popen(
                ['pkexec', xampp_path, command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            # Update UI in main thread
            GLib.idle_add(self.command_finished, stdout, stderr, process.returncode, command)
            
        except Exception as e:
            GLib.idle_add(self.command_error, str(e), command)

    def command_finished(self, stdout, stderr, returncode, command):
        if stdout:
            self.append_output(stdout)
        
        # Filter out egrep warnings and show meaningful errors only
        if stderr:
            # Remove egrep obsolescence warnings
            filtered_errors = '\n'.join([
                line for line in stderr.split('\n') 
                if 'egrep' not in line.lower() and line.strip()
            ])
            if filtered_errors:
                self.append_output(f"Error: {filtered_errors}\n")
        
        if returncode == 0:
            self.append_output(f"✓ Command completed successfully\n")
            self.update_status(f"Success: xampp {command}")
        elif returncode == 126:
            self.append_output(f"✗ Authentication cancelled or permission denied\n")
            self.update_status(f"Cancelled: xampp {command}")
        else:
            self.append_output(f"✗ Command failed with exit code {returncode}\n")
            self.update_status(f"Failed: xampp {command}")
        
        return False

    def command_error(self, error, command):
        self.append_output(f"Error executing command: {error}\n")
        self.update_status(f"Error: {command}")
        return False

def main():
    app = Gtk.Application(application_id="com.naufal.xampp-control")
    
    def on_activate(app):
        win = XAMPPControl()
        win.set_application(app)
        win.present()
    
    app.connect("activate", on_activate)
    app.run(None)

if __name__ == "__main__":
    main()
