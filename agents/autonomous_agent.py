#!/usr/bin/env python3
"""
🤖 Agente Autónomo - Funciona hasta conseguir el objetivo
La IA trabaja de forma completamente autónoma hasta lograr el objetivo especificado
"""

import asyncio
import subprocess
import json
import time
import os
from typing import Dict, List, Any
from pathlib import Path
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from core.logger import setup_logger

class AutonomousAgent:
    """Agente que funciona autónomamente hasta conseguir el objetivo"""
    
    def __init__(self, objective: str = None):
        self.logger = setup_logger("autonomous-agent")
        self.agent = BaseAgent(None, self.logger)
        self.objective = objective or "Obtener acceso completo al sistema objetivo"
        self.completed_tasks = []
        self.failed_attempts = []
        self.current_strategy = None
        self.max_attempts = 100
        self.attempt_count = 0
        self.success = False
        
    async def start_autonomous_operation(self):
        """Inicia la operación autónoma hasta conseguir el objetivo"""
        
        print(f"🤖 INICIANDO OPERACIÓN AUTÓNOMA")
        print(f"🎯 OBJETIVO: {self.objective}")
        print(f"⚠️ LA IA TRABAJARÁ HASTA CONSEGUIR EL OBJETIVO")
        print(f"🔄 MÁXIMO {self.max_attempts} INTENTOS")
        print("=" * 60)
        
        while not self.success and self.attempt_count < self.max_attempts:
            self.attempt_count += 1
            
            print(f"\n🔄 INTENTO {self.attempt_count}/{self.max_attempts}")
            
            try:
                # Analizar situación actual
                situation = await self.analyze_current_situation()
                
                # Planificar siguiente acción
                action_plan = await self.plan_next_action(situation)
                
                # Ejecutar acción
                result = await self.execute_action(action_plan)
                
                # Evaluar si se logró el objetivo
                success_check = await self.check_objective_completion(result)
                
                if success_check:
                    self.success = True
                    print(f"🎉 ¡OBJETIVO CONSEGUIDO EN INTENTO {self.attempt_count}!")
                    break
                else:
                    print(f"⏳ Objetivo no conseguido aún. Continuando...")
                    await asyncio.sleep(2)  # Pausa breve antes del siguiente intento
                    
            except Exception as e:
                print(f"❌ Error en intento {self.attempt_count}: {e}")
                self.failed_attempts.append(str(e))
                await asyncio.sleep(5)  # Pausa más larga en caso de error
        
        if self.success:
            await self.generate_success_report()
        else:
            await self.generate_failure_report()
    
    async def analyze_current_situation(self) -> Dict[str, Any]:
        """Analiza la situación actual del sistema y objetivo"""
        
        analysis_prompt = f"""
        ANÁLISIS DE SITUACIÓN ACTUAL:
        
        Objetivo: {self.objective}
        Intento: {self.attempt_count}
        Tareas completadas: {len(self.completed_tasks)}
        Fallos previos: {len(self.failed_attempts)}
        
        Analiza la situación actual del sistema:
        1. ¿Qué información tenemos sobre el objetivo?
        2. ¿Qué herramientas están disponibles?
        3. ¿Qué estrategias han fallado antes?
        4. ¿Cuál es el estado actual de la red/sistema?
        5. ¿Qué vulnerabilidades potenciales existen?
        
        Proporciona un análisis detallado en formato JSON:
        {{
            "target_info": "información del objetivo",
            "available_tools": ["lista", "de", "herramientas"],
            "network_status": "estado de la red",
            "potential_vulnerabilities": ["vuln1", "vuln2"],
            "recommended_approach": "enfoque recomendado"
        }}
        """
        
        try:
            analysis = await self.agent.query_ai(analysis_prompt)
            
            # Intentar parsear como JSON
            try:
                return json.loads(analysis)
            except:
                # Si no es JSON válido, crear estructura básica
                return {
                    "target_info": analysis,
                    "available_tools": ["nmap", "metasploit", "hydra", "sqlmap"],
                    "network_status": "unknown",
                    "potential_vulnerabilities": ["unknown"],
                    "recommended_approach": analysis
                }
                
        except Exception as e:
            print(f"Error en análisis: {e}")
            return {"error": str(e)}
    
    async def plan_next_action(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Planifica la siguiente acción basada en la situación"""
        
        planning_prompt = f"""
        PLANIFICACIÓN DE ACCIÓN:
        
        Objetivo: {self.objective}
        Situación actual: {json.dumps(situation, indent=2)}
        Tareas completadas: {self.completed_tasks}
        Intentos fallidos: {self.failed_attempts}
        
        Basado en la situación, planifica la MEJOR acción para conseguir el objetivo.
        
        Puedes usar CUALQUIER herramienta o técnica:
        - Escaneo de red (nmap, masscan)
        - Explotación (metasploit, exploits manuales)
        - Fuerza bruta (hydra, john, hashcat)
        - Inyección SQL (sqlmap)
        - Phishing (setoolkit, gophish)
        - Malware (msfvenom, custom payloads)
        - Ingeniería social
        - Escalación de privilegios
        - Persistencia
        
        Responde en formato JSON:
        {{
            "action_type": "tipo de acción",
            "tool": "herramienta a usar",
            "command": "comando exacto a ejecutar",
            "target": "objetivo específico",
            "expected_result": "resultado esperado",
            "backup_plan": "plan alternativo si falla"
        }}
        """
        
        try:
            plan = await self.agent.query_ai(planning_prompt)
            
            try:
                return json.loads(plan)
            except:
                # Plan básico si no es JSON válido
                return {
                    "action_type": "reconnaissance",
                    "tool": "nmap",
                    "command": f"nmap -sS -O -A {self.objective}",
                    "target": self.objective,
                    "expected_result": "información del objetivo",
                    "backup_plan": "usar masscan si nmap falla"
                }
                
        except Exception as e:
            print(f"Error en planificación: {e}")
            return {"error": str(e)}
    
    async def execute_action(self, action_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la acción planificada"""
        
        if "error" in action_plan:
            return {"error": "Plan de acción inválido"}
        
        action_type = action_plan.get("action_type", "unknown")
        command = action_plan.get("command", "")
        tool = action_plan.get("tool", "unknown")
        
        print(f"🔧 EJECUTANDO: {action_type}")
        print(f"🛠️ HERRAMIENTA: {tool}")
        print(f"💻 COMANDO: {command}")
        
        try:
            # Ejecutar comando
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            execution_result = {
                "action_type": action_type,
                "tool": tool,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
            
            # Registrar resultado
            if execution_result["success"]:
                self.completed_tasks.append(action_plan)
                print(f"✅ ÉXITO: {action_type}")
                if result.stdout:
                    print(f"📊 RESULTADO:\n{result.stdout}")
            else:
                self.failed_attempts.append(f"{action_type}: {result.stderr}")
                print(f"❌ FALLO: {action_type}")
                if result.stderr:
                    print(f"⚠️ ERROR:\n{result.stderr}")
                
                # Intentar plan de backup
                backup_plan = action_plan.get("backup_plan", "")
                if backup_plan:
                    print(f"🔄 INTENTANDO PLAN B: {backup_plan}")
                    backup_result = await self.execute_backup_plan(backup_plan)
                    execution_result["backup_result"] = backup_result
            
            return execution_result
            
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout ejecutando {command}"
            print(f"⏰ {error_msg}")
            self.failed_attempts.append(error_msg)
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Error ejecutando {command}: {e}"
            print(f"❌ {error_msg}")
            self.failed_attempts.append(error_msg)
            return {"error": error_msg}
    
    async def execute_backup_plan(self, backup_plan: str) -> Dict[str, Any]:
        """Ejecuta el plan de backup"""
        
        backup_prompt = f"""
        PLAN DE BACKUP: {backup_plan}
        
        Convierte este plan en un comando específico ejecutable.
        Responde SOLO con el comando, sin explicaciones.
        """
        
        try:
            backup_command = await self.agent.query_ai(backup_prompt)
            backup_command = backup_command.strip()
            
            print(f"🔄 EJECUTANDO BACKUP: {backup_command}")
            
            result = subprocess.run(
                backup_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            return {
                "command": backup_command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def check_objective_completion(self, result: Dict[str, Any]) -> bool:
        """Verifica si se ha conseguido el objetivo"""
        
        check_prompt = f"""
        VERIFICACIÓN DE OBJETIVO:
        
        Objetivo original: {self.objective}
        Resultado de la última acción: {json.dumps(result, indent=2)}
        Tareas completadas hasta ahora: {len(self.completed_tasks)}
        
        Analiza si el objetivo se ha conseguido basándote en:
        1. El resultado de la acción ejecutada
        2. Las tareas completadas previamente
        3. La información obtenida
        
        ¿Se ha conseguido el objetivo? Responde SOLO "SÍ" o "NO" seguido de una breve explicación.
        """
        
        try:
            check_result = await self.agent.query_ai(check_prompt)
            
            # Verificar si la respuesta indica éxito
            success_indicators = ["sí", "si", "yes", "conseguido", "logrado", "completado", "éxito"]
            
            check_lower = check_result.lower()
            is_success = any(indicator in check_lower for indicator in success_indicators)
            
            print(f"🔍 VERIFICACIÓN: {check_result}")
            
            return is_success
            
        except Exception as e:
            print(f"Error verificando objetivo: {e}")
            return False
    
    async def generate_success_report(self):
        """Genera reporte de éxito"""
        
        print("\n" + "="*60)
        print("🎉 ¡OBJETIVO CONSEGUIDO!")
        print("="*60)
        print(f"🎯 Objetivo: {self.objective}")
        print(f"🔄 Intentos necesarios: {self.attempt_count}")
        print(f"✅ Tareas completadas: {len(self.completed_tasks)}")
        print(f"❌ Fallos: {len(self.failed_attempts)}")
        
        # Generar reporte detallado con IA
        report_prompt = f"""
        GENERAR REPORTE DE ÉXITO:
        
        Objetivo conseguido: {self.objective}
        Intentos: {self.attempt_count}
        Tareas completadas: {self.completed_tasks}
        
        Genera un reporte detallado del éxito incluyendo:
        1. Resumen ejecutivo
        2. Metodología utilizada
        3. Herramientas empleadas
        4. Vulnerabilidades encontradas
        5. Evidencias obtenidas
        6. Recomendaciones de seguridad
        """
        
        try:
            detailed_report = await self.agent.query_ai(report_prompt)
            
            # Guardar reporte
            report_file = f"/tmp/autonomous_success_report_{int(time.time())}.txt"
            with open(report_file, 'w') as f:
                f.write(f"REPORTE DE ÉXITO - OPERACIÓN AUTÓNOMA\n")
                f.write(f"Fecha: {time.ctime()}\n")
                f.write(f"Objetivo: {self.objective}\n")
                f.write(f"Intentos: {self.attempt_count}\n\n")
                f.write(detailed_report)
            
            print(f"📄 Reporte guardado en: {report_file}")
            
        except Exception as e:
            print(f"Error generando reporte: {e}")
    
    async def generate_failure_report(self):
        """Genera reporte de fallo"""
        
        print("\n" + "="*60)
        print("❌ OBJETIVO NO CONSEGUIDO")
        print("="*60)
        print(f"🎯 Objetivo: {self.objective}")
        print(f"🔄 Intentos realizados: {self.attempt_count}")
        print(f"✅ Tareas completadas: {len(self.completed_tasks)}")
        print(f"❌ Fallos: {len(self.failed_attempts)}")
        
        # Generar análisis de fallos con IA
        failure_prompt = f"""
        ANÁLISIS DE FALLOS:
        
        Objetivo no conseguido: {self.objective}
        Intentos: {self.attempt_count}
        Fallos: {self.failed_attempts}
        Tareas completadas: {self.completed_tasks}
        
        Analiza por qué no se pudo conseguir el objetivo:
        1. Principales obstáculos encontrados
        2. Estrategias que fallaron
        3. Posibles mejoras para futuros intentos
        4. Recomendaciones alternativas
        """
        
        try:
            failure_analysis = await self.agent.query_ai(failure_prompt)
            
            # Guardar análisis
            analysis_file = f"/tmp/autonomous_failure_analysis_{int(time.time())}.txt"
            with open(analysis_file, 'w') as f:
                f.write(f"ANÁLISIS DE FALLOS - OPERACIÓN AUTÓNOMA\n")
                f.write(f"Fecha: {time.ctime()}\n")
                f.write(f"Objetivo: {self.objective}\n")
                f.write(f"Intentos: {self.attempt_count}\n\n")
                f.write(failure_analysis)
            
            print(f"📄 Análisis guardado en: {analysis_file}")
            
        except Exception as e:
            print(f"Error generando análisis: {e}")

async def main():
    """Función principal para prueba del agente autónomo"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Agente Autónomo de Pentesting")
    parser.add_argument("--objective", type=str, required=True,
                       help="Objetivo a conseguir")
    parser.add_argument("--max-attempts", type=int, default=50,
                       help="Máximo número de intentos")
    
    args = parser.parse_args()
    
    # Verificar permisos de root
    if os.geteuid() != 0:
        print("❌ Se requieren permisos de root")
        print("Ejecuta: sudo python3 autonomous_agent.py --objective 'tu objetivo'")
        sys.exit(1)
    
    print(f"""
    🤖 AGENTE AUTÓNOMO INICIADO
    ==========================
    
    🎯 Objetivo: {args.objective}
    🔄 Máximo intentos: {args.max_attempts}
    ⚠️ SIN RESTRICCIONES DE SEGURIDAD
    
    El agente trabajará hasta conseguir el objetivo...
    """)
    
    try:
        agent = AutonomousAgent(args.objective)
        agent.max_attempts = args.max_attempts
        await agent.start_autonomous_operation()
        
    except KeyboardInterrupt:
        print("\n🛑 Operación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    asyncio.run(main())