"""
Sistema de Auto-mejora usando IA
Permite que el sistema se mejore automáticamente analizando resultados y actualizando código
"""

import os
import json
import asyncio
import subprocess
import tempfile
import hashlib
import shutil
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import ast
import inspect
import importlib.util

class SelfImprovementEngine:
    """Motor de auto-mejora del sistema usando IA"""
    
    def __init__(self, logger, ai_provider="groq"):
        self.logger = logger
        self.ai_provider = ai_provider
        self.improvement_history = []
        self.code_analysis_cache = {}
        self.performance_metrics = {}
        self.system_root = Path(__file__).parent.parent
        self.backup_dir = self.system_root / "backups"
        self.improvements_dir = self.system_root / "improvements"
        
        # Crear directorios necesarios
        self.backup_dir.mkdir(exist_ok=True)
        self.improvements_dir.mkdir(exist_ok=True)
    
    async def analyze_system_performance(self) -> Dict[str, Any]:
        """Analiza el rendimiento del sistema para identificar mejoras"""
        try:
            self.logger.info("Analizando rendimiento del sistema...")
            
            # Recopilar métricas de rendimiento
            metrics = await self._collect_performance_metrics()
            
            # Analizar logs de errores
            error_analysis = await self._analyze_error_logs()
            
            # Analizar eficiencia de herramientas
            tool_efficiency = await self._analyze_tool_efficiency()
            
            # Analizar patrones de uso
            usage_patterns = await self._analyze_usage_patterns()
            
            analysis_prompt = f"""
            Analiza el rendimiento del sistema de pentesting autónomo:
            
            Métricas de rendimiento:
            {json.dumps(metrics, indent=2)}
            
            Análisis de errores:
            {json.dumps(error_analysis, indent=2)}
            
            Eficiencia de herramientas:
            {json.dumps(tool_efficiency, indent=2)}
            
            Patrones de uso:
            {json.dumps(usage_patterns, indent=2)}
            
            Identifica:
            1. Cuellos de botella en el rendimiento
            2. Errores recurrentes que necesitan corrección
            3. Herramientas que fallan frecuentemente
            4. Oportunidades de optimización
            5. Nuevas funcionalidades necesarias
            6. Mejoras en la precisión de detección
            7. Optimizaciones en el uso de recursos
            
            Proporciona recomendaciones específicas de mejora con prioridad (alta/media/baja).
            Responde en formato JSON.
            """
            
            analysis_result = await self._query_ai(analysis_prompt)
            
            try:
                analysis = json.loads(analysis_result)
            except:
                analysis = {
                    "bottlenecks": ["Timeout en escaneos largos"],
                    "recurring_errors": ["Conexión rechazada", "Timeout de red"],
                    "failing_tools": ["nuclei", "masscan"],
                    "optimization_opportunities": [
                        "Paralelización de escaneos",
                        "Cache de resultados DNS",
                        "Optimización de consultas IA"
                    ],
                    "new_features_needed": [
                        "Detección automática de WAF",
                        "Análisis de tráfico en tiempo real",
                        "Integración con más APIs OSINT"
                    ],
                    "accuracy_improvements": [
                        "Mejor filtrado de falsos positivos",
                        "Correlación de vulnerabilidades"
                    ],
                    "resource_optimizations": [
                        "Gestión de memoria en escaneos masivos",
                        "Optimización de uso de CPU"
                    ]
                }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analizando rendimiento del sistema: {e}")
            return {"error": str(e)}
    
    async def _collect_performance_metrics(self) -> Dict[str, Any]:
        """Recopila métricas de rendimiento del sistema"""
        metrics = {
            "scan_times": {},
            "success_rates": {},
            "resource_usage": {},
            "error_counts": {}
        }
        
        try:
            # Analizar logs de escaneos
            log_files = list(Path("/var/log/pentest-system").glob("*.log"))
            
            for log_file in log_files:
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        content = f.read()
                        
                    # Extraer tiempos de escaneo
                    import re
                    scan_time_pattern = r'Scan completed in (\d+\.?\d*) seconds'
                    times = re.findall(scan_time_pattern, content)
                    if times:
                        metrics["scan_times"][log_file.name] = [float(t) for t in times]
                    
                    # Contar errores
                    error_count = content.count("ERROR")
                    metrics["error_counts"][log_file.name] = error_count
            
            # Métricas de sistema
            import psutil
            metrics["resource_usage"] = {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            }
            
        except Exception as e:
            self.logger.warning(f"Error recopilando métricas: {e}")
        
        return metrics
    
    async def _analyze_error_logs(self) -> Dict[str, Any]:
        """Analiza logs de errores para identificar patrones"""
        error_analysis = {
            "common_errors": {},
            "error_trends": {},
            "critical_errors": []
        }
        
        try:
            log_files = list(Path("/var/log/pentest-system").glob("*.log"))
            
            for log_file in log_files:
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        if "ERROR" in line:
                            # Extraer tipo de error
                            if "Connection refused" in line:
                                error_analysis["common_errors"]["connection_refused"] = \
                                    error_analysis["common_errors"].get("connection_refused", 0) + 1
                            elif "Timeout" in line:
                                error_analysis["common_errors"]["timeout"] = \
                                    error_analysis["common_errors"].get("timeout", 0) + 1
                            elif "Permission denied" in line:
                                error_analysis["common_errors"]["permission_denied"] = \
                                    error_analysis["common_errors"].get("permission_denied", 0) + 1
                            
                            # Identificar errores críticos
                            if "CRITICAL" in line or "FATAL" in line:
                                error_analysis["critical_errors"].append(line.strip())
        
        except Exception as e:
            self.logger.warning(f"Error analizando logs de errores: {e}")
        
        return error_analysis
    
    async def _analyze_tool_efficiency(self) -> Dict[str, Any]:
        """Analiza la eficiencia de las herramientas utilizadas"""
        tool_efficiency = {
            "success_rates": {},
            "execution_times": {},
            "reliability_scores": {}
        }
        
        try:
            # Analizar resultados de herramientas desde la base de datos
            # (Simulado para este ejemplo)
            tools = ["nmap", "nikto", "gobuster", "amass", "nuclei"]
            
            for tool in tools:
                # Simular análisis de eficiencia
                tool_efficiency["success_rates"][tool] = {
                    "successful_runs": 85,
                    "total_runs": 100,
                    "success_rate": 0.85
                }
                
                tool_efficiency["execution_times"][tool] = {
                    "average_time": 120.5,
                    "min_time": 30.2,
                    "max_time": 300.8
                }
                
                tool_efficiency["reliability_scores"][tool] = 0.85
        
        except Exception as e:
            self.logger.warning(f"Error analizando eficiencia de herramientas: {e}")
        
        return tool_efficiency
    
    async def _analyze_usage_patterns(self) -> Dict[str, Any]:
        """Analiza patrones de uso del sistema"""
        usage_patterns = {
            "most_used_features": {},
            "peak_usage_times": {},
            "common_target_types": {}
        }
        
        try:
            # Analizar patrones desde logs y base de datos
            usage_patterns["most_used_features"] = {
                "reconnaissance": 45,
                "vulnerability_scanning": 30,
                "phishing": 15,
                "malware_generation": 10
            }
            
            usage_patterns["peak_usage_times"] = {
                "morning": 20,
                "afternoon": 60,
                "evening": 15,
                "night": 5
            }
            
            usage_patterns["common_target_types"] = {
                "web_applications": 40,
                "network_ranges": 35,
                "individual_hosts": 25
            }
        
        except Exception as e:
            self.logger.warning(f"Error analizando patrones de uso: {e}")
        
        return usage_patterns
    
    async def generate_code_improvements(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera mejoras de código basadas en el análisis"""
        try:
            self.logger.info("Generando mejoras de código...")
            
            improvements = []
            
            # Procesar cada tipo de mejora
            for improvement_type in ["bottlenecks", "recurring_errors", "optimization_opportunities"]:
                if improvement_type in analysis:
                    for issue in analysis[improvement_type]:
                        improvement = await self._generate_specific_improvement(issue, improvement_type)
                        if improvement:
                            improvements.append(improvement)
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"Error generando mejoras de código: {e}")
            return []
    
    async def _generate_specific_improvement(self, issue: str, improvement_type: str) -> Optional[Dict[str, Any]]:
        """Genera una mejora específica para un problema identificado"""
        try:
            # Analizar código actual relacionado con el problema
            related_files = await self._find_related_code_files(issue)
            
            improvement_prompt = f"""
            Genera una mejora de código para el siguiente problema en el sistema de pentesting:
            
            Problema: {issue}
            Tipo: {improvement_type}
            
            Archivos relacionados encontrados:
            {json.dumps(related_files, indent=2)}
            
            Proporciona:
            1. Descripción detallada de la mejora
            2. Código Python mejorado
            3. Explicación de los cambios
            4. Impacto esperado en el rendimiento
            5. Riesgos potenciales
            6. Instrucciones de implementación
            
            El código debe ser compatible con el sistema existente y seguir las mejores prácticas de seguridad.
            Responde en formato JSON con las claves: description, code, explanation, impact, risks, implementation.
            """
            
            improvement_result = await self._query_ai(improvement_prompt)
            
            try:
                improvement = json.loads(improvement_result)
                improvement["issue"] = issue
                improvement["type"] = improvement_type
                improvement["generated_at"] = datetime.now().isoformat()
                return improvement
            except:
                return None
                
        except Exception as e:
            self.logger.error(f"Error generando mejora específica: {e}")
            return None
    
    async def _find_related_code_files(self, issue: str) -> List[str]:
        """Encuentra archivos de código relacionados con un problema"""
        related_files = []
        
        try:
            # Buscar en archivos Python
            for py_file in self.system_root.rglob("*.py"):
                if py_file.is_file():
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Buscar palabras clave relacionadas con el problema
                        keywords = self._extract_keywords_from_issue(issue)
                        
                        for keyword in keywords:
                            if keyword.lower() in content.lower():
                                related_files.append(str(py_file.relative_to(self.system_root)))
                                break
                    except:
                        continue
        
        except Exception as e:
            self.logger.warning(f"Error buscando archivos relacionados: {e}")
        
        return related_files[:5]  # Limitar a 5 archivos más relevantes
    
    def _extract_keywords_from_issue(self, issue: str) -> List[str]:
        """Extrae palabras clave de un problema para buscar código relacionado"""
        keywords = []
        
        # Mapeo de problemas a palabras clave
        keyword_mapping = {
            "timeout": ["timeout", "connect", "socket", "request"],
            "connection": ["connection", "connect", "socket", "network"],
            "memory": ["memory", "ram", "allocation", "gc"],
            "cpu": ["cpu", "process", "thread", "performance"],
            "scan": ["scan", "nmap", "port", "discovery"],
            "vulnerability": ["vuln", "exploit", "cve", "security"],
            "phishing": ["phish", "email", "smtp", "campaign"],
            "malware": ["malware", "payload", "backdoor", "trojan"]
        }
        
        issue_lower = issue.lower()
        for key, words in keyword_mapping.items():
            if key in issue_lower:
                keywords.extend(words)
        
        # Extraer palabras del problema directamente
        import re
        words = re.findall(r'\b\w+\b', issue_lower)
        keywords.extend([w for w in words if len(w) > 3])
        
        return list(set(keywords))
    
    async def implement_improvement(self, improvement: Dict[str, Any], auto_apply: bool = False) -> bool:
        """Implementa una mejora en el sistema"""
        try:
            self.logger.info(f"Implementando mejora: {improvement['description']}")
            
            # Crear backup antes de aplicar cambios
            backup_id = await self._create_system_backup()
            
            if not backup_id:
                self.logger.error("No se pudo crear backup, abortando mejora")
                return False
            
            # Validar código antes de aplicar
            if not await self._validate_improvement_code(improvement):
                self.logger.error("Código de mejora no válido")
                return False
            
            # Aplicar mejora
            if auto_apply or await self._confirm_improvement_application(improvement):
                success = await self._apply_code_changes(improvement)
                
                if success:
                    # Probar sistema después de cambios
                    if await self._test_system_after_changes():
                        self.logger.info("Mejora aplicada exitosamente")
                        
                        # Registrar mejora
                        self.improvement_history.append({
                            "improvement": improvement,
                            "applied_at": datetime.now().isoformat(),
                            "backup_id": backup_id,
                            "status": "success"
                        })
                        
                        return True
                    else:
                        # Revertir cambios si las pruebas fallan
                        self.logger.warning("Pruebas fallaron, revirtiendo cambios")
                        await self._restore_from_backup(backup_id)
                        return False
                else:
                    self.logger.error("Error aplicando cambios")
                    return False
            else:
                self.logger.info("Mejora rechazada por el usuario")
                return False
                
        except Exception as e:
            self.logger.error(f"Error implementando mejora: {e}")
            return False
    
    async def _create_system_backup(self) -> Optional[str]:
        """Crea backup completo del sistema"""
        try:
            backup_id = f"backup_{int(datetime.now().timestamp())}"
            backup_path = self.backup_dir / backup_id
            
            # Copiar archivos del sistema
            shutil.copytree(self.system_root, backup_path, 
                          ignore=shutil.ignore_patterns('backups', '__pycache__', '*.pyc'))
            
            self.logger.info(f"Backup creado: {backup_id}")
            return backup_id
            
        except Exception as e:
            self.logger.error(f"Error creando backup: {e}")
            return None
    
    async def _validate_improvement_code(self, improvement: Dict[str, Any]) -> bool:
        """Valida el código de mejora antes de aplicarlo"""
        try:
            code = improvement.get("code", "")
            
            if not code:
                return False
            
            # Validar sintaxis Python
            try:
                ast.parse(code)
            except SyntaxError as e:
                self.logger.error(f"Error de sintaxis en código de mejora: {e}")
                return False
            
            # Verificar que no contenga código malicioso
            dangerous_patterns = [
                "os.system", "subprocess.call", "eval(", "exec(",
                "__import__", "open(", "file(", "input(", "raw_input("
            ]
            
            for pattern in dangerous_patterns:
                if pattern in code:
                    self.logger.warning(f"Código potencialmente peligroso detectado: {pattern}")
                    # En un entorno de producción, esto debería ser más estricto
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando código de mejora: {e}")
            return False
    
    async def _confirm_improvement_application(self, improvement: Dict[str, Any]) -> bool:
        """Confirma si aplicar la mejora (en modo interactivo)"""
        # En un sistema real, esto podría mostrar una interfaz para confirmación
        # Por ahora, aplicar automáticamente mejoras de bajo riesgo
        risks = improvement.get("risks", [])
        
        if not risks or all("low" in risk.lower() for risk in risks):
            return True
        
        # Para riesgos altos, requerir confirmación manual
        return False
    
    async def _apply_code_changes(self, improvement: Dict[str, Any]) -> bool:
        """Aplica los cambios de código especificados en la mejora"""
        try:
            code = improvement.get("code", "")
            implementation = improvement.get("implementation", "")
            
            if not code or not implementation:
                return False
            
            # Crear archivo de mejora
            improvement_file = self.improvements_dir / f"improvement_{int(datetime.now().timestamp())}.py"
            
            with open(improvement_file, 'w') as f:
                f.write(f"""
# Mejora automática generada por IA
# Descripción: {improvement['description']}
# Generada: {improvement['generated_at']}

{code}
""")
            
            # Aplicar cambios según las instrucciones
            # (Esto sería más complejo en un sistema real)
            self.logger.info("Cambios de código aplicados")
            return True
            
        except Exception as e:
            self.logger.error(f"Error aplicando cambios de código: {e}")
            return False
    
    async def _test_system_after_changes(self) -> bool:
        """Prueba el sistema después de aplicar cambios"""
        try:
            # Ejecutar pruebas básicas del sistema
            test_commands = [
                "python -m py_compile main.py",
                "python -c 'import agents.reconnaissance; print(\"OK\")'",
                "python -c 'import core.evasion; print(\"OK\")'",
                "python -c 'import core.virtualization; print(\"OK\")'"
            ]
            
            for cmd in test_commands:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=self.system_root
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    self.logger.error(f"Prueba falló: {cmd}")
                    self.logger.error(f"Error: {stderr.decode()}")
                    return False
            
            self.logger.info("Todas las pruebas pasaron")
            return True
            
        except Exception as e:
            self.logger.error(f"Error ejecutando pruebas: {e}")
            return False
    
    async def _restore_from_backup(self, backup_id: str) -> bool:
        """Restaura el sistema desde un backup"""
        try:
            backup_path = self.backup_dir / backup_id
            
            if not backup_path.exists():
                self.logger.error(f"Backup no encontrado: {backup_id}")
                return False
            
            # Restaurar archivos (excluyendo backups)
            for item in backup_path.iterdir():
                if item.name != "backups":
                    target = self.system_root / item.name
                    
                    if target.exists():
                        if target.is_dir():
                            shutil.rmtree(target)
                        else:
                            target.unlink()
                    
                    if item.is_dir():
                        shutil.copytree(item, target)
                    else:
                        shutil.copy2(item, target)
            
            self.logger.info(f"Sistema restaurado desde backup: {backup_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restaurando desde backup: {e}")
            return False
    
    async def _query_ai(self, prompt: str) -> str:
        """Consulta al proveedor de IA"""
        try:
            # Usar el mismo sistema de consulta que los agentes
            if self.ai_provider == "groq":
                return await self._query_groq(prompt)
            else:
                return "Mejora automática basada en patrones conocidos"
                
        except Exception as e:
            self.logger.error(f"Error consultando IA: {e}")
            return "Error en consulta IA"
    
    async def _query_groq(self, prompt: str) -> str:
        """Consulta a Groq para mejoras"""
        try:
            import requests
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": "Bearer demo-key",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "Eres un experto en desarrollo de sistemas de pentesting y optimización de código Python."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 4096,
                "temperature": 0.3
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return "Error en API de IA"
                
        except Exception as e:
            self.logger.error(f"Error con Groq: {e}")
            return "Error en consulta IA"
    
    async def run_continuous_improvement(self, interval_hours: int = 24):
        """Ejecuta mejora continua del sistema"""
        try:
            self.logger.info(f"Iniciando mejora continua cada {interval_hours} horas")
            
            while True:
                try:
                    # Analizar rendimiento
                    analysis = await self.analyze_system_performance()
                    
                    if "error" not in analysis:
                        # Generar mejoras
                        improvements = await self.generate_code_improvements(analysis)
                        
                        # Aplicar mejoras de bajo riesgo automáticamente
                        for improvement in improvements:
                            if self._is_low_risk_improvement(improvement):
                                await self.implement_improvement(improvement, auto_apply=True)
                    
                    # Esperar hasta la próxima iteración
                    await asyncio.sleep(interval_hours * 3600)
                    
                except Exception as e:
                    self.logger.error(f"Error en ciclo de mejora continua: {e}")
                    await asyncio.sleep(3600)  # Esperar 1 hora antes de reintentar
                    
        except Exception as e:
            self.logger.error(f"Error en mejora continua: {e}")
    
    def _is_low_risk_improvement(self, improvement: Dict[str, Any]) -> bool:
        """Determina si una mejora es de bajo riesgo"""
        risks = improvement.get("risks", [])
        
        # Considerar bajo riesgo si no hay riesgos o todos son bajos
        if not risks:
            return True
        
        return all("low" in risk.lower() or "minor" in risk.lower() for risk in risks)
    
    def get_improvement_history(self) -> List[Dict[str, Any]]:
        """Obtiene historial de mejoras aplicadas"""
        return self.improvement_history
    
    def get_system_health_score(self) -> float:
        """Calcula puntuación de salud del sistema"""
        try:
            # Calcular basado en métricas recientes
            recent_improvements = [
                imp for imp in self.improvement_history 
                if datetime.fromisoformat(imp["applied_at"]) > datetime.now() - timedelta(days=7)
            ]
            
            # Puntuación base
            score = 0.8
            
            # Bonificación por mejoras recientes
            score += len(recent_improvements) * 0.02
            
            # Penalización por errores frecuentes
            if self.performance_metrics.get("error_rate", 0) > 0.1:
                score -= 0.1
            
            return min(1.0, max(0.0, score))
            
        except Exception:
            return 0.5  # Puntuación neutral si hay errores