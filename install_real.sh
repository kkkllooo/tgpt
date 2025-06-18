#!/bin/bash
# 🔥 INSTALADOR REAL DE HERRAMIENTAS DE PENTESTING - ARCH LINUX + BLACKARCH

echo "🔥 INSTALANDO SISTEMA DE PENTESTING REAL - ARCH LINUX"
echo "====================================================="

# Verificar root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Ejecuta como root: sudo $0"
    exit 1
fi

# Detectar distribución
if command -v pacman &> /dev/null; then
    DISTRO="arch"
    echo "🐧 Detectado: Arch Linux"
elif command -v apt &> /dev/null; then
    DISTRO="debian"
    echo "🐧 Detectado: Debian/Ubuntu"
else
    echo "❌ Distribución no soportada"
    exit 1
fi

if [ "$DISTRO" = "arch" ]; then
    # ARCH LINUX + BLACKARCH
    echo "📦 Actualizando sistema Arch..."
    pacman -Syu --noconfirm
    
    # Instalar dependencias básicas
    echo "🔧 Instalando dependencias básicas..."
    pacman -S --noconfirm base-devel git curl wget python python-pip

    # Agregar repositorio BlackArch
    echo "🖤 Agregando repositorio BlackArch..."
    curl -O https://blackarch.org/strap.sh
    chmod +x strap.sh
    ./strap.sh
    
    # Actualizar con BlackArch
    echo "🖤 Actualizando con BlackArch..."
    pacman -Syu --noconfirm
    
    # Instalar herramientas de BlackArch
    echo "⚔️ Instalando herramientas de BlackArch..."
    pacman -S --noconfirm \
        blackarch-scanner \
        blackarch-webapp \
        blackarch-exploitation \
        blackarch-networking \
        blackarch-wireless \
        blackarch-forensic \
        blackarch-crypto \
        blackarch-backdoor \
        blackarch-malware \
        blackarch-reversing \
        blackarch-social \
        blackarch-misc
    
    # Herramientas específicas principales
    echo "🛠️ Instalando herramientas principales..."
    pacman -S --noconfirm \
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
        net-snmp \
        ike-scan \
        sslyze \
        sslscan \
        testssl.sh \
        metasploit \
        burpsuite \
        wireshark-qt \
        tcpdump \
        netcat \
        socat \
        proxychains-ng \
        tor \
        openvpn \
        stunnel \
        ncrack \
        medusa \
        patator \
        thc-hydra \
        crunch \
        cewl \
        maltego \
        recon-ng \
        theHarvester \
        shodan \
        amass \
        subfinder \
        assetfinder \
        httprobe \
        waybackurls \
        gau \
        nuclei \
        httpx \
        dnsx \
        naabu \
        chaos-client \
        shuffledns \
        puredns \
        massdns \
        altdns \
        dnsgen \
        gotator \
        anew \
        unfurl \
        qsreplace \
        freq \
        hakrawler \
        gospider \
        katana \
        gf \
        meg \
        hakcheckurl \
        haklistgen \
        hakrevdns \
        haktldextract \
        haktrails \
        interactsh-client \
        notify \
        dalfox \
        xss-hunter \
        sqlmap \
        commix \
        nosqlmap \
        xxeinjector \
        ssti-scanner \
        ldapdomaindump \
        bloodhound \
        neo4j \
        crackmapexec \
        impacket \
        responder \
        mitm6 \
        ntlmrelayx \
        secretsdump \
        mimikatz \
        powersploit \
        empire \
        covenant \
        sliver \
        merlin \
        mythic \
        cobalt-strike \
        armitage \
        beef \
        social-engineer-toolkit \
        king-phisher \
        gophish \
        evilginx2 \
        modlishka \
        bettercap \
        ettercap \
        mitmproxy \
        zaproxy \
        w3af \
        skipfish \
        arachni \
        wpscan \
        joomscan \
        droopescan \
        cmsmap \
        wig \
        builtwith \
        webtech \
        retire \
        vulners-scanner \
        searchsploit \
        exploit-db \
        linux-exploit-suggester \
        windows-exploit-suggester \
        privilege-escalation-awesome-scripts-suite \
        linpeas \
        winpeas \
        pspy \
        gtfobins \
        lolbas \
        payloadsallthethings \
        seclist \
        fuzzdb \
        dirb-wordlists \
        wfuzz-wordlists

    # Instalar herramientas AUR (si yay está disponible)
    if command -v yay &> /dev/null; then
        echo "📦 Instalando herramientas AUR..."
        yay -S --noconfirm \
            burpsuite-pro \
            cobalt-strike \
            metasploit-pro \
            nessus \
            openvas \
            nexpose \
            rapid7-insight \
            qualys-vmdr \
            tenable-nessus \
            greenbone-vulnerability-manager \
            nuclei-templates \
            jaeles \
            x8 \
            arjun \
            paramspider \
            linkfinder \
            secretfinder \
            jsparser \
            relative-url-extractor \
            subjs \
            getjs \
            xnlinkfinder \
            burp-extensions \
            turbo-intruder \
            param-miner \
            backslash-powered-scanner \
            collaborator-everywhere \
            active-scan-plus-plus \
            autorize \
            bambdas \
            co2 \
            csrf-scanner \
            distribute-damage \
            error-message-checks \
            freddy \
            hackvertor \
            http-request-smuggler \
            j2ee-scan \
            java-deserialization-scanner \
            json-web-tokens \
            param-miner \
            reflected-parameters \
            retire-js \
            software-vulnerability-scanner \
            taborator \
            upload-scanner \
            wsdler \
            xss-validator
    fi

    # Wordlists
    echo "📚 Instalando wordlists..."
    pacman -S --noconfirm wordlists
    
else
    # DEBIAN/UBUNTU (código original)
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
fi

# Crear directorios comunes
if [ ! -d "/usr/share/wordlists" ]; then
    mkdir -p /usr/share/wordlists
fi

# SecLists
if [ ! -d "/usr/share/wordlists/SecLists" ]; then
    echo "📚 Clonando SecLists..."
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
cp natural_pentest.py /opt/real-pentest/
chmod +x /opt/real-pentest/real_pentest.py
chmod +x /opt/real-pentest/natural_pentest.py

# Crear enlaces simbólicos
ln -sf /opt/real-pentest/real_pentest.py /usr/local/bin/real-pentest
ln -sf /opt/real-pentest/natural_pentest.py /usr/local/bin/pentest

# Configurar permisos
chmod +x /usr/local/bin/real-pentest
chmod +x /usr/local/bin/pentest

echo ""
echo "✅ INSTALACIÓN COMPLETADA"
echo "========================="
echo ""
echo "🚀 Para ejecutar:"
echo "   sudo pentest          # Lenguaje natural"
echo "   sudo real-pentest     # Menú tradicional"
echo ""
echo "💬 LENGUAJE NATURAL - Ejemplos:"
echo "   escanear google.com"
echo "   atacar 192.168.1.1 con fuerza bruta"
echo "   pentesting completo de example.com"
echo "   generar payload reverse shell"
echo "   cmd: nmap -sS target.com"
echo ""
echo "🛠️ Herramientas instaladas:"
if [ "$DISTRO" = "arch" ]; then
    echo "   - BlackArch completo (2000+ herramientas)"
    echo "   - Todos los grupos de BlackArch"
    echo "   - Herramientas AUR adicionales"
fi
echo "   - Nmap, Nikto, Gobuster, SQLMap"
echo "   - Hydra, John, Hashcat, Metasploit"
echo "   - Aircrack-ng, Burp Suite, Wireshark"
echo "   - Nuclei, FFUF, Amass, Subfinder"
echo "   - Y 100+ herramientas más..."
echo ""
echo "📁 Resultados se guardan en /tmp/"
echo ""
echo "⚠️  SOLO PARA USO AUTORIZADO"
echo ""