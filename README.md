# XAMPP Control Panel (GTK & Qt)

Aplikasi GUI berbasis GTK4 dan PyQt6 untuk mengelola XAMPP di Linux dengan antarmuka yang intuitif dan mudah digunakan.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![GTK](https://img.shields.io/badge/GTK-4.0-green.svg)
![Qt](https://img.shields.io/badge/Qt-6-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Deskripsi

XAMPP Control Panel adalah aplikasi desktop yang menyediakan antarmuka grafis untuk mengelola layanan XAMPP (Apache, MySQL, ProFTPD) di Linux. Aplikasi ini menggantikan command line dengan GUI yang user-friendly, memudahkan developer dalam mengelola web server lokal mereka.

**Tersedia dalam 2 versi:**
- **GTK Version** (`xampp.py`) - Native GNOME/GTK interface
- **Qt Version** (`xampp_qt.py`) - Modern Qt6 interface (cross-platform)

## ✨ Fitur

### 🔧 Kontrol Layanan
- **Semua Layanan**: Start, Stop, Restart, dan Reload semua layanan sekaligus
- **Apache**: Kontrol individual untuk web server Apache
- **MySQL**: Manajemen database server MySQL
- **ProFTPD**: Kontrol FTP server

### 🛠️ Tools Tambahan
- **Security Check**: Pemeriksaan keamanan XAMPP
- **Enable/Disable SSL**: Aktifkan atau nonaktifkan SSL
- **Backup**: Backup konfigurasi dan data
- **Enable OCI8**: Aktifkan Oracle Database extension
- **Control Panel**: Akses control panel XAMPP
- **XAMPP Manager GUI**: Luncurkan native XAMPP Manager

### 🌐 Akses Web
Tombol cepat untuk membuka:
- phpMyAdmin
- Localhost
- XAMPP Dashboard

### 📊 Monitoring
- Area output real-time untuk melihat hasil eksekusi perintah
- Status bar untuk menampilkan status operasi terakhir
- Auto-scroll pada output log

## 🚀 Instalasi

### Persyaratan Sistem
- Linux (Ubuntu, Debian, Fedora, atau distro lain)
- Python 3.x
- GTK 3.0 (untuk versi GTK) atau PyQt6 (untuk versi Qt)
- XAMPP terinstal
- PolicyKit (untuk privilege escalation)

### Instalasi Dependensi

#### Versi GTK (xampp.py)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-4.0 policykit-1
```

**Fedora:**
```bash
sudo dnf install python3 python3-gobject gtk4 polkit
```

**Arch Linux:**
```bash
sudo pacman -S python python-gobject gtk4 polkit
```

#### Versi Qt (xampp_qt.py)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pyqt6 policykit-1
```

Atau menggunakan pip:
```bash
pip install PyQt6
```

**Fedora:**
```bash
sudo dnf install python3-qt6 polkit
```

**Arch Linux:**
```bash
sudo pacman -S python-pyqt6 polkit
```

> 💡 **Tip**: Lihat [INSTALL_QT.md](INSTALL_QT.md) untuk panduan lengkap instalasi versi Qt.

### Instalasi XAMPP
Jika belum memiliki XAMPP, download dan install dari [Apache Friends](https://www.apachefriends.org/):

```bash
# Download XAMPP (sesuaikan dengan versi terbaru)
wget https://www.apachefriends.org/xampp-files/8.2.12/xampp-linux-x64-8.2.12-0-installer.run

# Beri permission execute
chmod +x xampp-linux-x64-8.2.12-0-installer.run

# Install XAMPP
sudo ./xampp-linux-x64-8.2.12-0-installer.run
```

## 📖 Cara Penggunaan

### Menjalankan Aplikasi

1. Clone repository:
```bash
git clone https://github.com/naufal453/xampp-gtk.git
cd xampp-gtk
```

2. Jalankan aplikasi:

**Versi GTK:**
```bash
python3 xampp.py
```

**Versi Qt:**
```bash
python3 xampp_qt.py
```

Atau buat executable:
```bash
chmod +x xampp.py xampp_qt.py
./xampp.py      # GTK version
./xampp_qt.py   # Qt version
```

### Penggunaan

1. **Start Layanan**: Klik tombol "Start" pada layanan yang ingin dijalankan
2. **Stop Layanan**: Klik tombol "Stop" untuk menghentikan layanan
3. **Reload Layanan**: Klik "Reload" untuk memuat ulang konfigurasi tanpa restart
4. **Akses Web**: Klik tombol web access untuk membuka browser

**Catatan**: Aplikasi akan meminta password sudo melalui PolicyKit saat menjalankan perintah XAMPP.

## 🔐 Keamanan

Aplikasi menggunakan `pkexec` untuk menjalankan perintah XAMPP dengan privilege yang diperlukan. Sistem akan meminta autentikasi melalui PolicyKit setiap kali menjalankan perintah yang memerlukan akses root.

## 🏗️ Struktur Kode

```python
XAMPPControl (Gtk.Window)
├── Service Control Section
│   ├── All Services (start, stop, restart, reload)
│   ├── Apache Control
│   ├── MySQL Control
│   └── ProFTPD Control
├── Tools Section
│   ├── Security & SSL
│   └── Backup & Configuration
├── Web Access Section
│   └── Quick Links
└── Output & Status
    ├── TextView (output log)
    └── Statusbar
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Untuk berkontribusi:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 TODO

- [ ] Menambahkan indikator status real-time untuk setiap layanan
- [ ] Implementasi dark mode
- [ ] Menambahkan notifikasi desktop
- [ ] Export log ke file
- [ ] Konfigurasi port melalui GUI
- [ ] Monitoring resource usage

## 🐛 Bug Report

Jika menemukan bug, silakan buat issue di [GitHub Issues](https://github.com/naufal453/xampp-gtk/issues) dengan detail:
- Sistem operasi dan versi
- Versi Python
- Versi XAMPP
- Langkah-langkah untuk mereproduksi bug
- Screenshot (jika memungkinkan)

## 📜 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Naufal**
- GitHub: [@naufal453](https://github.com/naufal453)

## 🙏 Acknowledgments

- [XAMPP](https://www.apachefriends.org/) - Cross-platform Apache, MySQL, PHP development environment
- [GTK](https://www.gtk.org/) - The GTK toolkit
- [PyGObject](https://pygobject.readthedocs.io/) - Python bindings for GObject

## 📸 Screenshots

*Coming soon...*

---

⭐ Jika project ini membantu Anda, jangan lupa beri star!
