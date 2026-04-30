#!/bin/bash

# XAMPP Control Panel Installer for Linux
# Author: Gemini CLI

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   XAMPP Control Panel Installer     ${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}Silakan jalankan dengan sudo untuk menginstal dependensi dan menyalin file ke /opt${NC}"
  echo "Mencoba menjalankan ulang dengan sudo..."
  exec sudo "$0" "$@"
fi

# Check XAMPP
if [ ! -f "/opt/lampp/xampp" ]; then
    echo -e "${RED}Error: XAMPP tidak ditemukan di /opt/lampp.${NC}"
    echo "Pastikan XAMPP sudah terinstal sebelum menjalankan installer ini."
    exit 1
fi

# Detect Package Manager
if [ -f /etc/debian_version ]; then
    PKG_MANAGER="apt"
elif [ -f /etc/fedora-release ]; then
    PKG_MANAGER="dnf"
elif [ -f /etc/arch-release ]; then
    PKG_MANAGER="pacman"
else
    echo -e "${RED}Sistem operasi tidak didukung otomatis. Silakan instal dependensi secara manual.${NC}"
    PKG_MANAGER="unknown"
fi

echo -e "Distro terdeteksi menggunakan: ${GREEN}$PKG_MANAGER${NC}"

echo -e "\nPilih versi yang ingin diinstal:"
echo "1) XAMPP for Gnome (GTK4)"
echo "2) XAMPP-Qt for KDE (PyQt6)"
echo "3) Keduanya"
read -p "Pilihan [1-3]: " choice

# Dependencies
case $choice in
    1)
        echo -e "${BLUE}Menginstal dependensi GTK4...${NC}"
        if [ "$PKG_MANAGER" == "apt" ]; then
            apt update && apt install -y python3 python3-gi gir1.2-gtk-4.0 policykit-1 wget
        elif [ "$PKG_MANAGER" == "dnf" ]; then
            dnf install -y python3 python3-gobject gtk4 polkit wget
        elif [ "$PKG_MANAGER" == "pacman" ]; then
            pacman -Sy --noconfirm python python-gobject gtk4 polkit wget
        fi
        VERSIONS=("gtk")
        ;;
    2)
        echo -e "${BLUE}Menginstal dependensi PyQt6...${NC}"
        if [ "$PKG_MANAGER" == "apt" ]; then
            apt update && apt install -y python3-pyqt6 policykit-1 wget
        elif [ "$PKG_MANAGER" == "dnf" ]; then
            dnf install -y python3-qt6 polkit wget
        elif [ "$PKG_MANAGER" == "pacman" ]; then
            pacman -Sy --noconfirm python-pyqt6 polkit wget
        fi
        VERSIONS=("qt")
        ;;
    3)
        echo -e "${BLUE}Menginstal semua dependensi...${NC}"
        if [ "$PKG_MANAGER" == "apt" ]; then
            apt update && apt install -y python3 python3-gi gir1.2-gtk-4.0 python3-pyqt6 policykit-1 wget
        elif [ "$PKG_MANAGER" == "dnf" ]; then
            dnf install -y python3 python3-gobject gtk4 python3-qt6 polkit wget
        elif [ "$PKG_MANAGER" == "pacman" ]; then
            pacman -Sy --noconfirm python python-gobject gtk4 python-pyqt6 polkit wget
        fi
        VERSIONS=("gtk" "qt")
        ;;
    *)
        echo "Pilihan tidak valid."
        exit 1
        ;;
esac

# Create directory
INSTALL_DIR="/opt/xampp-gtk"
echo -e "\n${BLUE}Menyiapkan direktori instalasi di $INSTALL_DIR...${NC}"
mkdir -p $INSTALL_DIR
cp xampp.py xampp_qt.py $INSTALL_DIR/
chmod +x $INSTALL_DIR/xampp.py $INSTALL_DIR/xampp_qt.py

# Icon
echo -e "${BLUE}Mengatur icon...${NC}"
ICON_INSTALLED=false

# Try local XAMPP icons first
if [ -f "/opt/lampp/htdocs/dashboard/images/xampp-logo.svg" ]; then
    mkdir -p /usr/share/icons/hicolor/scalable/apps/
    cp /opt/lampp/htdocs/dashboard/images/xampp-logo.svg /usr/share/icons/hicolor/scalable/apps/xampp.svg
    ICON_INSTALLED=true
elif [ -f "/opt/lampp/htdocs/dashboard/images/bitnami-xampp.png" ]; then
    mkdir -p /usr/share/icons/hicolor/48x48/apps/
    cp /opt/lampp/htdocs/dashboard/images/bitnami-xampp.png /usr/share/icons/hicolor/48x48/apps/xampp.png
    ICON_INSTALLED=true
fi

# Download if not found locally
if [ "$ICON_INSTALLED" = false ]; then
    echo "Mendownload icon dari internet..."
    mkdir -p /usr/share/icons/hicolor/scalable/apps/
    wget -q -O /usr/share/icons/hicolor/scalable/apps/xampp.svg https://upload.wikimedia.org/wikipedia/commons/e/ef/XAMPP_logo.svg || \
    wget -q -O /usr/share/icons/hicolor/48x48/apps/xampp.png https://www.apachefriends.org/images/xampp-logo.png
fi

# Desktop Shortcuts
for ver in "${VERSIONS[@]}"; do
    if [ "$ver" == "gtk" ]; then
        NAME="XAMPP Control Panel (Gnome)"
        EXEC="python3 $INSTALL_DIR/xampp.py"
        FILE="/usr/share/applications/com.naufal.xampp-control.desktop"
    else
        NAME="XAMPP Control Panel (KDE)"
        EXEC="python3 $INSTALL_DIR/xampp_qt.py"
        FILE="/usr/share/applications/xampp-qt.desktop"
    fi

    echo -e "Membuat shortcut: ${GREEN}$NAME${NC}"
    cat > $FILE <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$NAME
Comment=Manage XAMPP services
Exec=$EXEC
Icon=xampp
Terminal=false
Categories=Development;
Keywords=xampp;apache;mysql;php;
EOF
done

# Update icon cache
gtk-update-icon-cache /usr/share/icons/hicolor/ || true

echo -e "\n${GREEN}Instalasi selesai!${NC}"
echo "Anda sekarang bisa menemukan XAMPP Control Panel di menu aplikasi."
echo "Jalankan dengan perintah: xampp-gtk (Gnome) atau xampp-qt (KDE)"

# Create symlinks for easier CLI access
ln -sf $INSTALL_DIR/xampp.py /usr/local/bin/xampp-gtk
ln -sf $INSTALL_DIR/xampp_qt.py /usr/local/bin/xampp-qt

echo -e "${BLUE}Selesai.${NC}"
