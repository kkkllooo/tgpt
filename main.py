#!/usr/bin/env python3
"""
🎯 Sistema de Pentesting Autónomo con TUI
Punto de entrada principal del sistema

Autor: Sistema Autónomo de Pentesting
Versión: 1.0.0
Licencia: MIT (Solo para uso ético)
"""

import sys
import os
import argparse
import asyncio
import signal
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.logger import setup_logger
from core.security import SecurityValidator
from core.database import DatabaseManager
from core.self_improvement import SelfImprovementEngine
from config.settings import Settings
from tui.main_interface import MainTUI
from agents.coordinator import CoordinatorAgent

# Banner del sistema
BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🎯 SISTEMA DE PENTESTING AUTÓNOMO CON TUI                                ║
║                                                                              ║
║    🚨 SIN RESTRICCIONES DE SEGURIDAD - USO BAJO TU RESPONSABILIDAD 🚨       ║
║                                                                              ║
║    Características:                                                          ║
║    • Interfaz TUI completa con curses                                        ║
║    • Agentes de IA especializados                                            ║
║    • Herramientas de pentesting integradas                                   ║
║    • Phishing avanzado y creación de malware                                 ║
║    • Evasión con Tor y técnicas avanzadas                                    ║
║    • Auto-mejora del sistema con IA                                          ║
║    • Memoria persistente con SQLite                                          ║
║    • Reportes automáticos en PDF/Markdown                                    ║
║                                                                              ║
║    ⚠️ PUEDE ATACAR CUALQUIER OBJETIVO - VALIDACIONES DESHABILITADAS ⚠️      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

class PentestSystem:
    """Clase principal del sistema de pentesting autónomo"""
    
    def __init__(self):
        self.logger = None
        self.db_manager = None
        self.coordinator = None
        self.tui = None
        self.settings = Settings()
        self.security_validator = SecurityValidator()
        self.improvement_engine = None
        
    def setup_signal_handlers(self):
        """Configura los manejadores de señales para cierre limpio"""
        def signal_handler(signum, frame):
            self.logger.info(f"Recibida señal {signum}, cerrando sistema...")
            self.cleanup()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def check_privileges(self):
        """Verifica que el sistema se ejecute con privilegios de root"""
        if os.geteuid() != 0:
            print("❌ Error: Este sistema requiere privilegios de root/sudo")
            print("   Ejecuta: sudo python main.py")
            sys.exit(1)
    
    def initialize_system(self):
        """Inicializa todos los componentes del sistema"""
        try:
            # Configurar logging
            self.logger = setup_logger()
            self.logger.info("Iniciando Sistema de Pentesting Autónomo")
            
            # Verificar privilegios
            self.check_privileges()
            
            # Validaciones de seguridad (DESHABILITADAS)
            # ⚠️ ADVERTENCIA: Validaciones de seguridad deshabilitadas por solicitud del usuario
            # El usuario es completamente responsable del uso ético y legal del sistema
            self.logger.warning("⚠️ VALIDACIONES DE SEGURIDAD DESHABILITADAS - USO BAJO RESPONSABILIDAD DEL USUARIO")
            
            # Inicializar base de datos
            self.db_manager = DatabaseManager()
            self.db_manager.initialize()
            
            # Configurar manejadores de señales
            self.setup_signal_handlers()
            
            # Inicializar motor de auto-mejora
            self.improvement_engine = SelfImprovementEngine(self.logger)
            
            self.logger.info("Sistema inicializado correctamente")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error durante la inicialización: {e}")
            else:
                print(f"❌ Error crítico durante la inicialización: {e}")
            return False
    
    def run_tui_mode(self):
        """Ejecuta el sistema en modo TUI Chatbot"""
        try:
            self.logger.info("Iniciando modo TUI Chatbot")
            
            print("🤖 Iniciando Chatbot TUI con control total de IA...")
            from tui.chatbot_interface import ChatbotTUI
            chatbot = ChatbotTUI()
            import curses
            curses.wrapper(chatbot.run)
            
        except Exception as e:
            self.logger.error(f"Error en modo TUI: {e}")
            raise
    
    async def run_autonomous_mode(self, target, scan_type="comprehensive"):
        """Ejecuta el sistema en modo autónomo"""
        try:
            self.logger.info(f"Iniciando modo autónomo contra objetivo: {target}")
            
            # Validar objetivo (DESHABILITADO)
            # ⚠️ Todas las validaciones de objetivo han sido deshabilitadas
            self.logger.warning(f"⚠️ Iniciando ataque contra: {target} - SIN VALIDACIONES DE SEGURIDAD")
            
            # Inicializar coordinador
            self.coordinator = CoordinatorAgent(self.db_manager, self.logger)
            
            # Ejecutar pentesting autónomo
            results = await self.coordinator.execute_autonomous_pentest(target, scan_type)
            
            self.logger.info("Pentesting autónomo completado")
            return results
            
        except Exception as e:
            self.logger.error(f"Error en modo autónomo: {e}")
            return False
    
    def cleanup(self):
        """Limpia recursos y cierra conexiones"""
        try:
            if self.logger:
                self.logger.info("Cerrando sistema...")
            
            if self.db_manager:
                self.db_manager.close()
            
            if self.tui:
                self.tui.cleanup()
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error durante la limpieza: {e}")

