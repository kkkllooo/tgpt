"""
Módulo de evasión y anonimato
Integra Tor, VPNs, proxies y técnicas de evasión avanzadas
"""

import os
import json
import time
import random
import asyncio
import subprocess
import tempfile
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import requests
from stem import Signal
from stem.control import Controller
import socks
import socket

class TorManager:
    """Gestor de red Tor para anonimato"""
    
    def __init__(self, logger):
        self.logger = logger
        self.tor_process = None
        self.control_port = 9051
        self.socks_port = 9050
        self.is_running = False
        self.controller = None
        
    async def start_tor(self) -> bool:
        """Inicia servicio Tor"""
        try:
            # Verificar si Tor ya está corriendo
            if await self._is_tor_running():
                self.logger.info("Tor ya está corriendo")
                self.is_running = True
                return True
            
            # Configuración de Tor
            tor_config = self._generate_tor_config()
            
            # Crear archivo de configuración temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
                f.write(tor_config)
                config_file = f.name
            
            # Iniciar Tor
            self.logger.info("Iniciando servicio Tor...")
            self.tor_process = await asyncio.create_subprocess_exec(
                "tor", "-f", config_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Esperar a que Tor se inicie
            await asyncio.sleep(10)
            
            if await self._is_tor_running():
                self.is_running = True
                self.logger.info("Tor iniciado correctamente")
                
                # Conectar al controlador
                await self._connect_controller()
                
                # Limpiar archivo temporal
                os.unlink(config_file)
                return True
            else:
                self.logger.error("No se pudo iniciar Tor")
                return False
                
        except Exception as e:
            self.logger.error(f"Error iniciando Tor: {e}")
            return False
    
    def _generate_tor_config(self) -> str:
        """Genera configuración de Tor"""
        return f"""
# Configuración Tor para pentesting
SocksPort {self.socks_port}
ControlPort {self.control_port}
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
DataDirectory /tmp/tor_data_{random.randint(1000, 9999)}

# Configuraciones de seguridad
ExitPolicy reject *:*
ExitRelay 0
PublishServerDescriptor 0

# Configuraciones de rendimiento
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 600

# Configuraciones de evasión
UseEntryGuards 1
NumEntryGuards 3
EnforceDistinctSubnets 1

# Configuraciones de bridges (opcional)
# UseBridges 1
# Bridge obfs4 [IP]:[PORT] [FINGERPRINT]

# Logging
Log notice stdout
"""
    
    async def _is_tor_running(self) -> bool:
        """Verifica si Tor está corriendo"""
        try:
            # Intentar conectar al puerto SOCKS
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except:
            return False
    
    async def _connect_controller(self):
        """Conecta al controlador Tor"""
        try:
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate(password="pentesting123")
            self.logger.info("Conectado al controlador Tor")
        except Exception as e:
            self.logger.warning(f"No se pudo conectar al controlador Tor: {e}")
    
    async def new_identity(self) -> bool:
        """Solicita nueva identidad Tor"""
        try:
            if self.controller:
                self.controller.signal(Signal.NEWNYM)
                self.logger.info("Nueva identidad Tor solicitada")
                await asyncio.sleep(5)  # Esperar cambio de circuito
                return True
            else:
                self.logger.warning("Controlador Tor no disponible")
                return False
        except Exception as e:
            self.logger.error(f"Error solicitando nueva identidad: {e}")
            return False
    
    def get_current_ip(self) -> Optional[str]:
        """Obtiene IP actual a través de Tor"""
        try:
            # Configurar proxy SOCKS
            session = requests.Session()
            session.proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            # Obtener IP
            response = session.get('https://httpbin.org/ip', timeout=10)
            ip_data = response.json()
            return ip_data.get('origin')
            
        except Exception as e:
            self.logger.error(f"Error obteniendo IP actual: {e}")
            return None
    
    def configure_system_proxy(self):
        """Configura proxy del sistema para usar Tor"""
        try:
            # Configurar proxy SOCKS para Python
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.socks_port)
            socket.socket = socks.socksocket
            
            self.logger.info("Proxy del sistema configurado para Tor")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configurando proxy del sistema: {e}")
            return False
    
    def stop_tor(self):
        """Detiene servicio Tor"""
        try:
            if self.controller:
                self.controller.close()
            
            if self.tor_process:
                self.tor_process.terminate()
                
            self.is_running = False
            self.logger.info("Servicio Tor detenido")
            
        except Exception as e:
            self.logger.error(f"Error deteniendo Tor: {e}")

