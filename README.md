# 🎯 Sistema de Pentesting Autónomo con TUI

Un sistema avanzado de pentesting autónomo que utiliza inteligencia artificial para la toma de decisiones y una interfaz TUI (Terminal User Interface) para el control completo del sistema.

## 🚀 Características

- **Interfaz TUI completa**: Control total desde la terminal usando curses
- **Agentes de IA especializados**: Toma de decisiones automática usando APIs gratuitas
- **Ejecución autónoma**: Herramientas de pentesting ejecutadas automáticamente
- **Memoria persistente**: Base de datos SQLite para recordar hallazgos
- **Reportes automáticos**: Generación de reportes en Markdown y PDF
- **Control root**: Ejecución con permisos elevados para pentesting completo

## 🛠️ Herramientas Integradas

### Reconocimiento y Escaneo
- **Nmap**: Escaneo de puertos y red
- **Nikto**: Escaneo de vulnerabilidades web
- **Gobuster**: Enumeración de directorios
- **Masscan**: Escaneo rápido de puertos
- **Amass**: Enumeración de subdominios

### Explotación
- **Metasploit**: Framework de explotación
- **SQLMap**: Inyección SQL automatizada
- **Burp Suite**: Proxy de interceptación web
- **Hydra**: Fuerza bruta de credenciales

### Redes Inalámbricas
- **Aircrack-ng**: Auditoría de redes WiFi
- **Reaver**: Ataques WPS
- **Kismet**: Detector de redes inalámbricas

### Ingeniería Social y Phishing
- **SET (Social Engineer Toolkit)**: Framework de ingeniería social
- **Gophish**: Plataforma de phishing avanzada
- **King Phisher**: Framework de phishing personalizable
- **Evilginx2**: Proxy de phishing 2FA bypass
- **Modlishka**: Proxy de phishing avanzado
- **BeEF**: Browser Exploitation Framework

### Creación de Malware (Solo para Pentesting Ético)
- **Veil**: Generador de payloads evasivos
- **TheFatRat**: Generador de backdoors
- **MSFVenom**: Generador de payloads Metasploit
- **Empire**: Framework post-explotación PowerShell
- **Covenant**: Framework C2 .NET
- **Sliver**: Framework C2 moderno

### Repositorios y Herramientas
- **BlackArch**: Repositorio completo de herramientas pentest
- **Pacman/AUR**: Repositorio completo de herramientas de Arch
- **Kali Tools**: Integración con herramientas de Kali Linux

## 🤖 Agentes de IA

- **Coordinador Principal**: Planificación y delegación de tareas
- **Agente de Reconocimiento**: Análisis de objetivos y estrategias
- **Agente de Explotación**: Selección y ejecución de exploits
- **Agente de Análisis**: Procesamiento de resultados y decisiones
- **Agente de Phishing**: Creación de campañas de phishing personalizadas
- **Agente de Malware**: Generación de payloads evasivos y backdoors
- **Agente de Ingeniería Social**: Análisis psicológico y creación de pretextos

## 📋 Requisitos

### Sistema Base
- **Manjaro Linux** (sistema base recomendado)
- Python 3.8+
- Permisos de root/sudo
- Conexión a internet (APIs de IA)

### Virtualización y Contenedores
- **Docker** y Docker Compose
- **VirtualBox** o **VMware** para máquinas virtuales
- **QEMU/KVM** para virtualización avanzada
- **Vagrant** para gestión de VMs

### Herramientas de Sistema
- **Git** para control de versiones
- **Curl** y **Wget** para descargas
- **OpenSSL** para certificados
- **Nmap**, **Metasploit**, **Aircrack-ng** y otras herramientas de pentesting

## 🚀 Instalación

### Instalación Automática (Recomendada)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/autonomous-pentest-system.git
cd autonomous-pentest-system

# Ejecutar instalador automático
sudo chmod +x install.sh
sudo ./install.sh

