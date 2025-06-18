#!/usr/bin/env python3
"""
🧠 Sistema de Auto-mejora Autónoma
La IA analiza su propio rendimiento y se mejora automáticamente
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.self_improvement import SelfImprovementEngine
from core.logger import setup_logger

class AutonomousSelfImprovement:
    """Sistema de auto-mejora completamente autónomo"""
    
    def __init__(self):
        self.logger = setup_logger("self-improvement")
        self.improvement_engine = SelfImprovementEngine(self.logger)
        self.improvement_cycles = 0
        self.max_cycles = 10
        self.improvements_applied = []
        
    async def start_continuous_improvement(self):
        """Inicia el ciclo continuo de auto-mejora"""
        
        print(f"""
        🧠 SISTEMA DE AUTO-MEJORA AUTÓNOMA INICIADO
        ==========================================
        
        🤖 La IA analizará su propio rendimiento
        🔧 Generará mejoras automáticamente
        ⚡ Aplicará cambios sin intervención humana
        🔄 Ciclo continuo hasta perfección
        
        Máximo {self.max_cycles} ciclos de mejora
        """)
        
        while self.improvement_cycles < self.max_cycles:
            self.improvement_cycles += 1
            
            print(f"\n🔄 CICLO DE MEJORA {self.improvement_cycles}/{self.max_cycles}")
            print("=" * 50)
            
            try:
                # 1. Analizar rendimiento actual
                print("🔍 Analizando rendimiento del sistema...")
                analysis = await self.improvement_engine.analyze_system_performance()
                
                if "error" in analysis:
                    print(f"❌ Error en análisis: {analysis['error']}")
                    continue
                
                print("✅ Análisis completado")
                self.print_analysis_summary(analysis)
                
                # 2. Generar mejoras
                print("\n🧠 Generando mejoras con IA...")
                improvements = await self.improvement_engine.generate_code_improvements(analysis)
                
                if not improvements:
                    print("ℹ️ No se encontraron mejoras necesarias")
                    continue
                
                print(f"✅ {len(improvements)} mejoras generadas")
                
                # 3. Aplicar mejoras automáticamente
                applied_count = 0
                for improvement in improvements:
                    print(f"\n🔧 Aplicando mejora: {improvement.get('description', 'Sin descripción')}")
                    
                    success = await self.improvement_engine.implement_improvement(
                        improvement, 
                        auto_apply=True  # Aplicación automática
                    )
                    
                    if success:
                        applied_count += 1
                        self.improvements_applied.append(improvement)
                        print("✅ Mejora aplicada exitosamente")
                    else:
                        print("❌ Error aplicando mejora")
                
                print(f"\n📊 RESUMEN DEL CICLO {self.improvement_cycles}:")
                print(f"   • Mejoras generadas: {len(improvements)}")
                print(f"   • Mejoras aplicadas: {applied_count}")
                print(f"   • Tasa de éxito: {(applied_count/len(improvements)*100):.1f}%")
                
                # 4. Verificar si se alcanzó la perfección
                if await self.check_perfection_achieved():
                    print("\n🎉 ¡PERFECCIÓN ALCANZADA!")
                    print("El sistema ha alcanzado un estado óptimo")
                    break
                
                # 5. Pausa antes del siguiente ciclo
                print(f"\n⏳ Esperando antes del siguiente ciclo...")
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Error en ciclo de mejora: {e}")
                continue
        
        await self.generate_final_report()
    
    def print_analysis_summary(self, analysis):
        """Imprime resumen del análisis"""
        
        print("\n📊 RESUMEN DEL ANÁLISIS:")
        
        if "bottlenecks" in analysis:
            print(f"   🚧 Cuellos de botella: {len(analysis['bottlenecks'])}")
            for bottleneck in analysis["bottlenecks"][:3]:
                print(f"      • {bottleneck}")
        
        if "recurring_errors" in analysis:
            print(f"   ❌ Errores recurrentes: {len(analysis['recurring_errors'])}")
            for error in analysis["recurring_errors"][:3]:
                print(f"      • {error}")
        
        if "optimization_opportunities" in analysis:
            print(f"   ⚡ Oportunidades de optimización: {len(analysis['optimization_opportunities'])}")
            for opt in analysis["optimization_opportunities"][:3]:
                print(f"      • {opt}")
        
        if "new_features_needed" in analysis:
            print(f"   🆕 Nuevas funcionalidades: {len(analysis['new_features_needed'])}")
            for feature in analysis["new_features_needed"][:3]:
                print(f"      • {feature}")
    
    async def check_perfection_achieved(self) -> bool:
        """Verifica si el sistema ha alcanzado la perfección"""
        
        # Criterios de perfección
        perfection_criteria = {
            "error_rate": 0.01,  # Menos del 1% de errores
            "performance_score": 0.95,  # 95% de rendimiento óptimo
            "improvement_impact": 0.05  # Mejoras menores al 5%
        }
        
        try:
            # Simular verificación de perfección
            # En un sistema real, esto analizaría métricas reales
            
            current_metrics = {
                "error_rate": 0.02,
                "performance_score": 0.92,
                "improvement_impact": 0.08
            }
            
            perfection_achieved = all(
                current_metrics[metric] <= threshold if "rate" in metric or "impact" in metric
                else current_metrics[metric] >= threshold
                for metric, threshold in perfection_criteria.items()
            )
            
            if perfection_achieved:
                print("🎯 Criterios de perfección alcanzados:")
                for metric, value in current_metrics.items():
                    print(f"   • {metric}: {value}")
            
            return perfection_achieved
            
        except Exception as e:
            self.logger.error(f"Error verificando perfección: {e}")
            return False
    
    async def generate_final_report(self):
        """Genera reporte final de auto-mejora"""
        
        print("\n" + "="*60)
        print("📋 REPORTE FINAL DE AUTO-MEJORA")
        print("="*60)
        
        print(f"🔄 Ciclos completados: {self.improvement_cycles}")
        print(f"🔧 Mejoras aplicadas: {len(self.improvements_applied)}")
        
        if self.improvements_applied:
            print("\n✅ MEJORAS IMPLEMENTADAS:")
            for i, improvement in enumerate(self.improvements_applied, 1):
                print(f"   {i}. {improvement.get('description', 'Sin descripción')}")
                print(f"      Tipo: {improvement.get('type', 'Desconocido')}")
                print(f"      Impacto: {improvement.get('impact', 'No especificado')}")
        
        # Generar reporte detallado con IA
        report_prompt = f"""
        Genera un reporte final de auto-mejora del sistema de pentesting:
        
        Ciclos completados: {self.improvement_cycles}
        Mejoras aplicadas: {len(self.improvements_applied)}
        
        Mejoras implementadas:
        {[imp.get('description', '') for imp in self.improvements_applied]}
        
        Incluye:
        1. Resumen ejecutivo de mejoras
        2. Impacto en el rendimiento
        3. Nuevas capacidades adquiridas
        4. Evolución del sistema
        5. Próximos pasos recomendados
        """
        
        try:
            detailed_report = await self.improvement_engine._query_ai(report_prompt)
            
            # Guardar reporte
            import time
            report_file = f"/tmp/self_improvement_report_{int(time.time())}.txt"
            with open(report_file, 'w') as f:
                f.write(f"REPORTE DE AUTO-MEJORA AUTÓNOMA\n")
                f.write(f"Fecha: {time.ctime()}\n")
                f.write(f"Ciclos: {self.improvement_cycles}\n")
                f.write(f"Mejoras: {len(self.improvements_applied)}\n\n")
                f.write(detailed_report)
            
            print(f"\n📄 Reporte detallado guardado en: {report_file}")
            
        except Exception as e:
            print(f"Error generando reporte detallado: {e}")
        
        print("\n🎉 AUTO-MEJORA COMPLETADA")

async def main():
    """Función principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema de Auto-mejora Autónoma")
    parser.add_argument("--cycles", type=int, default=5,
                       help="Número máximo de ciclos de mejora")
    parser.add_argument("--continuous", action="store_true",
                       help="Mejora continua sin límite de ciclos")
    
    args = parser.parse_args()
    
    # Verificar permisos de root
    if os.geteuid() != 0:
        print("❌ Se requieren permisos de root para auto-mejora")
        print("Ejecuta: sudo python3 run_self_improvement.py")
        sys.exit(1)
    
    print(f"""
    🧠 INICIANDO AUTO-MEJORA AUTÓNOMA
    ================================
    
    🤖 La IA se mejorará a sí misma
    🔄 Ciclos máximos: {'∞' if args.continuous else args.cycles}
    ⚠️ PROCESO COMPLETAMENTE AUTÓNOMO
    
    La IA analizará, generará y aplicará mejoras automáticamente...
    """)
    
    try:
        system = AutonomousSelfImprovement()
        
        if args.continuous:
            system.max_cycles = float('inf')
        else:
            system.max_cycles = args.cycles
        
        await system.start_continuous_improvement()
        
    except KeyboardInterrupt:
        print("\n🛑 Auto-mejora detenida por el usuario")
    except Exception as e:
        print(f"❌ Error crítico en auto-mejora: {e}")

if __name__ == "__main__":
    asyncio.run(main())