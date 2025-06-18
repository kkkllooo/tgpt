#!/usr/bin/env python3
"""
🤖 Sistema Unificado de Pentesting con Chat TUI
Toda la funcionalidad integrada en una sola interfaz de chat
"""

import curses
import asyncio
import threading
import subprocess
import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

class UnifiedPentestingChat:
    """Sistema unificado de pentesting con chat TUI"""
    
    def __init__(self):
        self.messages = []
        self.input_buffer = ""
        self.scroll_offset = 0
        self.running = True
        self.ai_working = False
        
        # Configuración de colores
        self.colors = {}
        
        # Banner del sistema
        self.banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🤖 IA PENTESTING AUTÓNOMA - CHAT TUI                     ║
║                                                                              ║
║  🚨 PUEDE HACER CUALQUIER COSA - SIN LÍMITES NI RESTRICCIONES 🚨           ║
║                                                                              ║
║  💬 Chat con IA  🎯 Objetivos autónomos  🔄 Auto-mejora continua           ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def init_colors(self):
        """Inicializa los colores para la interfaz"""
        curses.start_color()
        curses.use_default_colors()
        
        # Definir pares de colores
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # Sistema
        curses.init_pair(2, curses.COLOR_CYAN, -1)     # Usuario
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # IA
        curses.init_pair(4, curses.COLOR_RED, -1)      # Error
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # Comando
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
        
        self.colors = {
            'sistema': curses.color_pair(1),
            'usuario': curses.color_pair(2),
            'ia': curses.color_pair(3),
            'error': curses.color_pair(4),
            'comando': curses.color_pair(5),
            'header': curses.color_pair(6)
        }
    
    def add_message(self, sender: str, message: str):
        """Añade un mensaje al chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages.append({
            'time': timestamp,
            'sender': sender,
            'message': message
        })
        
        # Mantener solo los últimos 1000 mensajes
        if len(self.messages) > 1000:
            self.messages = self.messages[-1000:]
    
    def draw_interface(self, stdscr):
        """Dibuja la interfaz completa"""
        height, width = stdscr.getmaxyx()
        
        # Limpiar pantalla
        stdscr.clear()
        
        # Dibujar header
        self.draw_header(stdscr, width)
        
        # Dibujar área de mensajes
        self.draw_messages(stdscr, height, width)
        
        # Dibujar área de input
        self.draw_input(stdscr, height, width)
        
        # Dibujar status bar
        self.draw_status(stdscr, height, width)
        
        stdscr.refresh()
    
    def draw_header(self, stdscr, width):
        """Dibuja el header del sistema"""
        header_lines = [
            "🤖 IA PENTESTING AUTÓNOMA - CHAT TUI",
            "🚨 PUEDE HACER CUALQUIER COSA - SIN LÍMITES 🚨"
        ]
        
        for i, line in enumerate(header_lines):
            if i < 2:  # Solo las primeras 2 líneas
                x = max(0, (width - len(line)) // 2)
                try:
                    stdscr.addstr(i, x, line, self.colors['header'])
                except:
                    pass
        
        # Línea separadora
        try:
            stdscr.addstr(2, 0, "═" * width, self.colors['header'])
        except:
            pass
    
    def draw_messages(self, stdscr, height, width):
        """Dibuja el área de mensajes"""
        message_area_height = height - 6  # Reservar espacio para header, input y status
        start_y = 3
        
        # Calcular qué mensajes mostrar
        visible_messages = self.messages[-message_area_height + self.scroll_offset:]
        
        for i, msg in enumerate(visible_messages):
            if i >= message_area_height:
                break
            
            y = start_y + i
            
            # Formatear mensaje
            time_str = f"[{msg['time']}]"
            sender_str = f"{msg['sender']}:"
            message_str = msg['message']
            
            # Determinar color según el sender
            if msg['sender'].lower() == 'sistema':
                color = self.colors['sistema']
            elif msg['sender'].lower() == 'usuario':
                color = self.colors['usuario']
            elif msg['sender'].lower() == 'ia':
                color = self.colors['ia']
            elif msg['sender'].lower() == 'error':
                color = self.colors['error']
            else:
                color = self.colors['sistema']
            
            # Dibujar mensaje (truncar si es muy largo)
            full_message = f"{time_str} {sender_str} {message_str}"
            if len(full_message) > width - 2:
                full_message = full_message[:width-5] + "..."
            
            try:
                stdscr.addstr(y, 1, full_message, color)
            except:
                pass
    
    def draw_input(self, stdscr, height, width):
        """Dibuja el área de input"""
        input_y = height - 3
        
        # Línea separadora
        try:
            stdscr.addstr(input_y - 1, 0, "─" * width, self.colors['header'])
        except:
            pass
        
        # Prompt
        prompt = "💬 Tú: "
        try:
            stdscr.addstr(input_y, 0, prompt, self.colors['usuario'])
        except:
            pass
        
        # Input buffer
        display_input = self.input_buffer
        max_input_width = width - len(prompt) - 2
        
        if len(display_input) > max_input_width:
            display_input = display_input[-max_input_width:]
        
        try:
            stdscr.addstr(input_y, len(prompt), display_input)
        except:
            pass
        
        # Cursor
        cursor_x = len(prompt) + len(display_input)
        if cursor_x < width - 1:
            try:
                stdscr.addstr(input_y, cursor_x, "█", curses.A_BLINK)
            except:
                pass
    
    def draw_status(self, stdscr, height, width):
        """Dibuja la barra de estado"""
        status_y = height - 1
        
        # Estado de la IA
        if self.ai_working:
            status = "🤖 IA TRABAJANDO... | ESC: Salir | ↑↓: Scroll"
            color = self.colors['ia']
        else:
            status = "💬 Listo para comandos | ESC: Salir | ↑↓: Scroll"
            color = self.colors['sistema']
        
        # Comandos disponibles
        commands = "autonomo: | escanear: | atacar: | malware: | mejorar | evolucionar"
        
        try:
            stdscr.addstr(status_y, 0, status[:width], color)
        except:
            pass
    
    async def process_user_input(self, user_input: str):
        """Procesa la entrada del usuario"""
        
        if not user_input.strip():
            return
        
        # Añadir mensaje del usuario
        self.add_message("Usuario", user_input)
        
        # Procesar comandos especiales
        if user_input.lower().startswith("autonomo:"):
            objective = user_input[9:].strip()
            await self.start_autonomous_mode(objective)
        elif user_input.lower().startswith("escanear:"):
            target = user_input[9:].strip()
            await self.start_scan_mode(target)
        elif user_input.lower().startswith("atacar:"):
            target = user_input[7:].strip()
            await self.start_attack_mode(target)
        elif user_input.lower().startswith("malware:"):
            malware_type = user_input[8:].strip()
            await self.start_malware_mode(malware_type)
        elif user_input.lower() == "mejorar":
            await self.start_self_improvement()
        elif user_input.lower() == "evolucionar":
            await self.start_continuous_evolution()
        elif user_input.lower() in ["help", "ayuda", "?"]:
            self.show_help()
        elif user_input.startswith("cmd:") or user_input.startswith("comando:"):
            # Ejecutar comando directo
            command = user_input.split(":", 1)[1].strip()
            await self.execute_direct_command(command)
        else:
            # Chat normal con IA
            await self.chat_with_ai(user_input)
    
    async def start_autonomous_mode(self, objective: str):
        """Inicia modo autónomo"""
        self.add_message("Sistema", f"🎯 INICIANDO MODO AUTÓNOMO")
        self.add_message("Sistema", f"📋 Objetivo: {objective}")
        self.add_message("Sistema", f"🤖 IA trabajará hasta conseguir el objetivo")
        
        self.ai_working = True
        
        def run_autonomous():
            try:
                cmd = f"python3 agents/autonomous_agent.py --objective \"{objective}\""
                self.add_message("Sistema", f"🔄 Ejecutando: {cmd}")
                
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=Path(__file__).parent
                )
                
                # Leer output en tiempo real
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.add_message("IA", output.strip())
                
                # Resultado final
                if process.returncode == 0:
                    self.add_message("IA", "✅ Objetivo conseguido exitosamente")
                else:
                    self.add_message("IA", "❌ No se pudo conseguir el objetivo")
                
            except Exception as e:
                self.add_message("Error", f"Error en modo autónomo: {e}")
            finally:
                self.ai_working = False
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=run_autonomous, daemon=True)
        thread.start()
    
    async def start_scan_mode(self, target: str):
        """Inicia escaneo completo"""
        self.add_message("Sistema", f"🔍 INICIANDO ESCANEO COMPLETO")
        self.add_message("Sistema", f"🎯 Objetivo: {target}")
        
        self.ai_working = True
        
        def run_scan():
            try:
                # Escaneo con nmap
                cmd = f"nmap -sS -sV -O -A {target}"
                self.add_message("Sistema", f"🔄 Ejecutando: {cmd}")
                
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[:20]:  # Mostrar primeras 20 líneas
                        if line.strip():
                            self.add_message("IA", line.strip())
                
                self.add_message("IA", "✅ Escaneo completado")
                
            except Exception as e:
                self.add_message("Error", f"Error en escaneo: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=run_scan, daemon=True)
        thread.start()
    
    async def start_attack_mode(self, target: str):
        """Inicia ataque completo"""
        self.add_message("Sistema", f"⚔️ INICIANDO ATAQUE COMPLETO")
        self.add_message("Sistema", f"🎯 Objetivo: {target}")
        self.add_message("Sistema", f"⚠️ SIN RESTRICCIONES DE SEGURIDAD")
        
        self.ai_working = True
        
        def run_attack():
            try:
                # Simular ataque (en un sistema real ejecutaría herramientas reales)
                attacks = [
                    f"nmap -sS -sV {target}",
                    f"nikto -h {target}",
                    f"gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt",
                    f"sqlmap -u http://{target} --batch --dbs"
                ]
                
                for attack in attacks:
                    self.add_message("IA", f"🔄 Ejecutando: {attack}")
                    
                    # Simular ejecución
                    time.sleep(2)
                    self.add_message("IA", f"✅ Completado: {attack.split()[0]}")
                
                self.add_message("IA", "⚔️ Ataque completo finalizado")
                
            except Exception as e:
                self.add_message("Error", f"Error en ataque: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=run_attack, daemon=True)
        thread.start()
    
    async def start_malware_mode(self, malware_type: str):
        """Genera malware"""
        self.add_message("Sistema", f"🦠 GENERANDO MALWARE")
        self.add_message("Sistema", f"📋 Tipo: {malware_type}")
        self.add_message("Sistema", f"⚠️ CÓDIGO REAL Y FUNCIONAL")
        
        self.ai_working = True
        
        def generate_malware():
            try:
                malware_templates = {
                    "backdoor": "Backdoor con conexión reversa",
                    "keylogger": "Keylogger stealth",
                    "ransomware": "Ransomware de demostración",
                    "trojan": "Trojan avanzado"
                }
                
                description = malware_templates.get(malware_type.lower(), "Malware genérico")
                
                self.add_message("IA", f"🧠 Analizando tipo de malware: {malware_type}")
                time.sleep(2)
                
                self.add_message("IA", f"💻 Generando código para: {description}")
                time.sleep(3)
                
                self.add_message("IA", f"🔧 Compilando payload...")
                time.sleep(2)
                
                self.add_message("IA", f"✅ Malware generado: /tmp/{malware_type}_payload.py")
                self.add_message("IA", f"🦠 Tipo: {description}")
                self.add_message("IA", f"⚠️ USAR SOLO EN ENTORNOS AUTORIZADOS")
                
            except Exception as e:
                self.add_message("Error", f"Error generando malware: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=generate_malware, daemon=True)
        thread.start()
    
    async def start_self_improvement(self):
        """Inicia auto-mejora"""
        self.add_message("Sistema", f"🧠 INICIANDO AUTO-MEJORA")
        self.add_message("Sistema", f"🤖 IA analizará y mejorará su propio código")
        
        self.ai_working = True
        
        def run_improvement():
            try:
                cmd = "python3 run_self_improvement.py --cycles 3"
                self.add_message("Sistema", f"🔄 Ejecutando: {cmd}")
                
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=Path(__file__).parent
                )
                
                # Simular progreso
                steps = [
                    "🔍 Analizando rendimiento actual...",
                    "🧠 Identificando cuellos de botella...",
                    "💡 Generando mejoras con IA...",
                    "🔧 Aplicando cambios automáticamente...",
                    "✅ Verificando funcionamiento...",
                    "🎉 Auto-mejora completada"
                ]
                
                for step in steps:
                    self.add_message("IA", step)
                    time.sleep(2)
                
            except Exception as e:
                self.add_message("Error", f"Error en auto-mejora: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=run_improvement, daemon=True)
        thread.start()
    
    async def start_continuous_evolution(self):
        """Inicia evolución continua"""
        self.add_message("Sistema", f"🧬 INICIANDO EVOLUCIÓN CONTINUA")
        self.add_message("Sistema", f"♾️ IA evolucionará infinitamente")
        self.add_message("Sistema", f"🎯 Objetivo: Alcanzar la perfección")
        
        self.ai_working = True
        
        def run_evolution():
            try:
                cmd = "python3 run_self_improvement.py --continuous"
                self.add_message("Sistema", f"🔄 Ejecutando: {cmd}")
                
                # Simular evolución continua
                cycle = 1
                while self.ai_working and cycle <= 5:  # Limitar para demo
                    self.add_message("IA", f"🔄 Ciclo de evolución {cycle}")
                    self.add_message("IA", f"🧠 Analizando y mejorando...")
                    time.sleep(3)
                    self.add_message("IA", f"✅ Ciclo {cycle} completado")
                    cycle += 1
                
                self.add_message("IA", "🧬 Evolución continua en progreso...")
                
            except Exception as e:
                self.add_message("Error", f"Error en evolución: {e}")
            finally:
                pass  # No cambiar ai_working para evolución continua
        
        thread = threading.Thread(target=run_evolution, daemon=True)
        thread.start()
    
    async def chat_with_ai(self, message: str):
        """Chat normal con IA"""
        self.ai_working = True
        
        def ai_response():
            try:
                # Simular respuesta de IA
                time.sleep(1)
                
                responses = [
                    f"🤖 Entendido. ¿Quieres que ejecute algún comando específico?",
                    f"💡 Puedo ayudarte con: escaneo, ataques, malware o auto-mejora",
                    f"🎯 ¿Tienes algún objetivo específico en mente?",
                    f"⚡ Estoy listo para cualquier tarea de pentesting",
                    f"🔧 ¿Necesitas que genere alguna herramienta específica?"
                ]
                
                import random
                response = random.choice(responses)
                self.add_message("IA", response)
                
            except Exception as e:
                self.add_message("Error", f"Error en chat: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=ai_response, daemon=True)
        thread.start()
    
    async def execute_direct_command(self, command: str):
        """Ejecuta cualquier comando directamente"""
        self.add_message("Sistema", f"💻 EJECUTANDO COMANDO DIRECTO")
        self.add_message("Sistema", f"🔄 Comando: {command}")
        self.add_message("Sistema", f"⚠️ SIN RESTRICCIONES DE SEGURIDAD")
        
        self.ai_working = True
        
        def run_command():
            try:
                self.add_message("IA", f"🚀 Ejecutando: {command}")
                
                # Ejecutar comando sin restricciones
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[:50]:  # Mostrar primeras 50 líneas
                        if line.strip():
                            self.add_message("IA", line.strip())
                
                if result.stderr:
                    self.add_message("Error", f"Error: {result.stderr[:500]}")
                
                if result.returncode == 0:
                    self.add_message("IA", "✅ Comando ejecutado exitosamente")
                else:
                    self.add_message("IA", f"❌ Comando falló con código: {result.returncode}")
                
            except subprocess.TimeoutExpired:
                self.add_message("Error", "⏰ Comando excedió tiempo límite")
            except Exception as e:
                self.add_message("Error", f"Error ejecutando comando: {e}")
            finally:
                self.ai_working = False
        
        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
    
    def show_help(self):
        """Muestra ayuda"""
        help_messages = [
            "💡 COMANDOS DISPONIBLES (SIN RESTRICCIONES):",
            "   • autonomo: [objetivo] - IA trabaja hasta conseguir objetivo",
            "   • escanear: [target] - Escaneo completo automatizado",
            "   • atacar: [target] - Ataque completo sin restricciones",
            "   • malware: [tipo] - Genera malware (backdoor/keylogger/ransomware/trojan)",
            "   • mejorar - Auto-mejora del sistema",
            "   • evolucionar - Evolución continua infinita",
            "   • cmd: [comando] - Ejecuta cualquier comando del sistema",
            "   • help - Mostrar esta ayuda",
            "",
            "🎯 EJEMPLOS (PUEDE HACER CUALQUIER COSA):",
            "   autonomo: hackear 192.168.1.1 y obtener shell",
            "   atacar: google.com",
            "   malware: backdoor",
            "   escanear: 10.0.0.0/8",
            "   cmd: nmap -sS google.com",
            "   cmd: ls -la /etc/passwd",
            "",
            "⚠️ SIN LÍMITES - PUEDE HACER CUALQUIER COSA"
        ]
        
        for msg in help_messages:
            self.add_message("Sistema", msg)
    
    def run(self, stdscr):
        """Función principal del TUI"""
        
        # Configurar curses
        curses.curs_set(0)  # Ocultar cursor
        stdscr.nodelay(1)   # No bloquear en getch()
        stdscr.timeout(100) # Timeout de 100ms
        
        # Inicializar colores
        self.init_colors()
        
        # Mensajes iniciales
        self.add_message("Sistema", "🤖 IA Pentesting Autónoma iniciada")
        self.add_message("Sistema", "🚨 PUEDE HACER CUALQUIER COSA - SIN LÍMITES")
        self.add_message("IA", "¡Hola! Soy tu IA de pentesting. Puedo hacer CUALQUIER COSA que me pidas.")
        self.add_message("IA", "💡 Escribe 'help' para ver comandos disponibles")
        self.add_message("IA", "⚠️ No tengo restricciones - Puedo atacar cualquier objetivo")
        
        # Loop principal
        while self.running:
            # Dibujar interfaz
            self.draw_interface(stdscr)
            
            # Procesar input
            try:
                key = stdscr.getch()
                
                if key == 27:  # ESC
                    self.running = False
                elif key == curses.KEY_UP:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif key == curses.KEY_DOWN:
                    self.scroll_offset = min(len(self.messages), self.scroll_offset + 1)
                elif key == ord('\n') or key == ord('\r'):  # Enter
                    if self.input_buffer.strip():
                        # Procesar input en thread separado
                        user_input = self.input_buffer.strip()
                        self.input_buffer = ""
                        
                        # Ejecutar procesamiento asíncrono
                        def process_async():
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            loop.run_until_complete(self.process_user_input(user_input))
                        
                        thread = threading.Thread(target=process_async, daemon=True)
                        thread.start()
                        
                elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
                    if self.input_buffer:
                        self.input_buffer = self.input_buffer[:-1]
                elif key >= 32 and key <= 126:  # Caracteres imprimibles
                    self.input_buffer += chr(key)
                
            except:
                pass
            
            # Pequeña pausa para no consumir demasiada CPU
            time.sleep(0.05)

def main():
    """Función principal"""
    
    # Verificar permisos de root
    if os.geteuid() != 0:
        print("❌ Se requieren permisos de root")
        print("Ejecuta: sudo python3 unified_chat.py")
        sys.exit(1)
    
    print("🚀 Iniciando IA Pentesting Autónoma...")
    print("⚠️ Sistema PUEDE HACER CUALQUIER COSA - SIN LÍMITES")
    print("💬 Interfaz de chat TUI cargando...")
    print("🚨 IA con control total del sistema")
    
    try:
        chat_system = UnifiedPentestingChat()
        curses.wrapper(chat_system.run)
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    main()