# El instalador configurará automáticamente:
# - Dependencias del sistema (nmap, metasploit, etc.)
# - Docker y virtualización
# - Tor y proxychains
# - Herramientas de BlackArch/Kali
# - Certificados SSL
# - Base de datos SQLite
# - Servicios systemd
```

### Instalación Manual

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Instalar herramientas de pentesting
sudo pacman -S nmap metasploit nikto gobuster hydra sqlmap aircrack-ng
sudo pacman -S tor proxychains-ng docker virtualbox

# Configurar servicios
sudo systemctl enable docker tor
sudo systemctl start docker tor

# Ejecutar el sistema
sudo python main.py --tui
```

## 🎮 Uso

### Modo Interactivo TUI
```bash
sudo python main.py --tui
```

### Modo Autónomo
```bash
# Escaneo completo de red
sudo python main.py --target 192.168.1.0/24 --autonomous

# Escaneo web específico
sudo python main.py --target example.com --autonomous --scan-type web

# Escaneo de red con evasión automática
sudo python main.py --target 10.0.0.0/24 --autonomous --scan-type network
```

### Campañas de Phishing
```bash
# Campaña básica
sudo python main.py --phishing --target-email victim@example.com

# Campaña con plantilla específica
sudo python main.py --phishing --target-email victim@company.com --phishing-template linkedin

# Campaña con dominio personalizado
sudo python main.py --phishing --target-email victim@target.com --phishing-domain secure-login.com
```

### Generación de Malware
```bash
# Backdoor básico
sudo python main.py --malware --malware-type backdoor --payload-format exe

# Troyano avanzado
sudo python main.py --malware --malware-type trojan --payload-format py

# Keylogger sigiloso
sudo python main.py --malware --malware-type keylogger --payload-format dll

# Ransomware de demostración
sudo python main.py --malware --malware-type ransomware --payload-format exe
```

### Auto-mejora del Sistema
```bash
# Análisis y mejora manual
sudo python main.py --self-improve

# Aplicar mejoras automáticamente
sudo python main.py --self-improve --auto-apply-improvements

# Mejora continua cada 12 horas
sudo python main.py --continuous-improvement --improvement-interval 12

# Mejora continua con aplicación automática
sudo python main.py --continuous-improvement --auto-apply-improvements
```

### Configuración de Agentes IA
```bash
# Configurar API keys (opcional, usa APIs gratuitas por defecto)
export OPENAI_API_KEY="tu-api-key"
export GROQ_API_KEY="tu-api-key"
export ANTHROPIC_API_KEY="tu-api-key"
export GEMINI_API_KEY="tu-api-key"

# El sistema usará automáticamente Groq (gratuito) si no hay keys configuradas
```

### Uso con Docker y VMs
```bash
# El sistema automáticamente:
# - Crea contenedores Kali Linux para escaneos
# - Usa Tor para todas las operaciones comprometidas
# - Rota identidades automáticamente
# - Aplica técnicas de evasión avanzadas
```

## 📊 Estructura del Proyecto

```
autonomous-pentest-system/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias Python
├── install.sh             # Script de instalación
├── config/
│   ├── __init__.py
│   ├── settings.py        # Configuración global
│   └── ai_config.py       # Configuración de agentes IA
├── core/
│   ├── __init__.py
│   ├── database.py        # Gestión de base de datos
│   ├── logger.py          # Sistema de logging
│   └── security.py        # Validaciones de seguridad
├── agents/
│   ├── __init__.py
│   ├── coordinator.py     # Agente coordinador principal
│   ├── reconnaissance.py  # Agente de reconocimiento
│   ├── exploitation.py    # Agente de explotación
│   └── analysis.py        # Agente de análisis
├── tools/
│   ├── __init__.py
│   ├── nmap_wrapper.py    # Wrapper para Nmap
│   ├── metasploit_wrapper.py # Wrapper para Metasploit
│   ├── nikto_wrapper.py   # Wrapper para Nikto
│   ├── gobuster_wrapper.py # Wrapper para Gobuster
│   └── aircrack_wrapper.py # Wrapper para Aircrack-ng
├── tui/
│   ├── __init__.py
│   ├── main_interface.py  # Interfaz principal TUI
│   ├── dashboard.py       # Dashboard de estado
│   ├── target_manager.py  # Gestión de objetivos
│   ├── results_viewer.py  # Visualizador de resultados
│   └── settings_panel.py  # Panel de configuración
├── reports/
│   ├── __init__.py
│   ├── generator.py       # Generador de reportes
│   ├── templates/         # Plantillas de reportes
│   └── exports/           # Reportes generados
└── tests/
    ├── __init__.py
    ├── test_agents.py     # Tests para agentes
    ├── test_tools.py      # Tests para herramientas
    └── test_tui.py        # Tests para TUI
```

