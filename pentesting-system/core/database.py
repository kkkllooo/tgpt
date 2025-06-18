"""
Gestor de base de datos SQLite para el sistema de pentesting
"""

import sqlite3
import json
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import threading

class DatabaseManager:
    """Gestor de base de datos para almacenar resultados y configuraciones"""
    
    def __init__(self, db_path: str = "/var/lib/pentest-system/pentest.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.lock = threading.Lock()
    
    def initialize(self):
        """Inicializa la base de datos y crea tablas"""
        try:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            
            self._create_tables()
            
        except Exception as e:
            raise Exception(f"Error inicializando base de datos: {e}")
    
    def _create_tables(self):
        """Crea las tablas necesarias"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                results TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                status TEXT DEFAULT 'completed'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT UNIQUE NOT NULL,
                target_email TEXT NOT NULL,
                template_type TEXT NOT NULL,
                status TEXT DEFAULT 'created',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                sent_at DATETIME,
                clicks INTEGER DEFAULT 0,
                credentials_captured INTEGER DEFAULT 0,
                campaign_data TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS malware_payloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload_id TEXT UNIQUE NOT NULL,
                malware_type TEXT NOT NULL,
                platform TEXT NOT NULL,
                file_path TEXT NOT NULL,
                config TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT,
                compiled BOOLEAN DEFAULT FALSE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                improvement_id TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                improvement_type TEXT NOT NULL,
                code_changes TEXT,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'applied',
                backup_id TEXT,
                impact_score REAL DEFAULT 0.0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS agent_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        with self.lock:
            cursor = self.connection.cursor()
            for table_sql in tables:
                cursor.execute(table_sql)
            self.connection.commit()
    
    async def save_scan_results(self, results: Dict[str, Any]) -> bool:
        """Guarda resultados de escaneo"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO scan_results (target, scan_type, results, agent_name, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    results.get("target", ""),
                    results.get("technique", "unknown"),
                    json.dumps(results),
                    results.get("agent_name", "unknown"),
                    results.get("status", "completed")
                ))
                self.connection.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando resultados de escaneo: {e}")
            return False
    
    async def save_campaign(self, campaign: Dict[str, Any]) -> bool:
        """Guarda campaña de phishing"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO phishing_campaigns 
                    (campaign_id, target_email, template_type, status, campaign_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    campaign["id"],
                    campaign["target_email"],
                    campaign["template_type"],
                    campaign["status"],
                    json.dumps(campaign)
                ))
                self.connection.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando campaña: {e}")
            return False
    
    async def update_campaign(self, campaign: Dict[str, Any]) -> bool:
        """Actualiza campaña de phishing"""
        return await self.save_campaign(campaign)
    
    async def save_payload(self, payload_info: Dict[str, Any]) -> bool:
        """Guarda información de payload"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO malware_payloads 
                    (payload_id, malware_type, platform, file_path, config, hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    payload_info["id"],
                    payload_info["type"],
                    payload_info["platform"],
                    payload_info["file_path"],
                    json.dumps(payload_info["config"]),
                    payload_info["hash"]
                ))
                self.connection.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando payload: {e}")
            return False
    
    async def save_improvement(self, improvement: Dict[str, Any]) -> bool:
        """Guarda mejora del sistema"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO system_improvements 
                    (improvement_id, description, improvement_type, code_changes, backup_id, impact_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    improvement.get("id", ""),
                    improvement.get("description", ""),
                    improvement.get("type", ""),
                    json.dumps(improvement.get("code", "")),
                    improvement.get("backup_id", ""),
                    improvement.get("impact_score", 0.0)
                ))
                self.connection.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando mejora: {e}")
            return False
    
    async def save_conversation(self, agent_name: str, prompt: str, response: str, context: Dict = None) -> bool:
        """Guarda conversación de agente"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO agent_conversations (agent_name, prompt, response, context)
                    VALUES (?, ?, ?, ?)
                """, (
                    agent_name,
                    prompt,
                    response,
                    json.dumps(context) if context else None
                ))
                self.connection.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando conversación: {e}")
            return False
    
    def get_scan_results(self, target: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene resultados de escaneos"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                if target:
                    cursor.execute("""
                        SELECT * FROM scan_results WHERE target = ? 
                        ORDER BY timestamp DESC LIMIT ?
                    """, (target, limit))
                else:
                    cursor.execute("""
                        SELECT * FROM scan_results 
                        ORDER BY timestamp DESC LIMIT ?
                    """, (limit,))
                
                rows = cursor.fetchall()
                results = []
                
                for row in rows:
                    result = dict(row)
                    try:
                        result["results"] = json.loads(result["results"])
                    except:
                        pass
                    results.append(result)
                
                return results
                
        except Exception as e:
            print(f"Error obteniendo resultados: {e}")
            return []
    
    def get_campaigns(self, status: str = None) -> List[Dict[str, Any]]:
        """Obtiene campañas de phishing"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                if status:
                    cursor.execute("""
                        SELECT * FROM phishing_campaigns WHERE status = ?
                        ORDER BY created_at DESC
                    """, (status,))
                else:
                    cursor.execute("""
                        SELECT * FROM phishing_campaigns
                        ORDER BY created_at DESC
                    """)
                
                rows = cursor.fetchall()
                campaigns = []
                
                for row in rows:
                    campaign = dict(row)
                    try:
                        campaign["campaign_data"] = json.loads(campaign["campaign_data"])
                    except:
                        pass
                    campaigns.append(campaign)
                
                return campaigns
                
        except Exception as e:
            print(f"Error obteniendo campañas: {e}")
            return []
    
    def get_payloads(self, malware_type: str = None) -> List[Dict[str, Any]]:
        """Obtiene payloads generados"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                if malware_type:
                    cursor.execute("""
                        SELECT * FROM malware_payloads WHERE malware_type = ?
                        ORDER BY created_at DESC
                    """, (malware_type,))
                else:
                    cursor.execute("""
                        SELECT * FROM malware_payloads
                        ORDER BY created_at DESC
                    """)
                
                rows = cursor.fetchall()
                payloads = []
                
                for row in rows:
                    payload = dict(row)
                    try:
                        payload["config"] = json.loads(payload["config"])
                    except:
                        pass
                    payloads.append(payload)
                
                return payloads
                
        except Exception as e:
            print(f"Error obteniendo payloads: {e}")
            return []
    
    def get_improvements(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene mejoras aplicadas"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT * FROM system_improvements
                    ORDER BY applied_at DESC LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                improvements = []
                
                for row in rows:
                    improvement = dict(row)
                    try:
                        improvement["code_changes"] = json.loads(improvement["code_changes"])
                    except:
                        pass
                    improvements.append(improvement)
                
                return improvements
                
        except Exception as e:
            print(f"Error obteniendo mejoras: {e}")
            return []
    
    def close(self):
        """Cierra conexión a la base de datos"""
        if self.connection:
            self.connection.close()