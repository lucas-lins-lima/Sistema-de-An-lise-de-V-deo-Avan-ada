"""
Módulos utilitários para o sistema de análise de vídeo.

Este pacote contém funções auxiliares para:
- Processamento de vídeo
- Geração de relatórios
- Visualizações
- Manipulação de dados
"""

from .video_processor import VideoProcessor
from .report_generator import ReportGenerator
from .visualization import VisualizationManager

__all__ = [
    'VideoProcessor',
    'ReportGenerator', 
    'VisualizationManager'
]

__version__ = '1.0.0'
__author__ = 'Video Analysis System'