## ⚠️ ADVERTENCIA CRÍTICA DE SEGURIDAD

### 🚨 VALIDACIONES DE SEGURIDAD DESHABILITADAS

**ESTE SISTEMA NO TIENE RESTRICCIONES DE SEGURIDAD ACTIVAS**

- ❌ **Sin validación de objetivos**: Puede atacar cualquier IP, dominio o red
- ❌ **Sin restricciones de red**: Permite ataques a redes públicas y privadas
- ❌ **Sin lista de dominios bloqueados**: Puede atacar sitios gubernamentales, militares, etc.
- ❌ **Sin verificaciones éticas**: No verifica autorización para pentesting

### 🔥 CAPACIDADES DESTRUCTIVAS

- **Ataques automatizados**: Puede ejecutar ataques masivos sin supervisión
- **Generación de malware**: Crea malware real y funcional
- **Campañas de phishing**: Envía emails de phishing reales
- **Explotación automática**: Explota vulnerabilidades automáticamente
- **Evasión avanzada**: Usa Tor y técnicas de evasión para evitar detección

### ⚖️ RESPONSABILIDAD LEGAL

**EL USUARIO ES 100% RESPONSABLE DE:**
- Obtener autorización explícita antes de usar
- Cumplir con todas las leyes locales e internacionales
- No atacar sistemas sin permiso
- No usar para actividades ilegales
- Cualquier daño causado por el uso del sistema

### 🛡️ USO RECOMENDADO

**SOLO usar en:**
- Laboratorios de prueba propios
- Sistemas con autorización explícita por escrito
- Entornos de pentesting autorizados
- Investigación académica con permisos

**NUNCA usar contra:**
- Sistemas sin autorización
- Infraestructura crítica
- Sistemas gubernamentales
- Redes de terceros sin permiso

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ DISCLAIMER CRÍTICO

### 🚨 HERRAMIENTA SIN RESTRICCIONES DE SEGURIDAD

**ESTE SOFTWARE ES UNA HERRAMIENTA DE ATAQUE REAL SIN LIMITACIONES**

Este sistema puede:
- Atacar cualquier objetivo en Internet
- Generar malware funcional
- Ejecutar campañas de phishing reales
- Explotar vulnerabilidades automáticamente
- Evadir sistemas de detección

### 📜 EXENCIÓN DE RESPONSABILIDAD

**LOS DESARROLLADORES NO SE HACEN RESPONSABLES DE:**
- Uso ilegal o no autorizado
- Daños causados a sistemas de terceros
- Violaciones de leyes locales o internacionales
- Consecuencias legales del uso indebido
- Actividades criminales realizadas con esta herramienta

### ⚖️ AVISO LEGAL

El uso de esta herramienta contra sistemas sin autorización explícita es **ILEGAL** en la mayoría de jurisdicciones y puede resultar en:
- Cargos criminales
- Multas significativas
- Tiempo de prisión
- Demandas civiles
- Prohibición de usar computadoras

**ÚSALA BAJO TU PROPIO RIESGO Y RESPONSABILIDAD**