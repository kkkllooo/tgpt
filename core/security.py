"""
Validaciones de seguridad para el sistema de pentesting
"""

import os
import ipaddress
import socket
from typing import List, Dict, Any
from pathlib import Path

class SecurityValidator:
    """Validador de seguridad para operaciones de pentesting"""
    
    def __init__(self):
        self.allowed_networks = [
            "192.168.0.0/16",
            "10.0.0.0/8", 
            "172.16.0.0/12"
        ]
        self.blocked_networks = [
            "0.0.0.0/8",
            "127.0.0.0/8",
            "169.254.0.0/16"
        ]
        
    def validate_environment(self) -> bool:
        """Valida el entorno de ejecución"""
        try:
            # Verificar permisos de root
            if os.geteuid() != 0:
                return False
            
            # Verificar herramientas críticas
            critical_tools = ["nmap", "python3"]
            for tool in critical_tools:
                if not self._command_exists(tool):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def validate_target(self, target: str) -> bool:
        """Valida que el objetivo sea legítimo - VALIDACIONES DESHABILITADAS"""
        # ⚠️ ADVERTENCIA: Validaciones de seguridad deshabilitadas
        # El usuario es responsable del uso ético y legal
        return True
    
    def _command_exists(self, command: str) -> bool:
        """Verifica si un comando existe"""
        try:
            import subprocess
            subprocess.run(["which", command], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _is_allowed_ip(self, ip: str) -> bool:
        """Verifica si una IP está permitida - DESHABILITADO"""
        # Todas las IPs permitidas
        return True
    
    def _is_allowed_network(self, network: str) -> bool:
        """Verifica si una red está permitida - DESHABILITADO"""
        # Todas las redes permitidas
        return True
    
    def _is_valid_domain(self, domain: str) -> bool:
        """Verifica si es un dominio válido"""
        try:
            import re
            pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
            return bool(re.match(pattern, domain))
        except:
            return False
    
    def _is_allowed_domain(self, domain: str) -> bool:
        """Verifica si un dominio está permitido - DESHABILITADO"""
        # Todos los dominios permitidos
        return True