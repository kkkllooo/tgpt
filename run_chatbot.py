#!/usr/bin/env python3
"""
🤖 Launcher simple para el Chatbot TUI
Ejecuta directamente la interfaz de chat con IA
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Función principal simplificada"""
    
    print("""
    🤖 CHATBOT IA - CONTROL TOTAL DEL SISTEMA
    =========================================
    
    ⚠️ LA IA TENDRÁ CONTROL COMPLETO DEL SISTEMA
    ⚠️ PUEDE EJECUTAR CUALQUIER COMANDO
    ⚠️ PUEDE ATACAR CUALQUIER OBJETIVO
    ⚠️ SIN RESTRICCIONES DE SEGURIDAD
    
    Iniciando interfaz de chat...
    """)
    
    # Verificar permisos de root
    if os.geteuid() != 0:
        print("❌ Se requieren permisos de root para control total")
        print("Ejecuta: sudo python3 run_chatbot.py")
        sys.exit(1)
    
    try:
        from tui.chatbot_interface import ChatbotTUI
        import curses
        
        chatbot = ChatbotTUI()
        curses.wrapper(chatbot.run)
        
    except KeyboardInterrupt:
        print("\n🛑 Chatbot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()