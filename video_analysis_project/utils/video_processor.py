# -*- coding: utf-8 -*-
"""
Processador de Vídeo - Implementação Completa
Extração de frames, processamento e anotação de vídeos
"""

import numpy as np
from pathlib import Path
import logging
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import hashlib

# Importações para processamento de imagem
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class VideoProcessor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('VideoProcessor')
        self.output_path = Path(config.get('video', {}).get('output_path', 'output'))
        self.frame_skip = config.get('video', {}).get('frame_skip', 1)
        self.setup_directories()
        
        # Verificar dependências
        self.check_dependencies()
        
        print("✓ VideoProcessor inicializado (modo funcional)")
        
    def check_dependencies(self):
        """Verifica disponibilidade das dependências"""
        if not MATPLOTLIB_AVAILABLE:
            self.logger.warning("Matplotlib não disponível - algumas funcionalidades limitadas")
        if not PIL_AVAILABLE:
            self.logger.warning("PIL não disponível - algumas funcionalidades limitadas")
    
    def setup_directories(self):
        """Configura diretórios de saída"""
        self.frames_path = self.output_path / 'frames'
        self.metadata_path = self.output_path / 'metadata'
        
        for path in [self.frames_path, self.metadata_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def extract_frames(self, video_path: Path) -> List[np.ndarray]:
        """
        Extrai frames do vídeo
        
        Args:
            video_path: Caminho para o arquivo de vídeo
            
        Returns:
            Lista de frames como arrays numpy
        """
        try:
            self.logger.info(f"Extraindo frames de: {video_path.name}")
            
            # Verificar se o arquivo existe
            if not video_path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")
            
            # Para este exemplo, vamos simular a extração de frames
            # Em uma implementação real, você usaria cv2.VideoCapture ou similar
            frames = self._simulate_frame_extraction(video_path)
            
            self.logger.info(f"Extraídos {len(frames)} frames de {video_path.name}")
            
            # Salvar metadados da extração
            self._save_extraction_metadata(video_path, len(frames))
            
            return frames
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair frames de {video_path}: {str(e)}")
            return []
    
    def _simulate_frame_extraction(self, video_path: Path) -> List[np.ndarray]:
        """
        Simula extração de frames para demonstração
        Em produção, substitua por implementação real com OpenCV
        """
        # Determinar número de frames baseado no tamanho do arquivo
        file_size_mb = video_path.stat().st_size / (1024 * 1024)
        
        # Simular mais frames para arquivos maiores
        if file_size_mb > 50:
            num_frames = 20
        elif file_size_mb > 10:
            num_frames = 15
        else:
            num_frames = 10
        
        frames = []
        
        for i in range(num_frames):
            # Criar frame simulado com variação
            if i % 3 == 0:
                # Frame mais claro
                frame = np.random.randint(100, 255, (480, 640, 3), dtype=np.uint8)
            elif i % 3 == 1:
                # Frame médio
                frame = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)
            else:
                # Frame mais escuro
                frame = np.random.randint(20, 150, (480, 640, 3), dtype=np.uint8)
            
            # Adicionar alguma estrutura para simular conteúdo real
            frame = self._add_simulated_content(frame, i)
            
            frames.append(frame)
        
        return frames
    
    def _add_simulated_content(self, frame: np.ndarray, frame_index: int) -> np.ndarray:
        """Adiciona conteúdo simulado ao frame"""
        # Adicionar gradiente simples
        height, width = frame.shape[:2]
        
        # Gradiente horizontal
        for x in range(width):
            intensity = int((x / width) * 100)
            frame[:, x] = np.clip(frame[:, x] + intensity, 0, 255)
        
        # Adicionar "objetos" simulados baseados no índice do frame
        if frame_index % 4 == 0:
            # Simular objeto retangular
            frame[100:200, 200:300] = [255, 200, 200]  # Área rosa
        elif frame_index % 4 == 1:
            # Simular outro objeto
            frame[150:250, 350:450] = [200, 255, 200]  # Área verde
        
        return frame
    
    def get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """
        Obtém informações do vídeo
        
        Args:
            video_path: Caminho para o arquivo de vídeo
            
        Returns:
            Dicionário com informações do vídeo
        """
        try:
            # Informações básicas do arquivo
            file_stat = video_path.stat()
            file_size_mb = file_stat.st_size / (1024 * 1024)
            
            # Simular informações de vídeo baseadas no tamanho do arquivo
            # Em produção, use cv2.VideoCapture para obter informações reais
            video_info = {
                'file_path': str(video_path),
                'file_name': video_path.name,
                'file_extension': video_path.suffix.lower(),
                'file_size_bytes': file_stat.st_size,
                'file_size_mb': round(file_size_mb, 2),
                'creation_time': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modification_time': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'file_hash': self._calculate_file_hash(video_path),
                
                # Informações simuladas do vídeo
                'duration_seconds': self._estimate_duration(file_size_mb),
                'fps': 30.0,
                'total_frames': self._estimate_total_frames(file_size_mb),
                'resolution': self._estimate_resolution(file_size_mb),
                'codec': self._estimate_codec(video_path.suffix),
                'bitrate_kbps': self._estimate_bitrate(file_size_mb),
                'aspect_ratio': '16:9',
                
                # Metadados adicionais
                'analysis_metadata': {
                    'extracted_by': 'VideoProcessor',
                    'extraction_time': datetime.now().isoformat(),
                    'extraction_method': 'simulated',
                    'frame_skip': self.frame_skip
                }
            }
            
            self.logger.info(f"Informações obtidas para {video_path.name}")
            return video_info
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações do vídeo {video_path}: {str(e)}")
            return {
                'file_name': video_path.name,
                'error': str(e),
                'file_size_mb': 0,
                'duration_seconds': 0
            }
    
    def save_annotated_frame(self, frame: np.ndarray, analysis_results: Dict, 
                           frame_index: int, video_name: str) -> bool:
        """
        Salva frame com anotações das análises
        
        Args:
            frame: Frame original
            analysis_results: Resultados das análises
            frame_index: Índice do frame
            video_name: Nome do vídeo
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Criar diretório específico para o vídeo
            video_frames_dir = self.frames_path / video_name
            video_frames_dir.mkdir(parents=True, exist_ok=True)
            
            if not PIL_AVAILABLE:
                # Fallback: salvar apenas os dados JSON
                return self._save_frame_data_only(analysis_results, frame_index, video_frames_dir)
            
            # Processar frame
            annotated_frame = self._create_annotated_frame(frame, analysis_results)
            
            # Converter para PIL Image
            if annotated_frame.dtype != np.uint8:
                annotated_frame = (annotated_frame * 255).astype(np.uint8)
            
            # Converter BGR para RGB se necessário
            if len(annotated_frame.shape) == 3 and annotated_frame.shape[2] == 3:
                annotated_frame = annotated_frame[:, :, ::-1]
            
            pil_image = Image.fromarray(annotated_frame)
            
            # Adicionar anotações visuais
            annotated_image = self._add_visual_annotations(pil_image, analysis_results, frame_index)
            
            # Salvar frame anotado
            frame_filename = f"frame_{frame_index:06d}_annotated.jpg"
            frame_path = video_frames_dir / frame_filename
            annotated_image.save(frame_path, 'JPEG', quality=95, optimize=True)
            
            # Salvar dados da análise em JSON
            analysis_filename = f"frame_{frame_index:06d}_analysis.json"
            analysis_path = video_frames_dir / analysis_filename
            
            # Preparar dados para serialização
            serializable_results = self._make_json_serializable(analysis_results)
            serializable_results['frame_metadata'] = {
                'frame_index': frame_index,
                'video_name': video_name,
                'timestamp': frame_index / 30.0,  # Assumindo 30 FPS
                'annotation_time': datetime.now().isoformat(),
                'frame_dimensions': {
                    'height': frame.shape[0],
                    'width': frame.shape[1],
                    'channels': frame.shape[2] if len(frame.shape) > 2 else 1
                }
            }
            
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            # Criar thumbnail se necessário
            if frame_index % 10 == 0:  # Thumbnail a cada 10 frames
                self._create_thumbnail(annotated_image, frame_index, video_frames_dir)
            
            self.logger.debug(f"Frame {frame_index} salvo: {frame_filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar frame anotado {frame_index}: {str(e)}")
            return False
    
    def _create_annotated_frame(self, frame: np.ndarray, analysis_results: Dict) -> np.ndarray:
        """Cria versão anotada do frame"""
        # Clonar frame original
        annotated = frame.copy()
        
        # Adicionar overlay de informações se necessário
        # Por exemplo, ajustar brilho em áreas de interesse
        
        return annotated
    
    def _add_visual_annotations(self, pil_image: Image.Image, analysis_results: Dict, 
                              frame_index: int) -> Image.Image:
        """Adiciona anotações visuais ao frame"""
        draw = ImageDraw.Draw(pil_image)
        
        # Configurar fontes
        try:
            title_font = ImageFont.truetype("arial.ttf", 20)
            text_font = ImageFont.truetype("arial.ttf", 14)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except (OSError, IOError):
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Cores para diferentes tipos de detecção
        colors = {
            'human': (0, 255, 0),       # Verde
            'objects': (255, 0, 0),     # Vermelho
            'animals': (0, 0, 255),     # Azul
            'medical': (255, 0, 255),   # Magenta
            'environment': (255, 255, 0) # Amarelo
        }
        
        # Posições para texto
        text_y = 10
        text_margin = 25
        
        # Título do frame
        frame_title = f"Frame {frame_index:06d}"
        draw.text((10, text_y), frame_title, fill=(255, 255, 255), font=title_font)
        text_y += 30
        
        # Anotar detecções humanas
        if 'human' in analysis_results:
            human_data = analysis_results['human']
            people_count = human_data.get('people_detected', 0)
            
            if people_count > 0:
                # Desenhar indicadores de pessoas
                for i in range(people_count):
                    x = 50 + i * 120
                    y = 60
                    w, h = 80, 160
                    
                    # Retângulo da pessoa
                    draw.rectangle([x, y, x+w, y+h], outline=colors['human'], width=3)
                    draw.text((x, y-20), f'Pessoa {i+1}', fill=colors['human'], font=text_font)
                    
                    # Adicionar detalhes se disponíveis
                    poses = human_data.get('poses', [])
                    if i < len(poses) and poses[i]:
                        pose_info = poses[i].get('posture', 'unknown')
                        draw.text((x, y+h+5), pose_info, fill=colors['human'], font=small_font)
                
                # Resumo
                draw.text((10, text_y), f'👥 Pessoas: {people_count}', 
                         fill=colors['human'], font=text_font)
                text_y += text_margin
        
        # Anotar detecções de objetos
        if 'objects' in analysis_results:
            objects_data = analysis_results['objects']
            total_objects = objects_data.get('total_objects', 0)
            
            if total_objects > 0:
                # Desenhar caixas de objetos
                categories = objects_data.get('categories', {})
                obj_x = 200
                
                for category, objects in categories.items():
                    for j, obj in enumerate(objects):
                        x = obj_x + j * 70
                        y = 250
                        w, h = 60, 60
                        
                        # Retângulo do objeto
                        draw.rectangle([x, y, x+w, y+h], outline=colors['objects'], width=2)
                        
                        # Nome do objeto
                        obj_name = obj.get('name', category)[:8]  # Limitar comprimento
                        draw.text((x, y-15), obj_name, fill=colors['objects'], font=small_font)
                        
                        # Confiança
                        confidence = obj.get('confidence', 0)
                        if confidence > 0:
                            draw.text((x, y+h+2), f'{confidence:.2f}', 
                                     fill=colors['objects'], font=small_font)
                
                draw.text((10, text_y), f'📦 Objetos: {total_objects}', 
                         fill=colors['objects'], font=text_font)
                text_y += text_margin
        
        # Anotar detecções de animais
        if 'animals' in analysis_results:
            animals_data = analysis_results['animals']
            total_animals = animals_data.get('total_animals', 0)
            
            if total_animals > 0:
                # Desenhar indicadores de animais
                for i in range(min(total_animals, 3)):  # Máximo 3 para não sobrecarregar
                    x = 300 + i * 80
                    y = 400
                    w, h = 70, 50
                    
                    draw.rectangle([x, y, x+w, y+h], outline=colors['animals'], width=2)
                    draw.text((x, y-15), f'Animal {i+1}', fill=colors['animals'], font=small_font)
                
                draw.text((10, text_y), f'🐾 Animais: {total_animals}', 
                         fill=colors['animals'], font=text_font)
                text_y += text_margin
        
        # Anotar análise médica
        if 'medical' in analysis_results:
            medical_data = analysis_results['medical']
            
            if medical_data.get('region_detected', False):
                # Região médica detectada
                x, y = 400, 100
                w, h = 200, 200
                
                # Retângulo da região médica
                draw.rectangle([x, y, x+w, y+h], outline=colors['medical'], width=4)
                draw.text((x, y-25), 'Região Anatômica', fill=colors['medical'], font=text_font)
                
                # Score de saúde
                health_assessment = medical_data.get('health_assessment', {})
                health_score = health_assessment.get('overall_health_score', 0)
                
                if health_score > 0:
                    score_text = f'Score: {health_score:.2f}'
                    draw.text((x, y+h+5), score_text, fill=colors['medical'], font=small_font)
                
                draw.text((10, text_y), f'🏥 Análise Médica: ✓', 
                         fill=colors['medical'], font=text_font)
                text_y += text_margin
        
        # Anotar análise ambiental
        if 'environment' in analysis_results:
            env_data = analysis_results['environment']
            env_type = env_data.get('environment_type', {}).get('primary_type', 'unknown')
            
            if env_type != 'unknown':
                draw.text((10, text_y), f'🌍 Ambiente: {env_type}', 
                         fill=colors['environment'], font=text_font)
                text_y += text_margin
        
        # Rodapé com informações adicionais
        footer_y = pil_image.height - 60
        timestamp = datetime.now().strftime('%H:%M:%S')
        footer_text = f"Análise realizada em {timestamp}"
        draw.text((10, footer_y), footer_text, fill=(200, 200, 200), font=small_font)
        
        # Linha de status
        status_y = pil_image.height - 40
        status_items = []
        
        for analysis_type in ['human', 'objects', 'animals', 'medical', 'environment']:
            if analysis_type in analysis_results:
                status_items.append(f"{analysis_type}:✓")
            else:
                status_items.append(f"{analysis_type}:✗")
        
        status_text = " | ".join(status_items)
        draw.text((10, status_y), status_text, fill=(150, 150, 150), font=small_font)
        
        # Adicionar marca d'água
        watermark_text = "Video Analysis System"
        bbox = draw.textbbox((0, 0), watermark_text, font=small_font)
        watermark_width = bbox[2] - bbox[0]
        watermark_x = pil_image.width - watermark_width - 10
        draw.text((watermark_x, 10), watermark_text, fill=(100, 100, 100), font=small_font)
        
        return pil_image
    
    def _save_frame_data_only(self, analysis_results: Dict, frame_index: int, 
                            output_dir: Path) -> bool:
        """Salva apenas dados JSON quando PIL não está disponível"""
        try:
            analysis_filename = f"frame_{frame_index:06d}_analysis.json"
            analysis_path = output_dir / analysis_filename
            
            serializable_results = self._make_json_serializable(analysis_results)
            
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Dados do frame {frame_index} salvos (sem imagem)")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados do frame {frame_index}: {str(e)}")
            return False
    
    def _create_thumbnail(self, image: Image.Image, frame_index: int, output_dir: Path):
        """Cria thumbnail do frame"""
        try:
            thumbnail_size = (160, 120)
            thumbnail = image.copy()
            thumbnail.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            
            thumbnail_filename = f"thumb_{frame_index:06d}.jpg"
            thumbnail_path = output_dir / thumbnail_filename
            thumbnail.save(thumbnail_path, 'JPEG', quality=80)
            
        except Exception as e:
            self.logger.warning(f"Erro ao criar thumbnail para frame {frame_index}: {str(e)}")
    
    def _save_extraction_metadata(self, video_path: Path, frame_count: int):
        """Salva metadados da extração"""
        try:
            metadata = {
                'video_file': str(video_path),
                'video_name': video_path.stem,
                'extraction_time': datetime.now().isoformat(),
                'total_frames_extracted': frame_count,
                'frame_skip': self.frame_skip,
                'extraction_method': 'simulated',
                'processor_version': '1.0.0'
            }
            
            metadata_file = self.metadata_path / f"{video_path.stem}_extraction.json"
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.warning(f"Erro ao salvar metadados de extração: {str(e)}")
    
    def _make_json_serializable(self, obj):
        """Torna objeto serializável para JSON"""
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj
    
    # Métodos utilitários para estimativas
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash MD5 do arquivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Ler apenas os primeiros 1MB para performance
                chunk = f.read(1024 * 1024)
                hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return "unknown"
    
    def _estimate_duration(self, file_size_mb: float) -> float:
        """Estima duração baseada no tamanho do arquivo"""
        # Estimativa grosseira: ~1MB por segundo para vídeo de qualidade média
        base_duration = file_size_mb * 0.8
        return round(max(5.0, min(300.0, base_duration)), 1)  # Entre 5s e 5min
    
    def _estimate_total_frames(self, file_size_mb: float) -> int:
        """Estima número total de frames"""
        duration = self._estimate_duration(file_size_mb)
        return int(duration * 30)  # Assumindo 30 FPS
    
    def _estimate_resolution(self, file_size_mb: float) -> Dict[str, int]:
        """Estima resolução baseada no tamanho do arquivo"""
        if file_size_mb > 100:
            return {'width': 1920, 'height': 1080}  # Full HD
        elif file_size_mb > 50:
            return {'width': 1280, 'height': 720}   # HD
        else:
            return {'width': 854, 'height': 480}    # SD
    
    def _estimate_codec(self, file_extension: str) -> str:
        """Estima codec baseado na extensão"""
        codec_map = {
            '.mp4': 'h264',
            '.avi': 'xvid',
            '.mov': 'h264',
            '.mkv': 'h264',
            '.wmv': 'wmv3',
            '.webm': 'vp8'
        }
        return codec_map.get(file_extension.lower(), 'unknown')
    
    def _estimate_bitrate(self, file_size_mb: float) -> int:
        """Estima bitrate baseado no tamanho do arquivo"""
        duration = self._estimate_duration(file_size_mb)
        if duration > 0:
            # Bitrate em kbps
            bitrate = (file_size_mb * 8 * 1024) / duration
            return int(bitrate)
        return 1000  # Default
    
    def create_video_summary(self, video_path: Path, analysis_results: Dict) -> str:
        """Cria resumo visual do vídeo analisado"""
        try:
            summary_dir = self.frames_path / video_path.stem
            summary_path = summary_dir / "video_summary.json"
            
            # Compilar estatísticas do vídeo
            summary_data = {
                'video_info': analysis_results.get('video_info', {}),
                'analysis_summary': self._compile_analysis_summary(analysis_results),
                'frame_statistics': self._calculate_frame_statistics(analysis_results),
                'detection_timeline': self._create_detection_timeline(analysis_results),
                'summary_creation_time': datetime.now().isoformat()
            }
            
            # Salvar resumo
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Resumo do vídeo criado: {summary_path}")
            return str(summary_path)
            
        except Exception as e:
            self.logger.error(f"Erro ao criar resumo do vídeo: {str(e)}")
            return ""
    
    def _compile_analysis_summary(self, analysis_results: Dict) -> Dict:
        """Compila resumo das análises"""
        summary = {
            'total_frames_analyzed': 0,
            'analyses_performed': [],
            'detection_counts': {}
        }
        
        for analysis_type, data in analysis_results.items():
            if isinstance(data, list) and analysis_type != 'video_info':
                summary['total_frames_analyzed'] = max(summary['total_frames_analyzed'], len(data))
                summary['analyses_performed'].append(analysis_type)
                
                # Contar detecções específicas
                if analysis_type == 'human_analysis':
                    total_people = sum(frame.get('data', {}).get('people_detected', 0) for frame in data)
                    summary['detection_counts']['people'] = total_people
                elif analysis_type == 'object_detection':
                    total_objects = sum(frame.get('data', {}).get('total_objects', 0) for frame in data)
                    summary['detection_counts']['objects'] = total_objects
                elif analysis_type == 'animal_detection':
                    total_animals = sum(frame.get('data', {}).get('total_animals', 0) for frame in data)
                    summary['detection_counts']['animals'] = total_animals
        
        return summary
    
    def _calculate_frame_statistics(self, analysis_results: Dict) -> Dict:
        """Calcula estatísticas por frame"""
        stats = {
            'frames_with_people': 0,
            'frames_with_objects': 0,
            'frames_with_animals': 0,
            'frames_with_medical_analysis': 0,
            'average_detections_per_frame': 0
        }
        
        total_detections = 0
        total_frames = 0
        
        for analysis_type, data in analysis_results.items():
            if isinstance(data, list) and analysis_type != 'video_info':
                total_frames = len(data)
                
                for frame_data in data:
                    frame_info = frame_data.get('data', {})
                    
                    if analysis_type == 'human_analysis' and frame_info.get('people_detected', 0) > 0:
                        stats['frames_with_people'] += 1
                        total_detections += frame_info.get('people_detected', 0)
                    elif analysis_type == 'object_detection' and frame_info.get('total_objects', 0) > 0:
                        stats['frames_with_objects'] += 1
                        total_detections += frame_info.get('total_objects', 0)
                    elif analysis_type == 'animal_detection' and frame_info.get('total_animals', 0) > 0:
                        stats['frames_with_animals'] += 1
                        total_detections += frame_info.get('total_animals', 0)
                    elif analysis_type == 'medical_analysis' and frame_info.get('region_detected', False):
                        stats['frames_with_medical_analysis'] += 1
        
        if total_frames > 0:
            stats['average_detections_per_frame'] = round(total_detections / total_frames, 2)
        
        return stats
    
    def _create_detection_timeline(self, analysis_results: Dict) -> List[Dict]:
        """Cria timeline de detecções"""
        timeline = []
        
        # Determinar número de frames
        max_frames = 0
        for analysis_type, data in analysis_results.items():
            if isinstance(data, list):
                max_frames = max(max_frames, len(data))
        
        # Criar entrada para cada frame
        for i in range(max_frames):
            frame_entry = {
                'frame_index': i,
                'timestamp': round(i / 30.0, 2),  # Assumindo 30 FPS
                'detections': {}
            }
            
            # Coletar detecções de cada tipo de análise
            for analysis_type, data in analysis_results.items():
                if isinstance(data, list) and i < len(data):
                    frame_data = data[i].get('data', {})
                    
                    if analysis_type == 'human_analysis':
                        frame_entry['detections']['people'] = frame_data.get('people_detected', 0)
                    elif analysis_type == 'object_detection':
                        frame_entry['detections']['objects'] = frame_data.get('total_objects', 0)
                    elif analysis_type == 'animal_detection':
                        frame_entry['detections']['animals'] = frame_data.get('total_animals', 0)
                    elif analysis_type == 'medical_analysis':
                        frame_entry['detections']['medical_regions'] = 1 if frame_data.get('region_detected', False) else 0
            
            timeline.append(frame_entry)
        
        return timeline