class VPNManager:
    """Gestor de conexiones VPN"""
    
    def __init__(self, logger):
        self.logger = logger
        self.active_vpn = None
        self.vpn_configs = {}
    
    async def connect_openvpn(self, config_file: str, credentials: Tuple[str, str] = None) -> bool:
        """Conecta a VPN usando OpenVPN"""
        try:
            cmd = ["sudo", "openvpn", "--config", config_file, "--daemon"]
            
            if credentials:
                # Crear archivo temporal con credenciales
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write(f"{credentials[0]}\n{credentials[1]}\n")
                    auth_file = f.name
                
                cmd.extend(["--auth-user-pass", auth_file])
            
            process = await asyncio.create_subprocess_exec(*cmd)
            await process.wait()
            
            if process.returncode == 0:
                self.active_vpn = "openvpn"
                self.logger.info("Conectado a VPN OpenVPN")
                
                if credentials:
                    os.unlink(auth_file)
                
                return True
            else:
                self.logger.error("Error conectando a VPN OpenVPN")
                return False
                
        except Exception as e:
            self.logger.error(f"Error en conexión VPN: {e}")
            return False
    
    async def connect_wireguard(self, config_file: str) -> bool:
        """Conecta a VPN usando WireGuard"""
        try:
            # Activar interfaz WireGuard
            process = await asyncio.create_subprocess_exec(
                "sudo", "wg-quick", "up", config_file
            )
            await process.wait()
            
            if process.returncode == 0:
                self.active_vpn = "wireguard"
                self.logger.info("Conectado a VPN WireGuard")
                return True
            else:
                self.logger.error("Error conectando a VPN WireGuard")
                return False
                
        except Exception as e:
            self.logger.error(f"Error en conexión WireGuard: {e}")
            return False
    
    async def disconnect_vpn(self):
        """Desconecta VPN activa"""
        try:
            if self.active_vpn == "openvpn":
                await asyncio.create_subprocess_exec("sudo", "killall", "openvpn")
            elif self.active_vpn == "wireguard":
                # Necesitaríamos el nombre de la interfaz
                pass
            
            self.active_vpn = None
            self.logger.info("VPN desconectada")
            
        except Exception as e:
            self.logger.error(f"Error desconectando VPN: {e}")

