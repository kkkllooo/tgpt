"""
Módulo de virtualización y contenedores
Gestiona Docker, VMs y entornos aislados para pentesting
"""

import os
import json
import asyncio
import subprocess
import tempfile
from typing import Dict, List, Optional, Any
from pathlib import Path
import docker
from docker.errors import DockerException

class DockerManager:
    """Gestor de contenedores Docker para pentesting"""
    
    def __init__(self, logger):
        self.logger = logger
        self.client = None
        self.containers = {}
        self.networks = {}
        
    async def initialize(self):
        """Inicializa el cliente Docker"""
        try:
            # Verificar si Docker está corriendo
            if not await self._is_docker_running():
                self.logger.info("Docker no está corriendo, intentando iniciar...")
                await self._start_docker_daemon()
            
            self.client = docker.from_env()
            self.logger.info("Cliente Docker inicializado correctamente")
            return True
            
        except DockerException as e:
            self.logger.error(f"Error inicializando Docker: {e}")
            return False
    
    async def _is_docker_running(self) -> bool:
        """Verifica si Docker daemon está corriendo"""
        try:
            result = await asyncio.create_subprocess_exec(
                "docker", "info",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            return result.returncode == 0
        except:
            return False
    
    async def _start_docker_daemon(self):
        """Inicia Docker daemon si no está corriendo"""
        try:
            # Intentar iniciar dockerd en background
            process = await asyncio.create_subprocess_exec(
                "sudo", "dockerd",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Esperar un poco para que se inicie
            await asyncio.sleep(5)
            
            if await self._is_docker_running():
                self.logger.info("Docker daemon iniciado correctamente")
            else:
                self.logger.warning("No se pudo iniciar Docker daemon automáticamente")
                
        except Exception as e:
            self.logger.error(f"Error iniciando Docker daemon: {e}")
    
    async def create_kali_container(self, name: str = "kali-pentest") -> Optional[str]:
        """Crea un contenedor Kali Linux para pentesting"""
        try:
            # Dockerfile para Kali con herramientas
            dockerfile_content = """
FROM kalilinux/kali-rolling

# Actualizar sistema
RUN apt-get update && apt-get upgrade -y

# Instalar herramientas básicas de pentesting
RUN apt-get install -y \\
    nmap \\
    metasploit-framework \\
    nikto \\
    gobuster \\
    hydra \\
    sqlmap \\
    aircrack-ng \\
    john \\
    hashcat \\
    burpsuite \\
    wireshark \\
    tcpdump \\
    netcat-traditional \\
    socat \\
    python3 \\
    python3-pip \\
    git \\
    curl \\
    wget \\
    vim \\
    nano

# Instalar herramientas de phishing
RUN apt-get install -y \\
    setoolkit \\
    beef-xss

# Instalar herramientas de malware
RUN apt-get install -y \\
    veil \\
    empire

# Configurar Metasploit
RUN msfdb init

# Crear directorio de trabajo
WORKDIR /pentest

# Mantener contenedor activo
CMD ["/bin/bash"]
"""
            
            # Crear directorio temporal para build
            with tempfile.TemporaryDirectory() as temp_dir:
                dockerfile_path = Path(temp_dir) / "Dockerfile"
                dockerfile_path.write_text(dockerfile_content)
                
                # Construir imagen
                self.logger.info("Construyendo imagen Kali Linux...")
                image, logs = self.client.images.build(
                    path=temp_dir,
                    tag=f"{name}:latest",
                    rm=True
                )
                
                # Crear contenedor
                container = self.client.containers.run(
                    image.id,
                    name=name,
                    detach=True,
                    tty=True,
                    stdin_open=True,
                    privileged=True,  # Necesario para algunas herramientas
                    network_mode="host",  # Acceso completo a red
                    volumes={
                        "/tmp": {"bind": "/tmp", "mode": "rw"},
                        str(Path.cwd() / "reports"): {"bind": "/pentest/reports", "mode": "rw"}
                    }
                )
                
                self.containers[name] = container
                self.logger.info(f"Contenedor Kali creado: {container.id[:12]}")
                return container.id
                
        except Exception as e:
            self.logger.error(f"Error creando contenedor Kali: {e}")
            return None
    
    async def create_windows_container(self, name: str = "windows-target") -> Optional[str]:
        """Crea un contenedor Windows para testing"""
        try:
            # Usar imagen Windows Server Core
            container = self.client.containers.run(
                "mcr.microsoft.com/windows/servercore:ltsc2019",
                name=name,
                detach=True,
                tty=True,
                stdin_open=True,
                ports={"3389/tcp": 3389, "445/tcp": 445, "139/tcp": 139}
            )
            
            self.containers[name] = container
            self.logger.info(f"Contenedor Windows creado: {container.id[:12]}")
            return container.id
            
        except Exception as e:
            self.logger.error(f"Error creando contenedor Windows: {e}")
            return None
    
    async def execute_command(self, container_name: str, command: str) -> Dict[str, Any]:
        """Ejecuta comando en contenedor"""
        try:
            if container_name not in self.containers:
                self.logger.error(f"Contenedor {container_name} no encontrado")
                return {"success": False, "error": "Container not found"}
            
            container = self.containers[container_name]
            
            # Ejecutar comando
            result = container.exec_run(command, tty=True, stream=False)
            
            return {
                "success": True,
                "exit_code": result.exit_code,
                "output": result.output.decode('utf-8', errors='ignore'),
                "command": command
            }
            
        except Exception as e:
            self.logger.error(f"Error ejecutando comando en contenedor: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_isolated_network(self, name: str = "pentest-network") -> Optional[str]:
        """Crea red aislada para pentesting"""
        try:
            network = self.client.networks.create(
                name,
                driver="bridge",
                options={
                    "com.docker.network.bridge.enable_icc": "true",
                    "com.docker.network.bridge.enable_ip_masquerade": "true"
                }
            )
            
            self.networks[name] = network
            self.logger.info(f"Red aislada creada: {name}")
            return network.id
            
        except Exception as e:
            self.logger.error(f"Error creando red aislada: {e}")
            return None
    
    def cleanup(self):
        """Limpia contenedores y redes"""
        try:
            # Detener y eliminar contenedores
            for name, container in self.containers.items():
                try:
                    container.stop()
                    container.remove()
                    self.logger.info(f"Contenedor {name} eliminado")
                except:
                    pass
            
            # Eliminar redes
            for name, network in self.networks.items():
                try:
                    network.remove()
                    self.logger.info(f"Red {name} eliminada")
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Error durante limpieza Docker: {e}")

class VMManager:
    """Gestor de máquinas virtuales"""
    
    def __init__(self, logger):
        self.logger = logger
        self.vms = {}
        self.hypervisor = self._detect_hypervisor()
    
    def _detect_hypervisor(self) -> str:
        """Detecta el hipervisor disponible"""
        hypervisors = ["vboxmanage", "vmrun", "virsh"]
        
        for hypervisor in hypervisors:
            if self._command_exists(hypervisor):
                self.logger.info(f"Hipervisor detectado: {hypervisor}")
                return hypervisor
        
        self.logger.warning("No se detectó ningún hipervisor")
        return None
    
    def _command_exists(self, command: str) -> bool:
        """Verifica si un comando existe"""
        try:
            subprocess.run(["which", command], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    async def create_kali_vm(self, name: str = "kali-vm") -> bool:
        """Crea VM Kali Linux usando Vagrant"""
        try:
            # Vagrantfile para Kali
            vagrantfile_content = """
Vagrant.configure("2") do |config|
  config.vm.box = "kalilinux/rolling"
  config.vm.hostname = "kali-pentest"
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
    vb.name = "kali-pentest-vm"
  end
  
  config.vm.network "private_network", type: "dhcp"
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y metasploit-framework nmap nikto gobuster
    msfdb init
  SHELL
end
"""
            
            # Crear directorio para VM
            vm_dir = Path(f"./vms/{name}")
            vm_dir.mkdir(parents=True, exist_ok=True)
            
            # Escribir Vagrantfile
            vagrantfile_path = vm_dir / "Vagrantfile"
            vagrantfile_path.write_text(vagrantfile_content)
            
            # Iniciar VM
            process = await asyncio.create_subprocess_exec(
                "vagrant", "up",
                cwd=vm_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.vms[name] = str(vm_dir)
                self.logger.info(f"VM Kali creada: {name}")
                return True
            else:
                self.logger.error(f"Error creando VM: {stderr.decode()}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creando VM Kali: {e}")
            return False
    
    async def execute_vm_command(self, vm_name: str, command: str) -> Dict[str, Any]:
        """Ejecuta comando en VM"""
        try:
            if vm_name not in self.vms:
                return {"success": False, "error": "VM not found"}
            
            vm_dir = Path(self.vms[vm_name])
            
            process = await asyncio.create_subprocess_exec(
                "vagrant", "ssh", "-c", command,
                cwd=vm_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "exit_code": process.returncode,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore'),
                "command": command
            }
            
        except Exception as e:
            self.logger.error(f"Error ejecutando comando en VM: {e}")
            return {"success": False, "error": str(e)}
    
    def cleanup(self):
        """Limpia VMs"""
        try:
            for name, vm_dir in self.vms.items():
                try:
                    subprocess.run(["vagrant", "destroy", "-f"], 
                                 cwd=vm_dir, 
                                 check=False)
                    self.logger.info(f"VM {name} eliminada")
                except:
                    pass
        except Exception as e:
            self.logger.error(f"Error durante limpieza VMs: {e}")

class VirtualizationManager:
    """Gestor principal de virtualización"""
    
    def __init__(self, logger):
        self.logger = logger
        self.docker_manager = DockerManager(logger)
        self.vm_manager = VMManager(logger)
        self.environments = {}
    
    async def initialize(self):
        """Inicializa gestores de virtualización"""
        docker_ok = await self.docker_manager.initialize()
        
        self.logger.info("Gestor de virtualización inicializado")
        return docker_ok
    
    async def create_pentest_environment(self, env_type: str = "docker") -> str:
        """Crea entorno de pentesting completo"""
        try:
            env_id = f"pentest-env-{len(self.environments)}"
            
            if env_type == "docker":
                # Crear red aislada
                network_id = await self.docker_manager.create_isolated_network(f"{env_id}-network")
                
                # Crear contenedor Kali
                kali_id = await self.docker_manager.create_kali_container(f"{env_id}-kali")
                
                # Crear contenedor objetivo (opcional)
                target_id = await self.docker_manager.create_windows_container(f"{env_id}-target")
                
                self.environments[env_id] = {
                    "type": "docker",
                    "network": network_id,
                    "kali": kali_id,
                    "target": target_id
                }
                
            elif env_type == "vm":
                # Crear VM Kali
                vm_created = await self.vm_manager.create_kali_vm(f"{env_id}-kali")
                
                if vm_created:
                    self.environments[env_id] = {
                        "type": "vm",
                        "kali": f"{env_id}-kali"
                    }
            
            self.logger.info(f"Entorno de pentesting creado: {env_id}")
            return env_id
            
        except Exception as e:
            self.logger.error(f"Error creando entorno de pentesting: {e}")
            return None
    
    async def execute_in_environment(self, env_id: str, command: str, target: str = "kali") -> Dict[str, Any]:
        """Ejecuta comando en entorno específico"""
        if env_id not in self.environments:
            return {"success": False, "error": "Environment not found"}
        
        env = self.environments[env_id]
        
        if env["type"] == "docker":
            container_name = f"{env_id}-{target}"
            return await self.docker_manager.execute_command(container_name, command)
        
        elif env["type"] == "vm":
            vm_name = f"{env_id}-{target}"
            return await self.vm_manager.execute_vm_command(vm_name, command)
        
        return {"success": False, "error": "Unknown environment type"}
    
    def cleanup(self):
        """Limpia todos los entornos"""
        self.docker_manager.cleanup()
        self.vm_manager.cleanup()
        self.environments.clear()
        self.logger.info("Entornos de virtualización limpiados")