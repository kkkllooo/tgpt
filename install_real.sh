#!/bin/bash
# 🔥 INSTALADOR REAL DE HERRAMIENTAS DE PENTESTING

echo "🔥 INSTALANDO SISTEMA DE PENTESTING REAL"
echo "========================================"

# Verificar root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Ejecuta como root: sudo $0"
    exit 1
fi

# Actualizar sistema
echo "📦 Actualizando sistema..."
apt update && apt upgrade -y

# Instalar Python y dependencias
echo "🐍 Instalando Python..."
apt install -y python3 python3-pip python3-dev

# Instalar herramientas de pentesting REALES
echo "⚔️ Instalando herramientas de pentesting..."

# Herramientas básicas
apt install -y \
    nmap \
    nikto \
    gobuster \
    dirb \
    sqlmap \
    hydra \
    john \
    hashcat \
    aircrack-ng \
    masscan \
    zmap \
    fierce \
    dnsrecon \
    sublist3r \
    wfuzz \
    ffuf \
    whatweb \
    wafw00f \
    enum4linux \
    smbclient \
    nbtscan \
    onesixtyone \
    snmpwalk \
    ike-scan \
    sslyze \
    sslscan \
    testssl.sh

# Instalar Metasploit
echo "💥 Instalando Metasploit Framework..."
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Wordlists
echo "📚 Instalando wordlists..."
apt install -y wordlists
if [ ! -d "/usr/share/wordlists" ]; then
    mkdir -p /usr/share/wordlists
fi

# SecLists
if [ ! -d "/usr/share/wordlists/SecLists" ]; then
    git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/SecLists
fi

# Instalar herramientas adicionales con pip
echo "🐍 Instalando herramientas Python..."
pip3 install \
    shodan \
    censys \
    python-nmap \
    requests \
    beautifulsoup4 \
    paramiko \
    scapy \
    impacket \
    pycryptodome

# Crear directorio de trabajo
mkdir -p /opt/real-pentest
cp real_pentest.py /opt/real-pentest/
chmod +x /opt/real-pentest/real_pentest.py

# Crear enlace simbólico
ln -sf /opt/real-pentest/real_pentest.py /usr/local/bin/real-pentest

# Configurar permisos
chmod +x /usr/local/bin/real-pentest

echo ""
echo "✅ INSTALACIÓN COMPLETADA"
echo "========================="
echo ""
echo "🚀 Para ejecutar:"
echo "   sudo real-pentest"
echo ""
echo "🛠️ Herramientas instaladas:"
echo "   - Nmap (escaneo de puertos)"
echo "   - Nikto (escaneo web)"
echo "   - Gobuster (enumeración directorios)"
echo "   - SQLMap (SQL injection)"
echo "   - Hydra (fuerza bruta)"
echo "   - Metasploit (exploits)"
echo "   - Aircrack-ng (WiFi)"
echo "   - Y muchas más..."
echo ""
echo "📁 Resultados se guardan en /tmp/"
echo ""
echo "⚠️  SOLO PARA USO AUTORIZADO"
echo ""