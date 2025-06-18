"""
Agente de Reconocimiento Avanzado
Utiliza múltiples herramientas de repositorios para reconocimiento completo
"""

import os
import json
import asyncio
import subprocess
import tempfile
import ipaddress
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

from .base_agent import BaseAgent
from core.evasion import EvasionManager
from core.virtualization import VirtualizationManager

class ReconnaissanceAgent(BaseAgent):
    """Agente especializado en reconocimiento y enumeración"""
    
    def __init__(self, db_manager, logger):
        super().__init__("ReconnaissanceAgent", db_manager, logger)
        self.evasion_manager = EvasionManager(logger)
        self.vm_manager = VirtualizationManager(logger)
        self.capabilities = [
            "network_scanning", "port_scanning", "service_enumeration",
            "subdomain_enumeration", "web_reconnaissance", "osint",
            "vulnerability_scanning", "wireless_reconnaissance"
        ]
        self.tools = {}
        self.scan_results = {}
        
    async def initialize(self):
        """Inicializa el agente de reconocimiento"""
        await super().initialize()
        await self.evasion_manager.initialize_evasion(["tor", "timing_randomization", "user_agent_rotation"])
        await self.vm_manager.initialize()
        await self._setup_tools()
        self.logger.info("Agente de Reconocimiento inicializado")
    
    async def _setup_tools(self):
        """Configura herramientas de reconocimiento"""
        self.tools = {
            # Escaneo de red
            "nmap": {
                "path": "/usr/bin/nmap",
                "repo_tools": ["masscan", "zmap", "rustscan"],
                "techniques": ["stealth_scan", "version_detection", "os_detection", "script_scan"]
            },
            
            # Enumeración de subdominios
            "subdomain_enum": {
                "tools": ["amass", "subfinder", "assetfinder", "findomain", "chaos", "dnsrecon"],
                "techniques": ["passive_dns", "certificate_transparency", "brute_force", "permutation"]
            },
            
            # Reconocimiento web
            "web_recon": {
                "tools": ["gobuster", "dirb", "dirsearch", "ffuf", "feroxbuster", "wfuzz"],
                "techniques": ["directory_bruteforce", "file_discovery", "parameter_fuzzing", "vhost_discovery"]
            },
            
            # Escaneo de vulnerabilidades
            "vuln_scan": {
                "tools": ["nikto", "nuclei", "nessus", "openvas", "wapiti", "skipfish"],
                "techniques": ["web_vulns", "network_vulns", "ssl_analysis", "cms_detection"]
            },
            
            # OSINT
            "osint": {
                "tools": ["theHarvester", "recon-ng", "maltego", "spiderfoot", "shodan", "censys"],
                "techniques": ["email_harvesting", "social_media", "search_engines", "public_databases"]
            },
            
            # Reconocimiento inalámbrico
            "wireless": {
                "tools": ["aircrack-ng", "kismet", "reaver", "bully", "wifite", "fluxion"],
                "techniques": ["ap_discovery", "client_enumeration", "wps_attack", "evil_twin"]
            },
            
            # Análisis de servicios
            "service_enum": {
                "tools": ["enum4linux", "smbclient", "rpcclient", "snmpwalk", "ldapsearch", "redis-cli"],
                "techniques": ["smb_enumeration", "ldap_enumeration", "snmp_enumeration", "database_enumeration"]
            }
        }
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analiza el objetivo y planifica reconocimiento"""
        analysis_prompt = f"""
        Analiza el siguiente objetivo para planificar reconocimiento completo: {target}
        
        Determina:
        1. Tipo de objetivo (IP, dominio, rango de red)
        2. Técnicas de reconocimiento apropiadas
        3. Herramientas recomendadas por categoría
        4. Orden de ejecución óptimo
        5. Técnicas de evasión necesarias
        6. Estimación de tiempo
        
        Considera usar múltiples herramientas de cada categoría para resultados completos.
        Responde en formato JSON.
        """
        
        analysis = await self.query_ai(analysis_prompt)
        
        try:
            import json
            result = json.loads(analysis)
        except:
            # Análisis automático por defecto
            result = await self._auto_analyze_target(target)
        
        return result
    
    async def _auto_analyze_target(self, target: str) -> Dict[str, Any]:
        """Análisis automático del objetivo"""
        target_type = "unknown"
        techniques = []
        
        try:
            # Verificar si es IP
            ipaddress.ip_address(target)
            target_type = "ip"
            techniques = ["port_scan", "service_enum", "vuln_scan"]
        except:
            try:
                # Verificar si es rango de red
                ipaddress.ip_network(target, strict=False)
                target_type = "network"
                techniques = ["network_discovery", "port_scan", "service_enum"]
            except:
                # Asumir que es dominio
                target_type = "domain"
                techniques = ["subdomain_enum", "web_recon", "osint", "port_scan"]
        
        return {
            "target_type": target_type,
            "recommended_techniques": techniques,
            "tools_by_category": {
                "network_scan": ["nmap", "masscan"],
                "subdomain_enum": ["amass", "subfinder", "assetfinder"],
                "web_recon": ["gobuster", "dirb", "ffuf"],
                "vuln_scan": ["nikto", "nuclei"],
                "osint": ["theHarvester", "shodan"]
            },
            "execution_order": techniques,
            "evasion_needed": True,
            "estimated_time": "30-60 minutes"
        }
    
    async def execute_comprehensive_recon(self, target: str) -> Dict[str, Any]:
        """Ejecuta reconocimiento completo usando múltiples herramientas"""
        try:
            self.logger.info(f"Iniciando reconocimiento completo de {target}")
            
            # Analizar objetivo
            analysis = await self.analyze_target(target)
            
            # Crear entorno aislado
            env_id = await self.vm_manager.create_pentest_environment("docker")
            
            results = {
                "target": target,
                "analysis": analysis,
                "environment": env_id,
                "scan_results": {},
                "start_time": datetime.now().isoformat(),
                "status": "running"
            }
            
            # Ejecutar técnicas según el análisis
            for technique in analysis.get("execution_order", []):
                if technique == "network_discovery":
                    results["scan_results"]["network_discovery"] = await self._network_discovery(target, env_id)
                elif technique == "port_scan":
                    results["scan_results"]["port_scan"] = await self._comprehensive_port_scan(target, env_id)
                elif technique == "subdomain_enum":
                    results["scan_results"]["subdomain_enum"] = await self._subdomain_enumeration(target, env_id)
                elif technique == "web_recon":
                    results["scan_results"]["web_recon"] = await self._web_reconnaissance(target, env_id)
                elif technique == "service_enum":
                    results["scan_results"]["service_enum"] = await self._service_enumeration(target, env_id)
                elif technique == "vuln_scan":
                    results["scan_results"]["vuln_scan"] = await self._vulnerability_scanning(target, env_id)
                elif technique == "osint":
                    results["scan_results"]["osint"] = await self._osint_gathering(target, env_id)
            
            results["status"] = "completed"
            results["end_time"] = datetime.now().isoformat()
            
            # Guardar resultados
            await self.db_manager.save_scan_results(results)
            
            self.logger.info(f"Reconocimiento completo de {target} finalizado")
            return results
            
        except Exception as e:
            self.logger.error(f"Error en reconocimiento completo: {e}")
            return {"error": str(e), "target": target}
    
    async def _network_discovery(self, target: str, env_id: str) -> Dict[str, Any]:
        """Descubrimiento de red usando múltiples herramientas"""
        results = {"technique": "network_discovery", "tools_used": [], "hosts_found": []}
        
        # Nmap ping sweep
        nmap_cmd = f"nmap -sn {target}"
        nmap_result = await self.evasion_manager.execute_with_evasion(nmap_cmd)
        if nmap_result["success"]:
            results["tools_used"].append("nmap")
            hosts = self._parse_nmap_ping_sweep(nmap_result["output"])
            results["hosts_found"].extend(hosts)
        
        # Masscan discovery (si está disponible)
        masscan_cmd = f"masscan {target} -p0 --ping"
        masscan_result = await self.evasion_manager.execute_with_evasion(masscan_cmd)
        if masscan_result["success"]:
            results["tools_used"].append("masscan")
            # Parsear resultados de masscan
        
        # ARP scan para redes locales
        if self._is_local_network(target):
            arp_cmd = f"arp-scan {target}"
            arp_result = await self.evasion_manager.execute_with_evasion(arp_cmd)
            if arp_result["success"]:
                results["tools_used"].append("arp-scan")
        
        return results
    
    async def _comprehensive_port_scan(self, target: str, env_id: str) -> Dict[str, Any]:
        """Escaneo de puertos usando múltiples herramientas"""
        results = {"technique": "port_scan", "tools_used": [], "open_ports": [], "services": {}}
        
        # Nmap stealth scan
        nmap_cmd = f"nmap -sS -sV -O -A --script=default,vuln {target}"
        nmap_result = await self.evasion_manager.execute_with_evasion(nmap_cmd)
        if nmap_result["success"]:
            results["tools_used"].append("nmap")
            ports, services = self._parse_nmap_results(nmap_result["output"])
            results["open_ports"].extend(ports)
            results["services"].update(services)
        
        # Masscan para escaneo rápido
        masscan_cmd = f"masscan {target} -p1-65535 --rate=1000"
        masscan_result = await self.evasion_manager.execute_with_evasion(masscan_cmd)
        if masscan_result["success"]:
            results["tools_used"].append("masscan")
            # Parsear resultados de masscan
        
        # Rustscan (si está disponible)
        rustscan_cmd = f"rustscan -a {target} -- -sV"
        rustscan_result = await self.evasion_manager.execute_with_evasion(rustscan_cmd)
        if rustscan_result["success"]:
            results["tools_used"].append("rustscan")
        
        # UDP scan con nmap
        nmap_udp_cmd = f"nmap -sU --top-ports 1000 {target}"
        nmap_udp_result = await self.evasion_manager.execute_with_evasion(nmap_udp_cmd)
        if nmap_udp_result["success"]:
            results["tools_used"].append("nmap-udp")
        
        return results
    
    async def _subdomain_enumeration(self, target: str, env_id: str) -> Dict[str, Any]:
        """Enumeración de subdominios usando múltiples herramientas"""
        results = {"technique": "subdomain_enum", "tools_used": [], "subdomains": set()}
        
        # Amass
        amass_cmd = f"amass enum -d {target}"
        amass_result = await self.evasion_manager.execute_with_evasion(amass_cmd)
        if amass_result["success"]:
            results["tools_used"].append("amass")
            subdomains = amass_result["output"].strip().split('\n')
            results["subdomains"].update(subdomains)
        
        # Subfinder
        subfinder_cmd = f"subfinder -d {target}"
        subfinder_result = await self.evasion_manager.execute_with_evasion(subfinder_cmd)
        if subfinder_result["success"]:
            results["tools_used"].append("subfinder")
            subdomains = subfinder_result["output"].strip().split('\n')
            results["subdomains"].update(subdomains)
        
        # Assetfinder
        assetfinder_cmd = f"assetfinder {target}"
        assetfinder_result = await self.evasion_manager.execute_with_evasion(assetfinder_cmd)
        if assetfinder_result["success"]:
            results["tools_used"].append("assetfinder")
            subdomains = assetfinder_result["output"].strip().split('\n')
            results["subdomains"].update(subdomains)
        
        # Findomain
        findomain_cmd = f"findomain -t {target}"
        findomain_result = await self.evasion_manager.execute_with_evasion(findomain_cmd)
        if findomain_result["success"]:
            results["tools_used"].append("findomain")
        
        # DNSrecon
        dnsrecon_cmd = f"dnsrecon -d {target} -t brt"
        dnsrecon_result = await self.evasion_manager.execute_with_evasion(dnsrecon_cmd)
        if dnsrecon_result["success"]:
            results["tools_used"].append("dnsrecon")
        
        # Convertir set a lista para JSON
        results["subdomains"] = list(results["subdomains"])
        
        return results
    
    async def _web_reconnaissance(self, target: str, env_id: str) -> Dict[str, Any]:
        """Reconocimiento web usando múltiples herramientas"""
        results = {"technique": "web_recon", "tools_used": [], "directories": [], "files": [], "technologies": []}
        
        # Gobuster
        gobuster_cmd = f"gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt"
        gobuster_result = await self.evasion_manager.execute_with_evasion(gobuster_cmd)
        if gobuster_result["success"]:
            results["tools_used"].append("gobuster")
            dirs = self._parse_gobuster_results(gobuster_result["output"])
            results["directories"].extend(dirs)
        
        # Dirb
        dirb_cmd = f"dirb http://{target}"
        dirb_result = await self.evasion_manager.execute_with_evasion(dirb_cmd)
        if dirb_result["success"]:
            results["tools_used"].append("dirb")
        
        # Dirsearch
        dirsearch_cmd = f"dirsearch -u http://{target}"
        dirsearch_result = await self.evasion_manager.execute_with_evasion(dirsearch_cmd)
        if dirsearch_result["success"]:
            results["tools_used"].append("dirsearch")
        
        # Ffuf
        ffuf_cmd = f"ffuf -w /usr/share/wordlists/dirb/common.txt -u http://{target}/FUZZ"
        ffuf_result = await self.evasion_manager.execute_with_evasion(ffuf_cmd)
        if ffuf_result["success"]:
            results["tools_used"].append("ffuf")
        
        # Feroxbuster
        feroxbuster_cmd = f"feroxbuster -u http://{target}"
        feroxbuster_result = await self.evasion_manager.execute_with_evasion(feroxbuster_cmd)
        if feroxbuster_result["success"]:
            results["tools_used"].append("feroxbuster")
        
        # Wfuzz para parámetros
        wfuzz_cmd = f"wfuzz -w /usr/share/wordlists/dirb/common.txt http://{target}/?FUZZ=test"
        wfuzz_result = await self.evasion_manager.execute_with_evasion(wfuzz_cmd)
        if wfuzz_result["success"]:
            results["tools_used"].append("wfuzz")
        
        # Whatweb para tecnologías
        whatweb_cmd = f"whatweb http://{target}"
        whatweb_result = await self.evasion_manager.execute_with_evasion(whatweb_cmd)
        if whatweb_result["success"]:
            results["tools_used"].append("whatweb")
            techs = self._parse_whatweb_results(whatweb_result["output"])
            results["technologies"].extend(techs)
        
        return results
    
    async def _service_enumeration(self, target: str, env_id: str) -> Dict[str, Any]:
        """Enumeración de servicios usando herramientas específicas"""
        results = {"technique": "service_enum", "tools_used": [], "services": {}}
        
        # SMB enumeration
        enum4linux_cmd = f"enum4linux {target}"
        enum4linux_result = await self.evasion_manager.execute_with_evasion(enum4linux_cmd)
        if enum4linux_result["success"]:
            results["tools_used"].append("enum4linux")
            results["services"]["smb"] = self._parse_enum4linux_results(enum4linux_result["output"])
        
        # SNMP enumeration
        snmpwalk_cmd = f"snmpwalk -v2c -c public {target}"
        snmpwalk_result = await self.evasion_manager.execute_with_evasion(snmpwalk_cmd)
        if snmpwalk_result["success"]:
            results["tools_used"].append("snmpwalk")
            results["services"]["snmp"] = snmpwalk_result["output"]
        
        # LDAP enumeration
        ldapsearch_cmd = f"ldapsearch -x -h {target} -s base"
        ldapsearch_result = await self.evasion_manager.execute_with_evasion(ldapsearch_cmd)
        if ldapsearch_result["success"]:
            results["tools_used"].append("ldapsearch")
            results["services"]["ldap"] = ldapsearch_result["output"]
        
        # DNS enumeration
        dnsrecon_cmd = f"dnsrecon -d {target} -a"
        dnsrecon_result = await self.evasion_manager.execute_with_evasion(dnsrecon_cmd)
        if dnsrecon_result["success"]:
            results["tools_used"].append("dnsrecon")
            results["services"]["dns"] = dnsrecon_result["output"]
        
        return results
    
    async def _vulnerability_scanning(self, target: str, env_id: str) -> Dict[str, Any]:
        """Escaneo de vulnerabilidades usando múltiples herramientas"""
        results = {"technique": "vuln_scan", "tools_used": [], "vulnerabilities": []}
        
        # Nikto
        nikto_cmd = f"nikto -h http://{target}"
        nikto_result = await self.evasion_manager.execute_with_evasion(nikto_cmd)
        if nikto_result["success"]:
            results["tools_used"].append("nikto")
            vulns = self._parse_nikto_results(nikto_result["output"])
            results["vulnerabilities"].extend(vulns)
        
        # Nuclei
        nuclei_cmd = f"nuclei -u http://{target}"
        nuclei_result = await self.evasion_manager.execute_with_evasion(nuclei_cmd)
        if nuclei_result["success"]:
            results["tools_used"].append("nuclei")
            vulns = self._parse_nuclei_results(nuclei_result["output"])
            results["vulnerabilities"].extend(vulns)
        
        # Wapiti
        wapiti_cmd = f"wapiti -u http://{target}"
        wapiti_result = await self.evasion_manager.execute_with_evasion(wapiti_cmd)
        if wapiti_result["success"]:
            results["tools_used"].append("wapiti")
        
        # Skipfish
        skipfish_cmd = f"skipfish -o /tmp/skipfish_results http://{target}"
        skipfish_result = await self.evasion_manager.execute_with_evasion(skipfish_cmd)
        if skipfish_result["success"]:
            results["tools_used"].append("skipfish")
        
        return results
    
    async def _osint_gathering(self, target: str, env_id: str) -> Dict[str, Any]:
        """Recopilación OSINT usando múltiples herramientas"""
        results = {"technique": "osint", "tools_used": [], "emails": [], "social_media": [], "leaked_data": []}
        
        # theHarvester
        harvester_cmd = f"theHarvester -d {target} -b all"
        harvester_result = await self.evasion_manager.execute_with_evasion(harvester_cmd)
        if harvester_result["success"]:
            results["tools_used"].append("theHarvester")
            emails = self._parse_harvester_results(harvester_result["output"])
            results["emails"].extend(emails)
        
        # Shodan search (si hay API key)
        shodan_cmd = f"shodan search hostname:{target}"
        shodan_result = await self.evasion_manager.execute_with_evasion(shodan_cmd)
        if shodan_result["success"]:
            results["tools_used"].append("shodan")
        
        # Recon-ng
        recon_ng_cmd = f"recon-ng -m recon/domains-hosts/hackertarget"
        recon_ng_result = await self.evasion_manager.execute_with_evasion(recon_ng_cmd)
        if recon_ng_result["success"]:
            results["tools_used"].append("recon-ng")
        
        # SpiderFoot
        spiderfoot_cmd = f"spiderfoot -s {target}"
        spiderfoot_result = await self.evasion_manager.execute_with_evasion(spiderfoot_cmd)
        if spiderfoot_result["success"]:
            results["tools_used"].append("spiderfoot")
        
        return results
    
    # Métodos de parsing de resultados
    def _parse_nmap_ping_sweep(self, output: str) -> List[str]:
        """Parsea resultados de ping sweep de Nmap"""
        hosts = []
        lines = output.split('\n')
        for line in lines:
            if "Nmap scan report for" in line:
                host = line.split()[-1].strip('()')
                hosts.append(host)
        return hosts
    
    def _parse_nmap_results(self, output: str) -> Tuple[List[int], Dict[int, str]]:
        """Parsea resultados de escaneo Nmap"""
        ports = []
        services = {}
        
        lines = output.split('\n')
        for line in lines:
            if "/tcp" in line and "open" in line:
                parts = line.split()
                port_info = parts[0]
                port = int(port_info.split('/')[0])
                service = parts[2] if len(parts) > 2 else "unknown"
                
                ports.append(port)
                services[port] = service
        
        return ports, services
    
    def _parse_gobuster_results(self, output: str) -> List[str]:
        """Parsea resultados de Gobuster"""
        directories = []
        lines = output.split('\n')
        for line in lines:
            if "(Status: 200)" in line or "(Status: 301)" in line:
                path = line.split()[0]
                directories.append(path)
        return directories
    
    def _parse_whatweb_results(self, output: str) -> List[str]:
        """Parsea resultados de Whatweb"""
        technologies = []
        if "[" in output and "]" in output:
            tech_section = output.split('[')[1].split(']')[0]
            techs = tech_section.split(',')
            technologies = [tech.strip() for tech in techs]
        return technologies
    
    def _parse_enum4linux_results(self, output: str) -> Dict[str, Any]:
        """Parsea resultados de enum4linux"""
        return {"raw_output": output}  # Simplificado
    
    def _parse_nikto_results(self, output: str) -> List[Dict[str, str]]:
        """Parsea resultados de Nikto"""
        vulnerabilities = []
        lines = output.split('\n')
        for line in lines:
            if "+ " in line and "OSVDB" in line:
                vulnerabilities.append({
                    "description": line.strip(),
                    "severity": "medium",
                    "tool": "nikto"
                })
        return vulnerabilities
    
    def _parse_nuclei_results(self, output: str) -> List[Dict[str, str]]:
        """Parsea resultados de Nuclei"""
        vulnerabilities = []
        lines = output.split('\n')
        for line in lines:
            if "[" in line and "]" in line:
                vulnerabilities.append({
                    "description": line.strip(),
                    "severity": "unknown",
                    "tool": "nuclei"
                })
        return vulnerabilities
    
    def _parse_harvester_results(self, output: str) -> List[str]:
        """Parsea resultados de theHarvester"""
        emails = []
        lines = output.split('\n')
        for line in lines:
            if "@" in line and "." in line:
                # Extraer emails usando regex simple
                import re
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                found_emails = re.findall(email_pattern, line)
                emails.extend(found_emails)
        return list(set(emails))  # Eliminar duplicados
    
    def _is_local_network(self, target: str) -> bool:
        """Verifica si el objetivo es una red local"""
        try:
            network = ipaddress.ip_network(target, strict=False)
            return network.is_private
        except:
            return False
    
    async def execute_targeted_recon(self, target: str, technique: str) -> Dict[str, Any]:
        """Ejecuta técnica específica de reconocimiento"""
        try:
            if technique == "port_scan":
                return await self._comprehensive_port_scan(target, None)
            elif technique == "subdomain_enum":
                return await self._subdomain_enumeration(target, None)
            elif technique == "web_recon":
                return await self._web_reconnaissance(target, None)
            elif technique == "vuln_scan":
                return await self._vulnerability_scanning(target, None)
            elif technique == "osint":
                return await self._osint_gathering(target, None)
            else:
                return {"error": f"Técnica no soportada: {technique}"}
                
        except Exception as e:
            self.logger.error(f"Error en reconocimiento dirigido: {e}")
            return {"error": str(e)}
    
    def get_scan_results(self, target: str = None) -> List[Dict[str, Any]]:
        """Obtiene resultados de escaneos"""
        if target:
            return [result for result in self.scan_results.values() if result.get("target") == target]
        return list(self.scan_results.values())
    
    def cleanup(self):
        """Limpia recursos del agente"""
        super().cleanup()
        self.evasion_manager.cleanup()
        self.vm_manager.cleanup()
        self.logger.info("Agente de Reconocimiento limpiado")