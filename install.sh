#!/bin/bash

# 🎯 Script de Instalación del Sistema de Pentesting Autónomo
# Compatible con Manjaro Linux y sistemas basados en Arch

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que se ejecuta como root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "Este script debe ejecutarse como root"
        echo "Uso: sudo ./install.sh"
        exit 1
    fi
}

# Detectar distribución
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    else
        print_error "No se pudo detectar la distribución"
        exit 1
    fi
    
    print_status "Distribución detectada: $DISTRO $VERSION"
}

# Actualizar sistema
update_system() {
    print_status "Actualizando sistema..."
    
    case $DISTRO in
        "manjaro"|"arch")
            pacman -Syu --noconfirm
            ;;
        "ubuntu"|"debian")
            apt update && apt upgrade -y
            ;;
        "fedora")
            dnf update -y
            ;;
        *)
            print_warning "Distribución no soportada oficialmente: $DISTRO"
            ;;
    esac
    
    print_success "Sistema actualizado"
}

# Instalar dependencias del sistema
install_system_dependencies() {
    print_status "Instalando dependencias del sistema..."
    
    case $DISTRO in
        "manjaro"|"arch")
            # Herramientas básicas
            pacman -S --noconfirm \
                python python-pip \
                git curl wget \
                nmap metasploit nikto gobuster hydra sqlmap \
                aircrack-ng john hashcat \
                wireshark-cli tcpdump netcat socat \
                tor proxychains-ng \
                docker docker-compose \
                virtualbox vagrant \
                openssl \
                base-devel
            
            # Herramientas de BlackArch (si está disponible)
            if pacman -Ss blackarch-keyring &>/dev/null; then
                print_status "Instalando herramientas de BlackArch..."
                pacman -S --noconfirm \
                    setoolkit beef evilginx \
                    veil empire \
                    gophish king-phisher
            fi
            ;;
            
        "ubuntu"|"debian")
            apt install -y \
                python3 python3-pip \
                git curl wget \
                nmap metasploit-framework nikto gobuster hydra sqlmap \
                aircrack-ng john hashcat \
                wireshark-common tcpdump netcat socat \
                tor proxychains4 \
                docker.io docker-compose \
                virtualbox vagrant \
                openssl \
                build-essential
            
            # Añadir repositorio de Kali para más herramientas
            echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" > /etc/apt/sources.list.d/kali.list
            wget -q -O - https://archive.kali.org/archive-key.asc | apt-key add -
            apt update
            
            apt install -y setoolkit beef-xss veil empire || true
            ;;
            
        "fedora")
            dnf install -y \
                python3 python3-pip \
                git curl wget \
                nmap nikto gobuster hydra sqlmap \
                aircrack-ng john \
                wireshark-cli tcpdump nmap-ncat socat \
                tor \
                docker docker-compose \
                VirtualBox vagrant \
                openssl \
                gcc gcc-c++ make
            ;;
    esac
    
    print_success "Dependencias del sistema instaladas"
}

# Configurar Docker
setup_docker() {
    print_status "Configurando Docker..."
    
    # Iniciar y habilitar Docker
    systemctl start docker
    systemctl enable docker
    
    # Añadir usuario actual al grupo docker
    if [ -n "$SUDO_USER" ]; then
        usermod -aG docker $SUDO_USER
        print_success "Usuario $SUDO_USER añadido al grupo docker"
    fi
    
    # Verificar instalación
    if docker --version &>/dev/null; then
        print_success "Docker configurado correctamente"
    else
        print_error "Error configurando Docker"
        exit 1
    fi
}

# Configurar Tor
setup_tor() {
    print_status "Configurando Tor..."
    
    # Crear configuración personalizada
    cat > /etc/tor/torrc.pentest << 'EOF'
# Configuración Tor para pentesting
SocksPort 9050
ControlPort 9051
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
DataDirectory /var/lib/tor
ExitPolicy reject *:*
ExitRelay 0
PublishServerDescriptor 0
EOF
    
    # Configurar proxychains
    if [ -f /etc/proxychains.conf ]; then
        cp /etc/proxychains.conf /etc/proxychains.conf.backup
    elif [ -f /etc/proxychains4.conf ]; then
        cp /etc/proxychains4.conf /etc/proxychains4.conf.backup
    fi
    
    cat > /etc/proxychains4.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 9050
EOF
    
    print_success "Tor configurado"
}

# Instalar dependencias Python
install_python_dependencies() {
    print_status "Instalando dependencias Python..."
    
    # Actualizar pip
    python3 -m pip install --upgrade pip
    
    # Instalar dependencias desde requirements.txt
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -r requirements.txt
    else
        print_error "Archivo requirements.txt no encontrado"
        exit 1
    fi
    
    print_success "Dependencias Python instaladas"
}

# Crear directorios necesarios
create_directories() {
    print_status "Creando estructura de directorios..."
    
    mkdir -p /opt/pentest-system
    mkdir -p /var/log/pentest-system
    mkdir -p /etc/pentest-system
    
    # Copiar archivos del sistema
    cp -r . /opt/pentest-system/
    chown -R root:root /opt/pentest-system
    chmod +x /opt/pentest-system/main.py
    
    # Crear enlace simbólico
    ln -sf /opt/pentest-system/main.py /usr/local/bin/pentest-system
    
    print_success "Directorios creados"
}

# Configurar base de datos
setup_database() {
    print_status "Configurando base de datos..."
    
    # Crear directorio de datos
    mkdir -p /var/lib/pentest-system
    
    # Inicializar base de datos SQLite
    python3 -c "
import sys
sys.path.append('/opt/pentest-system')
from core.database import DatabaseManager
db = DatabaseManager('/var/lib/pentest-system/pentest.db')
db.initialize()
print('Base de datos inicializada')
"
    
    print_success "Base de datos configurada"
}

# Configurar certificados SSL
setup_ssl_certificates() {
    print_status "Generando certificados SSL para phishing..."
    
    mkdir -p /etc/pentest-system/certs
    
    # Generar certificado autofirmado
    openssl req -x509 -newkey rsa:4096 -keyout /etc/pentest-system/certs/key.pem \
        -out /etc/pentest-system/certs/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    chmod 600 /etc/pentest-system/certs/key.pem
    chmod 644 /etc/pentest-system/certs/cert.pem
    
    print_success "Certificados SSL generados"
}

# Configurar servicios systemd
setup_systemd_services() {
    print_status "Configurando servicios systemd..."
    
    # Servicio principal
    cat > /etc/systemd/system/pentest-system.service << 'EOF'
[Unit]
Description=Sistema de Pentesting Autónomo
After=network.target docker.service tor.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/pentest-system
ExecStart=/usr/bin/python3 /opt/pentest-system/main.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Recargar systemd
    systemctl daemon-reload
    
    print_success "Servicios systemd configurados"
}

# Configurar firewall
setup_firewall() {
    print_status "Configurando firewall..."
    
    # Verificar si ufw está disponible
    if command -v ufw &> /dev/null; then
        # Permitir puertos necesarios
        ufw allow 8080/tcp  # Phishing landing pages
        ufw allow 4444/tcp  # Metasploit default
        ufw allow 9050/tcp  # Tor SOCKS
        ufw allow 9051/tcp  # Tor Control
        
        print_success "Firewall configurado (ufw)"
    elif command -v firewall-cmd &> /dev/null; then
        # Configurar firewalld
        firewall-cmd --permanent --add-port=8080/tcp
        firewall-cmd --permanent --add-port=4444/tcp
        firewall-cmd --permanent --add-port=9050/tcp
        firewall-cmd --permanent --add-port=9051/tcp
        firewall-cmd --reload
        
        print_success "Firewall configurado (firewalld)"
    else
        print_warning "No se encontró firewall configurado"
    fi
}

