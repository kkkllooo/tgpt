"""
Configuración global del sistema de pentesting autónomo
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    path: str = "./data/pentest.db"
    backup_interval: int = 3600  # segundos
    max_backups: int = 10

@dataclass
class AIConfig:
    """Configuración de agentes de IA"""
    default_provider: str = "groq"  # API gratuita por defecto
    openai_api_key: str = ""
    groq_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 30

@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    allowed_networks: List[str] = field(default_factory=lambda: [
        "192.168.0.0/16",
        "10.0.0.0/8", 
        "172.16.0.0/12"
    ])
    blocked_networks: List[str] = field(default_factory=lambda: [
        "0.0.0.0/8",
        "127.0.0.0/8",
        "169.254.0.0/16"
    ])
    require_authorization: bool = True
    max_concurrent_scans: int = 5
    scan_timeout: int = 3600

@dataclass
class ToolsConfig:
    """Configuración de herramientas"""
    nmap_path: str = "/usr/bin/nmap"
    metasploit_path: str = "/usr/bin/msfconsole"
    nikto_path: str = "/usr/bin/nikto"
    gobuster_path: str = "/usr/bin/gobuster"
    aircrack_path: str = "/usr/bin/aircrack-ng"
    hydra_path: str = "/usr/bin/hydra"
    sqlmap_path: str = "/usr/bin/sqlmap"
    
    # Herramientas de phishing
    gophish_path: str = "/opt/gophish/gophish"
    set_path: str = "/usr/share/set/setoolkit"
    evilginx_path: str = "/opt/evilginx2/evilginx"
    
    # Herramientas de malware
    veil_path: str = "/usr/share/veil/Veil.py"
    msfvenom_path: str = "/usr/bin/msfvenom"
    empire_path: str = "/opt/Empire/empire"

@dataclass
class PhishingConfig:
    """Configuración de phishing"""
    smtp_server: str = "localhost"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    default_sender: str = "noreply@example.com"
    landing_page_port: int = 8080
    ssl_cert_path: str = "./certs/cert.pem"
    ssl_key_path: str = "./certs/key.pem"

@dataclass
class MalwareConfig:
    """Configuración de generación de malware"""
    output_dir: str = "./payloads"
    encryption_key: str = "default_key_change_me"
    obfuscation_level: int = 3  # 1-5
    persistence_methods: List[str] = field(default_factory=lambda: [
        "registry", "startup", "service"
    ])
    evasion_techniques: List[str] = field(default_factory=lambda: [
        "packing", "encryption", "polymorphism"
    ])

@dataclass
class ReportsConfig:
    """Configuración de reportes"""
    output_dir: str = "./reports"
    template_dir: str = "./reports/templates"
    formats: List[str] = field(default_factory=lambda: ["pdf", "html", "markdown"])
    include_screenshots: bool = True
    auto_generate: bool = True

@dataclass
class TUIConfig:
    """Configuración de interfaz TUI"""
    theme: str = "dark"
    refresh_interval: int = 1000  # milisegundos
    max_log_lines: int = 1000
    enable_animations: bool = True
    key_bindings: Dict[str, str] = field(default_factory=lambda: {
        "quit": "q",
        "help": "h",
        "refresh": "r",
        "menu": "m",
        "settings": "s"
    })

class Settings:
    """Clase principal de configuración del sistema"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or "./config/settings.yaml"
        
        # Configuraciones por defecto
        self.database = DatabaseConfig()
        self.ai = AIConfig()
        self.security = SecurityConfig()
        self.tools = ToolsConfig()
        self.phishing = PhishingConfig()
        self.malware = MalwareConfig()
        self.reports = ReportsConfig()
        self.tui = TUIConfig()
        
        # Cargar configuración desde archivo si existe
        self.load_config()
        
        # Cargar variables de entorno
        self.load_env_vars()
    
    def load_config(self):
        """Carga configuración desde archivo YAML"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                if config_data:
                    self._update_from_dict(config_data)
                    
        except Exception as e:
            print(f"⚠️  Error cargando configuración: {e}")
    
    def load_env_vars(self):
        """Carga configuración desde variables de entorno"""
        # API Keys
        self.ai.openai_api_key = os.getenv("OPENAI_API_KEY", self.ai.openai_api_key)
        self.ai.groq_api_key = os.getenv("GROQ_API_KEY", self.ai.groq_api_key)
        self.ai.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", self.ai.anthropic_api_key)
        self.ai.gemini_api_key = os.getenv("GEMINI_API_KEY", self.ai.gemini_api_key)
        
        # Configuración de phishing
        self.phishing.smtp_username = os.getenv("SMTP_USERNAME", self.phishing.smtp_username)
        self.phishing.smtp_password = os.getenv("SMTP_PASSWORD", self.phishing.smtp_password)
        
        # Configuración de base de datos
        self.database.path = os.getenv("DB_PATH", self.database.path)
    
    def _update_from_dict(self, config_dict: Dict[str, Any]):
        """Actualiza configuración desde diccionario"""
        for section, values in config_dict.items():
            if hasattr(self, section) and isinstance(values, dict):
                config_obj = getattr(self, section)
                for key, value in values.items():
                    if hasattr(config_obj, key):
                        setattr(config_obj, key, value)
    
    def save_config(self):
        """Guarda configuración actual a archivo YAML"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            config_dict = {
                "database": self.database.__dict__,
                "ai": self.ai.__dict__,
                "security": self.security.__dict__,
                "tools": self.tools.__dict__,
                "phishing": self.phishing.__dict__,
                "malware": self.malware.__dict__,
                "reports": self.reports.__dict__,
                "tui": self.tui.__dict__
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
    
    def validate_tools(self) -> Dict[str, bool]:
        """Valida que las herramientas estén instaladas"""
        tools_status = {}
        
        # Herramientas básicas
        basic_tools = {
            "nmap": self.tools.nmap_path,
            "nikto": self.tools.nikto_path,
            "gobuster": self.tools.gobuster_path,
            "hydra": self.tools.hydra_path,
            "sqlmap": self.tools.sqlmap_path
        }
        
        # Herramientas de phishing
        phishing_tools = {
            "gophish": self.tools.gophish_path,
            "setoolkit": self.tools.set_path,
            "evilginx": self.tools.evilginx_path
        }
        
        # Herramientas de malware
        malware_tools = {
            "veil": self.tools.veil_path,
            "msfvenom": self.tools.msfvenom_path,
            "empire": self.tools.empire_path
        }
        
        all_tools = {**basic_tools, **phishing_tools, **malware_tools}
        
        for tool_name, tool_path in all_tools.items():
            tools_status[tool_name] = os.path.exists(tool_path) and os.access(tool_path, os.X_OK)
        
        return tools_status
    
    def get_available_ai_providers(self) -> List[str]:
        """Retorna lista de proveedores de IA disponibles"""
        providers = []
        
        # APIs gratuitas (siempre disponibles)
        providers.extend(["groq", "gemini", "anthropic"])
        
        # APIs con key
        if self.ai.openai_api_key:
            providers.append("openai")
        
        return providers
    
    def create_directories(self):
        """Crea directorios necesarios"""
        directories = [
            os.path.dirname(self.database.path),
            self.reports.output_dir,
            self.reports.template_dir,
            self.malware.output_dir,
            "./logs",
            "./data",
            "./certs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

# Instancia global de configuración
settings = Settings()