def parse_arguments():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Sistema de Pentesting Autónomo con TUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  sudo python main.py --tui                           # Modo TUI interactivo
  sudo python main.py --target 192.168.1.0/24 --autonomous  # Modo autónomo
  sudo python main.py --target example.com --scan-type web   # Escaneo web específico
  sudo python main.py --phishing --target-email victim@example.com  # Campaña de phishing
  sudo python main.py --malware --malware-type backdoor      # Generar malware
  sudo python main.py --self-improve --auto-apply-improvements  # Auto-mejora del sistema
  sudo python main.py --continuous-improvement --improvement-interval 12  # Mejora continua
        """
    )
    
    # Modos de operación
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--tui", action="store_true", 
                           help="Ejecutar en modo TUI interactivo")
    mode_group.add_argument("--autonomous", action="store_true",
                           help="Ejecutar en modo autónomo")
    mode_group.add_argument("--phishing", action="store_true",
                           help="Ejecutar campaña de phishing")
    mode_group.add_argument("--malware", action="store_true",
                           help="Generar malware personalizado")
    mode_group.add_argument("--self-improve", action="store_true",
                           help="Ejecutar análisis y mejora automática del sistema")
    mode_group.add_argument("--continuous-improvement", action="store_true",
                           help="Iniciar mejora continua del sistema")
    
    # Objetivos
    parser.add_argument("--target", type=str,
                       help="Objetivo del pentesting (IP, rango CIDR, dominio)")
    parser.add_argument("--target-email", type=str,
                       help="Email objetivo para phishing")
    parser.add_argument("--target-list", type=str,
                       help="Archivo con lista de objetivos")
    
    # Tipos de escaneo
    parser.add_argument("--scan-type", choices=["comprehensive", "web", "network", "wireless"],
                       default="comprehensive", help="Tipo de escaneo a realizar")
    
    # Configuración de phishing
    parser.add_argument("--phishing-template", type=str,
                       help="Plantilla de phishing a usar")
    parser.add_argument("--phishing-domain", type=str,
                       help="Dominio para campaña de phishing")
    
    # Configuración de malware
    parser.add_argument("--malware-type", choices=["backdoor", "trojan", "ransomware", "keylogger"],
                       help="Tipo de malware a generar")
    parser.add_argument("--payload-format", choices=["exe", "dll", "ps1", "py", "sh"],
                       default="exe", help="Formato del payload")
    
    # Opciones generales
    parser.add_argument("--output-dir", type=str, default="./reports",
                       help="Directorio de salida para reportes")
    parser.add_argument("--config", type=str, default="./config/settings.yaml",
                       help="Archivo de configuración")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Modo verbose")
    parser.add_argument("--debug", action="store_true",
                       help="Modo debug")
    parser.add_argument("--improvement-interval", type=int, default=24,
                       help="Intervalo en horas para mejora continua (default: 24)")
    parser.add_argument("--auto-apply-improvements", action="store_true",
                       help="Aplicar mejoras automáticamente sin confirmación")
    
    return parser.parse_args()

async def main():
    """Función principal del sistema"""
    # Mostrar banner
    print(BANNER)
    
    # Parsear argumentos
    args = parse_arguments()
    
    # Inicializar sistema
    system = PentestSystem()
    
    if not system.initialize_system():
        print("❌ Error: No se pudo inicializar el sistema")
        sys.exit(1)
    
    try:
        # Ejecutar según el modo seleccionado
        if args.tui:
            system.run_tui_mode()
            
        elif args.autonomous:
            if not args.target:
                print("❌ Error: Se requiere especificar un objetivo con --target")
                sys.exit(1)
            
            results = await system.run_autonomous_mode(args.target, args.scan_type)
            if results:
                print("✅ Pentesting autónomo completado exitosamente")
            else:
                print("❌ Error durante el pentesting autónomo")
                
        elif args.phishing:
            if not args.target_email:
                print("❌ Error: Se requiere especificar un email objetivo con --target-email")
                sys.exit(1)
            
            from agents.phishing import PhishingAgent
            phishing_agent = PhishingAgent(system.db_manager, system.logger)
            await phishing_agent.create_campaign(args.target_email, args.phishing_template)
            
        elif args.malware:
            if not args.malware_type:
                print("❌ Error: Se requiere especificar el tipo de malware con --malware-type")
                sys.exit(1)
            
            from agents.malware import MalwareAgent
            malware_agent = MalwareAgent(system.db_manager, system.logger)
            await malware_agent.generate_payload(args.malware_type, args.payload_format)
            
        elif args.self_improve:
            print("🔧 Iniciando análisis y mejora automática del sistema...")
            
            # Analizar rendimiento del sistema
            analysis = await system.improvement_engine.analyze_system_performance()
            
            if "error" not in analysis:
                print("📊 Análisis de rendimiento completado")
                
                # Generar mejoras
                improvements = await system.improvement_engine.generate_code_improvements(analysis)
                
                print(f"💡 Se generaron {len(improvements)} mejoras potenciales")
                
                # Mostrar mejoras encontradas
                for i, improvement in enumerate(improvements, 1):
                    print(f"\n{i}. {improvement['description']}")
                    print(f"   Tipo: {improvement['type']}")
                    print(f"   Impacto: {improvement.get('impact', 'No especificado')}")
                
                # Aplicar mejoras si se especifica
                if args.auto_apply_improvements:
                    applied_count = 0
                    for improvement in improvements:
                        if await system.improvement_engine.implement_improvement(improvement, auto_apply=True):
                            applied_count += 1
                    
                    print(f"✅ Se aplicaron {applied_count} mejoras automáticamente")
                else:
                    print("\n💡 Usa --auto-apply-improvements para aplicar mejoras automáticamente")
            else:
                print(f"❌ Error en análisis: {analysis['error']}")
                
        elif args.continuous_improvement:
            print(f"🔄 Iniciando mejora continua cada {args.improvement_interval} horas...")
            print("   Presiona Ctrl+C para detener")
            
            await system.improvement_engine.run_continuous_improvement(args.improvement_interval)
    
    except KeyboardInterrupt:
        print("\n🛑 Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        system.cleanup()

if __name__ == "__main__":
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    # Ejecutar sistema
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrumpido")
        sys.exit(0)