class ProxyChainManager:
    """Gestor de cadenas de proxies"""
    
    def __init__(self, logger):
        self.logger = logger
        self.proxy_chains = []
        self.current_chain = None
    
    def add_proxy(self, proxy_type: str, host: str, port: int, 
                  username: str = None, password: str = None):
        """Añade proxy a la cadena"""
        proxy = {
            "type": proxy_type,
            "host": host,
            "port": port,
            "username": username,
            "password": password
        }
        self.proxy_chains.append(proxy)
        self.logger.info(f"Proxy añadido: {proxy_type}://{host}:{port}")
    
    def generate_proxychains_config(self) -> str:
        """Genera configuración para proxychains"""
        config = """
# Configuración ProxyChains para pentesting
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
"""
        
        for proxy in self.proxy_chains:
            if proxy["username"] and proxy["password"]:
                config += f"{proxy['type']} {proxy['host']} {proxy['port']} {proxy['username']} {proxy['password']}\n"
            else:
                config += f"{proxy['type']} {proxy['host']} {proxy['port']}\n"
        
        return config
    
    async def test_proxy_chain(self) -> bool:
        """Prueba la cadena de proxies"""
        try:
            # Crear configuración temporal
            config = self.generate_proxychains_config()
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
                f.write(config)
                config_file = f.name
            
            # Probar conexión
            process = await asyncio.create_subprocess_exec(
                "proxychains", "-f", config_file, "curl", "-s", "https://httpbin.org/ip",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            os.unlink(config_file)
            
            if process.returncode == 0:
                self.logger.info("Cadena de proxies funcional")
                return True
            else:
                self.logger.error(f"Error en cadena de proxies: {stderr.decode()}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error probando cadena de proxies: {e}")
            return False

class EvasionManager:
    """Gestor principal de técnicas de evasión"""
    
    def __init__(self, logger):
        self.logger = logger
        self.tor_manager = TorManager(logger)
        self.vpn_manager = VPNManager(logger)
        self.proxy_manager = ProxyChainManager(logger)
        self.evasion_active = False
        self.current_techniques = []
    
    async def initialize_evasion(self, techniques: List[str] = None) -> bool:
        """Inicializa técnicas de evasión"""
        if techniques is None:
            techniques = ["tor", "user_agent_rotation", "timing_randomization"]
        
        success = True
        
        for technique in techniques:
            if technique == "tor":
                if await self.tor_manager.start_tor():
                    self.current_techniques.append("tor")
                    self.logger.info("Evasión Tor activada")
                else:
                    success = False
            
            elif technique == "user_agent_rotation":
                self.current_techniques.append("user_agent_rotation")
                self.logger.info("Rotación de User-Agent activada")
            
            elif technique == "timing_randomization":
                self.current_techniques.append("timing_randomization")
                self.logger.info("Randomización de timing activada")
        
        self.evasion_active = success
        return success
    
    def get_random_user_agent(self) -> str:
        """Retorna User-Agent aleatorio"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
        ]
        return random.choice(user_agents)
    
    def get_random_delay(self, min_delay: float = 1.0, max_delay: float = 5.0) -> float:
        """Retorna delay aleatorio para evasión"""
        if "timing_randomization" in self.current_techniques:
            return random.uniform(min_delay, max_delay)
        return 0
    
    async def execute_with_evasion(self, command: str, use_tor: bool = True) -> Dict[str, Any]:
        """Ejecuta comando con técnicas de evasión"""
        try:
            # Aplicar delay aleatorio
            delay = self.get_random_delay()
            if delay > 0:
                await asyncio.sleep(delay)
            
            # Preparar comando con evasión
            if use_tor and "tor" in self.current_techniques:
                # Usar Tor para el comando
                if self.tor_manager.is_running:
                    # Cambiar identidad antes del comando
                    await self.tor_manager.new_identity()
                    
                    # Ejecutar comando a través de Tor
                    proxified_command = f"proxychains -q {command}"
                    
                    process = await asyncio.create_subprocess_shell(
                        proxified_command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
                    stdout, stderr = await process.communicate()
                    
                    return {
                        "success": process.returncode == 0,
                        "output": stdout.decode('utf-8', errors='ignore'),
                        "error": stderr.decode('utf-8', errors='ignore'),
                        "evasion_used": self.current_techniques
                    }
            
            # Ejecutar comando normal si no hay evasión Tor
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore'),
                "evasion_used": self.current_techniques
            }
            
        except Exception as e:
            self.logger.error(f"Error ejecutando comando con evasión: {e}")
            return {
                "success": False,
                "error": str(e),
                "evasion_used": self.current_techniques
            }
    
    async def rotate_identity(self):
        """Rota identidad completa"""
        try:
            if "tor" in self.current_techniques:
                await self.tor_manager.new_identity()
            
            # Aquí se podrían añadir más técnicas de rotación
            self.logger.info("Identidad rotada")
            
        except Exception as e:
            self.logger.error(f"Error rotando identidad: {e}")
    
    def cleanup(self):
        """Limpia recursos de evasión"""
        try:
            self.tor_manager.stop_tor()
            self.evasion_active = False
            self.current_techniques.clear()
            self.logger.info("Técnicas de evasión desactivadas")
            
        except Exception as e:
            self.logger.error(f"Error limpiando evasión: {e}")
    
    def get_evasion_status(self) -> Dict[str, Any]:
        """Retorna estado actual de evasión"""
        return {
            "active": self.evasion_active,
            "techniques": self.current_techniques,
            "tor_running": self.tor_manager.is_running,
            "current_ip": self.tor_manager.get_current_ip() if self.tor_manager.is_running else None,
            "vpn_active": self.vpn_manager.active_vpn
        }