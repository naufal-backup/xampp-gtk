#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import threading
import webbrowser

class XAMPPControl(Gtk.Window):
    def __init__(self):
        super().__init__(title="XAMPP Control Panel")
        self.set_border_width(10)
        self.set_default_size(600, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<b><big>XAMPP Control Panel</big></b>")
        vbox.pack_start(title, False, False, 5)
        
        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 5)
        
        # Service Control Section
        service_frame = Gtk.Frame(label="Service Control")
        service_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        service_box.set_border_width(10)
        service_frame.add(service_box)
        
        # All Services buttons
        all_label = Gtk.Label()
        all_label.set_markup("<b>All Services:</b>")
        all_label.set_halign(Gtk.Align.START)
        service_box.pack_start(all_label, False, False, 0)
        
        all_btn_box = Gtk.Box(spacing=5)
        self.create_button(all_btn_box, "Start All", "start")
        self.create_button(all_btn_box, "Stop All", "stop")
        self.create_button(all_btn_box, "Restart All", "restart")
        self.create_button(all_btn_box, "Reload All", "reload")
        service_box.pack_start(all_btn_box, False, False, 5)
        
        service_box.pack_start(Gtk.Separator(), False, False, 5)
        
        # Apache buttons
        apache_label = Gtk.Label()
        apache_label.set_markup("<b>Apache:</b>")
        apache_label.set_halign(Gtk.Align.START)
        service_box.pack_start(apache_label, False, False, 0)
        
        apache_box = Gtk.Box(spacing=5)
        self.create_button(apache_box, "Start", "startapache")
        self.create_button(apache_box, "Stop", "stopapache")
        self.create_button(apache_box, "Reload", "reloadapache")
        service_box.pack_start(apache_box, False, False, 5)
        
        # MySQL buttons
        mysql_label = Gtk.Label()
        mysql_label.set_markup("<b>MySQL:</b>")
        mysql_label.set_halign(Gtk.Align.START)
        service_box.pack_start(mysql_label, False, False, 0)
        
        mysql_box = Gtk.Box(spacing=5)
        self.create_button(mysql_box, "Start", "startmysql")
        self.create_button(mysql_box, "Stop", "stopmysql")
        self.create_button(mysql_box, "Reload", "reloadmysql")
        service_box.pack_start(mysql_box, False, False, 5)
        
        # ProFTPD buttons
        ftp_label = Gtk.Label()
        ftp_label.set_markup("<b>ProFTPD:</b>")
        ftp_label.set_halign(Gtk.Align.START)
        service_box.pack_start(ftp_label, False, False, 0)
        
        ftp_box = Gtk.Box(spacing=5)
        self.create_button(ftp_box, "Start", "startftp")
        self.create_button(ftp_box, "Stop", "stopftp")
        self.create_button(ftp_box, "Reload", "reloadftp")
        service_box.pack_start(ftp_box, False, False, 5)
        
        vbox.pack_start(service_frame, False, False, 0)
        
        # Additional Tools Section
        tools_frame = Gtk.Frame(label="Tools")
        tools_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        tools_box.set_border_width(10)
        tools_frame.add(tools_box)
        
        tools_btn_box = Gtk.Box(spacing=5)
        self.create_button(tools_btn_box, "Security Check", "security")
        self.create_button(tools_btn_box, "Enable SSL", "enablessl")
        self.create_button(tools_btn_box, "Disable SSL", "disablessl")
        tools_box.pack_start(tools_btn_box, False, False, 0)
        
        tools_btn_box2 = Gtk.Box(spacing=5)
        self.create_button(tools_btn_box2, "Backup", "backup")
        self.create_button(tools_btn_box2, "Enable OCI8", "oci8")
        self.create_button(tools_btn_box2, "Control Panel", "panel")
        tools_box.pack_start(tools_btn_box2, False, False, 0)
        
        vbox.pack_start(tools_frame, False, False, 0)
        
        # Web Access Section
        web_frame = Gtk.Frame(label="Web Access")
        web_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        web_box.set_border_width(10)
        web_frame.add(web_box)
        
        web_btn_box = Gtk.Box(spacing=5)
        self.create_web_button(web_btn_box, "Open phpMyAdmin", "http://localhost/phpmyadmin")
        self.create_web_button(web_btn_box, "Open Localhost", "http://localhost")
        self.create_web_button(web_btn_box, "XAMPP Dashboard", "http://localhost/dashboard")
        web_box.pack_start(web_btn_box, False, False, 0)
        
        vbox.pack_start(web_frame, False, False, 0)
        
        # Output area
        output_frame = Gtk.Frame(label="Output")
        output_scroll = Gtk.ScrolledWindow()
        output_scroll.set_vexpand(True)
        
        self.output_text = Gtk.TextView()
        self.output_text.set_editable(False)
        self.output_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.output_buffer = self.output_text.get_buffer()
        
        output_scroll.add(self.output_text)
        output_frame.add(output_scroll)
        vbox.pack_start(output_frame, True, True, 0)
        
        # Status bar
        self.statusbar = Gtk.Statusbar()
        self.context_id = self.statusbar.get_context_id("xampp-status")
        vbox.pack_start(self.statusbar, False, False, 0)
        
        self.append_output("XAMPP Control Panel Ready\n")
        self.statusbar.push(self.context_id, "Ready")

    def create_button(self, container, label, command):
        btn = Gtk.Button(label=label)
        btn.connect("clicked", self.on_command_clicked, command)
        container.pack_start(btn, True, True, 0)
        return btn
    
    def create_web_button(self, container, label, url):
        btn = Gtk.Button(label=label)
        btn.connect("clicked", self.on_web_clicked, url)
        container.pack_start(btn, True, True, 0)
        return btn

    def append_output(self, text):
        end_iter = self.output_buffer.get_end_iter()
        self.output_buffer.insert(end_iter, text)
        # Auto-scroll to bottom
        mark = self.output_buffer.create_mark(None, end_iter, False)
        self.output_text.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def on_command_clicked(self, widget, command):
        self.statusbar.push(self.context_id, f"Executing: xampp {command}")
        self.append_output(f"\n==> Running: xampp {command}\n")
        
        # Run command in thread to avoid blocking UI
        thread = threading.Thread(target=self.run_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def on_web_clicked(self, widget, url):
        self.statusbar.push(self.context_id, f"Opening: {url}")
        self.append_output(f"\n==> Opening browser: {url}\n")
        try:
            webbrowser.open(url)
            self.append_output(f"✓ Browser opened successfully\n")
        except Exception as e:
            self.append_output(f"✗ Error opening browser: {e}\n")

    def run_command(self, command):
        try:
            # Run xampp command with sudo (will prompt for password if needed)
            process = subprocess.Popen(
                ['pkexec', 'xampp', command],
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
            self.statusbar.push(self.context_id, f"Success: xampp {command}")
        elif returncode == 126:
            self.append_output(f"✗ Authentication cancelled or permission denied\n")
            self.statusbar.push(self.context_id, f"Cancelled: xampp {command}")
        else:
            self.append_output(f"✗ Command failed with exit code {returncode}\n")
            self.statusbar.push(self.context_id, f"Failed: xampp {command}")
        
        return False

    def command_error(self, error, command):
        self.append_output(f"Error executing command: {error}\n")
        self.statusbar.push(self.context_id, f"Error: {command}")
        return False

def main():
    win = XAMPPControl()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