# Crear configuración por defecto
create_default_config() {
    print_status "Creando configuración por defecto..."
    
    cat > /etc/pentest-system/settings.yaml << 'EOF'
# Configuración del Sistema de Pentesting Autónomo

database:
  path: "/var/lib/pentest-system/pentest.db"
  backup_interval: 3600
  max_backups: 10

ai:
  default_provider: "groq"
  max_tokens: 4096
  temperature: 0.7
  timeout: 30

security:
  allowed_networks:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
    - "172.16.0.0/12"
  blocked_networks:
    - "0.0.0.0/8"
    - "127.0.0.0/8"
    - "169.254.0.0/16"
  require_authorization: true
  max_concurrent_scans: 5
  scan_timeout: 3600

tools:
  nmap_path: "/usr/bin/nmap"
  metasploit_path: "/usr/bin/msfconsole"
  nikto_path: "/usr/bin/nikto"
  gobuster_path: "/usr/bin/gobuster"
  aircrack_path: "/usr/bin/aircrack-ng"
  hydra_path: "/usr/bin/hydra"
  sqlmap_path: "/usr/bin/sqlmap"

phishing:
  smtp_server: "localhost"
  smtp_port: 1025
  landing_page_port: 8080
  ssl_cert_path: "/etc/pentest-system/certs/cert.pem"
  ssl_key_path: "/etc/pentest-system/certs/key.pem"

malware:
  output_dir: "/var/lib/pentest-system/payloads"
  encryption_key: "change_me_in_production"
  obfuscation_level: 3

reports:
  output_dir: "/var/lib/pentest-system/reports"
  template_dir: "/opt/pentest-system/reports/templates"
  formats: ["pdf", "html", "markdown"]
  include_screenshots: true
  auto_generate: true

tui:
  theme: "dark"
  refresh_interval: 1000
  max_log_lines: 1000
  enable_animations: true
EOF
    
    print_success "Configuración por defecto creada"
}

# Mostrar información post-instalación
show_post_install_info() {
    print_success "¡Instalación completada!"
    echo
    echo -e "${BLUE}=== INFORMACIÓN POST-INSTALACIÓN ===${NC}"
    echo
    echo "📍 Ubicación del sistema: /opt/pentest-system"
    echo "📊 Base de datos: /var/lib/pentest-system/pentest.db"
    echo "⚙️  Configuración: /etc/pentest-system/settings.yaml"
    echo "📝 Logs: /var/log/pentest-system/"
    echo
    echo -e "${BLUE}=== COMANDOS ÚTILES ===${NC}"
    echo
    echo "🚀 Iniciar sistema TUI:"
    echo "   sudo pentest-system --tui"
    echo
    echo "🤖 Modo autónomo:"
    echo "   sudo pentest-system --target 192.168.1.0/24 --autonomous"
    echo
    echo "🎣 Campaña de phishing:"
    echo "   sudo pentest-system --phishing --target-email victim@example.com"
    echo
    echo "🦠 Generar malware:"
    echo "   sudo pentest-system --malware --malware-type backdoor"
    echo
    echo "🔧 Iniciar como servicio:"
    echo "   sudo systemctl start pentest-system"
    echo "   sudo systemctl enable pentest-system"
    echo
    echo -e "${YELLOW}=== CONFIGURACIÓN ADICIONAL ===${NC}"
    echo
    echo "🔑 Para usar APIs de IA, configura las variables de entorno:"
    echo "   export OPENAI_API_KEY='tu-api-key'"
    echo "   export GROQ_API_KEY='tu-api-key'"
    echo "   export ANTHROPIC_API_KEY='tu-api-key'"
    echo
    echo "🐳 Para usar Docker sin sudo:"
    echo "   Cierra sesión y vuelve a iniciar sesión"
    echo
    echo -e "${RED}=== ADVERTENCIAS IMPORTANTES ===${NC}"
    echo
    echo "⚠️  Este sistema es SOLO para pentesting ético y autorizado"
    echo "⚠️  El uso indebido es responsabilidad del usuario"
    echo "⚠️  Asegúrate de tener autorización antes de usar"
    echo
}

# Función principal
main() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🎯 INSTALADOR DEL SISTEMA DE PENTESTING AUTÓNOMO                         ║
║                                                                              ║
║    ⚠️  SOLO PARA USO ÉTICO Y AUTORIZADO ⚠️                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    check_root
    detect_distro
    
    print_status "Iniciando instalación..."
    
    update_system
    install_system_dependencies
    setup_docker
    setup_tor
    install_python_dependencies
    create_directories
    setup_database
    setup_ssl_certificates
    setup_systemd_services
    setup_firewall
    create_default_config
    
    show_post_install_info
}

# Ejecutar instalación
main "$@"