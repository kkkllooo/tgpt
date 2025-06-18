"""
Clase base para todos los agentes de IA
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests

class BaseAgent:
    """Clase base para agentes de IA especializados"""
    
    def __init__(self, name: str, db_manager, logger):
        self.name = name
        self.db_manager = db_manager
        self.logger = logger
        self.ai_provider = "groq"  # Proveedor por defecto (gratuito)
        self.api_key = None
        self.conversation_history = []
        self.capabilities = []
        
    async def initialize(self):
        """Inicializa el agente"""
        self.logger.info(f"Inicializando agente {self.name}")
        await self._load_configuration()
        await self._setup_ai_provider()
    
    async def _load_configuration(self):
        """Carga configuración específica del agente"""
        # Cargar desde base de datos o archivo de configuración
        pass
    
    async def _setup_ai_provider(self):
        """Configura proveedor de IA"""
        # Configurar API keys y endpoints
        pass
    
    async def query_ai(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Consulta al proveedor de IA"""
        try:
            # Preparar contexto
            full_prompt = self._prepare_prompt(prompt, context)
            
            # Consultar según el proveedor
            if self.ai_provider == "groq":
                response = await self._query_groq(full_prompt)
            elif self.ai_provider == "openai":
                response = await self._query_openai(full_prompt)
            elif self.ai_provider == "anthropic":
                response = await self._query_anthropic(full_prompt)
            else:
                response = await self._query_fallback(full_prompt)
            
            # Guardar en historial
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "response": response,
                "context": context
            })
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error consultando IA: {e}")
            return "Error: No se pudo obtener respuesta de IA"
    
    def _prepare_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Prepara prompt con contexto del agente"""
        system_prompt = f"""
Eres {self.name}, un agente de IA especializado en pentesting ético.

Capacidades: {', '.join(self.capabilities)}

Contexto del sistema:
- Solo realizar actividades de pentesting ético y autorizado
- Proporcionar respuestas técnicas precisas
- Considerar aspectos de seguridad y legalidad
- Usar técnicas de evasión cuando sea apropiado

"""
        
        if context:
            system_prompt += f"\nContexto adicional: {json.dumps(context, indent=2)}\n"
        
        return system_prompt + f"\nConsulta: {prompt}"
    
    async def _query_groq(self, prompt: str) -> str:
        """Consulta a Groq (API gratuita)"""
        try:
            # Usar API de Groq (requiere key gratuita)
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.api_key or 'demo-key'}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2048,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return await self._query_fallback(prompt)
                
        except Exception as e:
            self.logger.warning(f"Error con Groq: {e}")
            return await self._query_fallback(prompt)
    
    async def _query_openai(self, prompt: str) -> str:
        """Consulta a OpenAI"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.warning(f"Error con OpenAI: {e}")
            return await self._query_fallback(prompt)
    
    async def _query_anthropic(self, prompt: str) -> str:
        """Consulta a Anthropic Claude"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            self.logger.warning(f"Error con Anthropic: {e}")
            return await self._query_fallback(prompt)
    
    async def _query_fallback(self, prompt: str) -> str:
        """Respuesta de fallback cuando no hay IA disponible"""
        # Respuestas básicas basadas en patrones
        if "nmap" in prompt.lower():
            return "Ejecutar: nmap -sS -sV -O <target>"
        elif "phishing" in prompt.lower():
            return "Crear campaña de phishing personalizada con plantillas apropiadas"
        elif "malware" in prompt.lower():
            return "Generar payload usando técnicas de evasión y ofuscación"
        elif "exploit" in prompt.lower():
            return "Buscar exploits conocidos para vulnerabilidades identificadas"
        else:
            return "Analizar objetivo y seleccionar herramientas apropiadas"
    
    async def analyze_target(self, target: str) -> Dict[str, Any]:
        """Analiza un objetivo (implementar en subclases)"""
        raise NotImplementedError("Subclases deben implementar analyze_target")
    
    async def execute_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una acción específica (implementar en subclases)"""
        raise NotImplementedError("Subclases deben implementar execute_action")
    
    def get_capabilities(self) -> List[str]:
        """Retorna capacidades del agente"""
        return self.capabilities
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Retorna historial de conversación"""
        return self.conversation_history
    
    def clear_history(self):
        """Limpia historial de conversación"""
        self.conversation_history.clear()
    
    def cleanup(self):
        """Limpia recursos del agente"""
        self.logger.info(f"Limpiando agente {self.name}")
        self.clear_history()