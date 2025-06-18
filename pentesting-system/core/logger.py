"""
Sistema de logging para el sistema de pentesting autónomo
"""

import os
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logger(name: str = "pentest-system", level: str = "INFO") -> logging.Logger:
    """Configura el sistema de logging"""
    
    # Crear directorio de logs
    log_dir = Path("/var/log/pentest-system")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivo
    log_file = log_dir / f"{name}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger