# -*- coding: utf-8 -*-
"""
Gerador de Relatórios - Placeholder funcional
"""
import json
from pathlib import Path
from datetime import datetime

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.output_path = Path(config.get('video', {}).get('output_path', 'output'))
        self.reports_path = self.output_path / 'reports'
        self.reports_path.mkdir(parents=True, exist_ok=True)
        print("✓ ReportGenerator inicializado (modo placeholder)")
    
    def generate_report(self, analysis_results, video_name):
        """Placeholder - gera relatório básico"""
        report_data = {
            'video_name': video_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': 'Relatório gerado em modo placeholder',
            'statistics': {
                'people_detected': self._count_people(analysis_results),
                'objects_detected': self._count_objects(analysis_results),
                'animals_detected': self._count_animals(analysis_results)
            },
            'results': analysis_results
        }
        
        report_path = self.reports_path / f"{video_name}_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"✓ Relatório criado: {report_path}")
        return str(report_path)
    
    def generate_consolidated_report(self, all_results):
        """Placeholder - gera relatório consolidado"""
        report_path = self.reports_path / f"consolidated_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        consolidated_data = {
            'total_videos': len(all_results),
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': f'Análise consolidada de {len(all_results)} vídeos',
            'results': all_results
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, default=str)
        
        print(f"✓ Relatório consolidado criado: {report_path}")
        return str(report_path)
    
    def _count_people(self, results):
        """Conta detecções de pessoas"""
        count = 0
        if 'human' in results:
            for frame_data in results['human']:
                data = frame_data.get('data', {})
                count += data.get('people_detected', 0)
        return count
    
    def _count_objects(self, results):
        """Conta detecções de objetos"""
        count = 0
        if 'objects' in results:
            for frame_data in results['objects']:
                data = frame_data.get('data', {})
                count += data.get('total_objects', 0)
        return count
    
    def _count_animals(self, results):
        """Conta detecções de animais"""
        count = 0
        if 'animals' in results:
            for frame_data in results['animals']:
                data = frame_data.get('data', {})
                count += data.get('total_animals', 0)
        return count
