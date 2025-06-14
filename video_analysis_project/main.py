import os
import sys
import yaml
import logging
from pathlib import Path
from tqdm import tqdm

# Importar módulos locais
from utils.video_processor import VideoProcessor
from utils.report_generator import ReportGenerator
from models.human_analyzer import HumanAnalyzer
from models.object_detector import ObjectDetector
from models.animal_detector import AnimalDetector
from models.behavior_analyzer import BehaviorAnalyzer
from models.environment_analyzer import EnvironmentAnalyzer

# Importação condicional do analisador médico
try:
    from models.medical_analyzer import MedicalAnalyzer
    MEDICAL_ANALYZER_AVAILABLE = True
except ImportError:
    MEDICAL_ANALYZER_AVAILABLE = False
    print("⚠️ MedicalAnalyzer não disponível")

# Importação condicional do gerenciador de visualização
try:
    from utils.visualization import VisualizationManager
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("⚠️ VisualizationManager não disponível")

class VideoAnalysisSystem:
    def __init__(self, config_path="config/config.yaml"):
        """Inicializa o sistema de análise de vídeo"""
        print("🚀 Inicializando Sistema de Análise de Vídeo...")
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.setup_directories()
        self.initialize_analyzers()
        print("✅ Sistema inicializado com sucesso!")
        
    def load_config(self, config_path):
        """Carrega configurações do arquivo YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print(f"✓ Configurações carregadas de: {config_path}")
                return config
        except FileNotFoundError:
            print(f"❌ Arquivo de configuração não encontrado: {config_path}")
            print("📝 Usando configurações padrão...")
            return self.get_default_config()
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {str(e)}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Retorna configurações padrão caso o arquivo não seja encontrado"""
        return {
            'video': {
                'input_path': 'videos/input/',
                'output_path': 'output/',
                'supported_formats': ['.mp4', '.avi', '.mov', '.mkv', '.wmv'],
                'frame_skip': 1
            },
            'analysis': {
                'human_detection': True,
                'pose_estimation': True,
                'facial_analysis': True,
                'behavior_analysis': True,
                'object_detection': True,
                'animal_detection': True,
                'environment_analysis': True,
                'medical_analysis': True
            },
            'output': {
                'generate_report': True,
                'save_frames': True,
                'create_visualizations': True,
                'detailed_logging': True
            },
            'medical_settings': {
                'analysis_detail_level': 'comprehensive',
                'anatomical_regions': ['breast', 'general'],
                'health_assessment': True,
                'privacy_mode': True,
                'medical_terminology': True,
                'generate_recommendations': True
            }
        }
    
    def setup_logging(self):
        """Configura sistema de logging"""
        log_level = logging.INFO if self.config.get('output', {}).get('detailed_logging', True) else logging.WARNING
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('output/analysis.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Configurar logger específico
        self.logger = logging.getLogger('VideoAnalysisSystem')
        self.logger.info("Sistema de logging configurado")
        
    def setup_directories(self):
        """Cria diretórios necessários"""
        directories = [
            'output/reports',
            'output/frames',
            'output/visualizations',
            'output/metadata',
            'videos/input'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print("✓ Diretórios de saída configurados")
    
    def initialize_analyzers(self):
        """Inicializa todos os analisadores"""
        print("🔧 Inicializando analisadores...")
        
        # Analisadores básicos
        self.video_processor = VideoProcessor(self.config)
        self.human_analyzer = HumanAnalyzer(self.config)
        self.object_detector = ObjectDetector(self.config)
        self.animal_detector = AnimalDetector(self.config)
        self.behavior_analyzer = BehaviorAnalyzer(self.config)
        self.environment_analyzer = EnvironmentAnalyzer(self.config)
        self.report_generator = ReportGenerator(self.config)
        
        # Analisador médico (se disponível)
        if MEDICAL_ANALYZER_AVAILABLE:
            self.medical_analyzer = MedicalAnalyzer(self.config)
        else:
            self.medical_analyzer = None
            print("⚠️ Analisador médico não disponível")
        
        # Gerenciador de visualização (se disponível)
        if VISUALIZATION_AVAILABLE:
            self.visualization_manager = VisualizationManager(self.config)
        else:
            self.visualization_manager = None
            print("⚠️ Gerenciador de visualização não disponível")
        
        print("✅ Todos os analisadores inicializados")
        
    def get_video_files(self):
        """Busca arquivos de vídeo na pasta de entrada"""
        input_path = Path(self.config['video']['input_path'])
        supported_formats = self.config['video']['supported_formats']
        
        if not input_path.exists():
            self.logger.warning(f"Pasta de entrada não encontrada: {input_path}")
            input_path.mkdir(parents=True, exist_ok=True)
            return []
        
        video_files = []
        for format_ext in supported_formats:
            found_files = list(input_path.glob(f"*{format_ext}"))
            video_files.extend(found_files)
            if found_files:
                self.logger.info(f"Encontrados {len(found_files)} arquivos {format_ext}")
        
        # Remover duplicatas e ordenar
        video_files = sorted(list(set(video_files)))
        
        return video_files
    
    def analyze_video(self, video_path):
        """Analisa um único vídeo"""
        self.logger.info(f"🎬 Iniciando análise do vídeo: {video_path.name}")
        
        try:
            # Verificar se o arquivo existe e é acessível
            if not video_path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")
            
            # Resultados da análise
            analysis_results = {
                'video_info': {},
                'human_analysis': [],
                'object_detection': [],
                'animal_detection': [],
                'environment_analysis': [],
                'medical_analysis': [],
                'behavior_analysis': {},
                'metadata': {
                    'analysis_start_time': self.get_current_timestamp(),
                    'video_path': str(video_path),
                    'video_name': video_path.stem,
                    'analysis_config': self.config['analysis'].copy()
                }
            }
            
            # Processamento do vídeo
            print(f"📹 Processando vídeo: {video_path.name}")
            frames = self.video_processor.extract_frames(video_path)
            analysis_results['video_info'] = self.video_processor.get_video_info(video_path)
            
            total_frames = len(frames)
            print(f"✓ Extraídos {total_frames} frames para análise")
            self.logger.info(f"Extraídos {total_frames} frames de {video_path.name}")
            
            if total_frames == 0:
                self.logger.warning("Nenhum frame extraído do vídeo")
                return analysis_results
            
            # Análises frame por frame
            print("🔍 Executando análises frame por frame...")
            
            for i, frame in enumerate(tqdm(frames, desc="Analisando frames", unit="frame")):
                try:
                    frame_results = {}
                    
                    # Análise humana
                    if self.config['analysis']['human_detection']:
                        frame_results['human'] = self.human_analyzer.analyze_frame(frame)
                    
                    # Detecção de objetos
                    if self.config['analysis']['object_detection']:
                        frame_results['objects'] = self.object_detector.detect_objects(frame)
                    
                    # Detecção de animais
                    if self.config['analysis']['animal_detection']:
                        frame_results['animals'] = self.animal_detector.detect_animals(frame)
                    
                    # Análise de ambiente
                    if self.config['analysis']['environment_analysis']:
                        frame_results['environment'] = self.environment_analyzer.analyze_environment(frame)
                    
                    # Análise médica (se disponível e habilitada)
                    if (self.config['analysis'].get('medical_analysis', False) and 
                        self.medical_analyzer is not None):
                        frame_results['medical'] = self.medical_analyzer.analyze_anatomical_region(frame)
                    
                    # Salvar frame anotado se configurado
                    if self.config['output']['save_frames']:
                        self.video_processor.save_annotated_frame(
                            frame, frame_results, i, video_path.stem
                        )
                    
                    # Acumular resultados
                    self.accumulate_results(analysis_results, frame_results, i)
                    
                except Exception as e:
                    self.logger.error(f"Erro ao analisar frame {i}: {str(e)}")
                    continue
            
            # Análise comportamental global
            if self.config['analysis']['behavior_analysis']:
                print("🧠 Executando análise comportamental...")
                try:
                    analysis_results['behavior_analysis'] = self.behavior_analyzer.analyze_behavior(
                        frames, analysis_results
                    )
                except Exception as e:
                    self.logger.error(f"Erro na análise comportamental: {str(e)}")
                    analysis_results['behavior_analysis'] = {}
            
            # Criar visualizações
            if (self.config['output'].get('create_visualizations', True) and 
                self.visualization_manager is not None):
                print("📊 Gerando visualizações...")
                try:
                    self.create_visualizations(analysis_results, video_path.stem)
                except Exception as e:
                    self.logger.error(f"Erro ao criar visualizações: {str(e)}")
            
            # Adicionar metadados finais
            analysis_results['metadata']['analysis_end_time'] = self.get_current_timestamp()
            analysis_results['metadata']['total_frames_processed'] = total_frames
            analysis_results['metadata']['analysis_success'] = True
            
            print(f"✅ Análise do vídeo {video_path.name} concluída com sucesso!")
            
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Erro crítico na análise do vídeo {video_path}: {str(e)}")
            # Retornar estrutura básica em caso de erro
            return {
                'video_info': {'file_name': video_path.name, 'error': str(e)},
                'metadata': {
                    'analysis_start_time': self.get_current_timestamp(),
                    'analysis_end_time': self.get_current_timestamp(),
                    'analysis_success': False,
                    'error_message': str(e)
                }
            }
    
    def create_visualizations(self, analysis_results, video_name):
        """Cria visualizações da análise"""
        try:
            # Dashboard principal
            dashboard_path = self.visualization_manager.create_analysis_dashboard(
                analysis_results, video_name
            )
            if dashboard_path:
                self.logger.info(f"Dashboard criado: {dashboard_path}")
            
            # Heatmap de detecções
            heatmap_path = self.visualization_manager.create_detection_heatmap(
                analysis_results, video_name
            )
            if heatmap_path:
                self.logger.info(f"Heatmap criado: {heatmap_path}")
            
            # Infográfico resumo
            infographic_path = self.visualization_manager.create_summary_infographic(
                analysis_results, video_name
            )
            if infographic_path:
                self.logger.info(f"Infográfico criado: {infographic_path}")
            
            # Análise médica específica (se disponível)
            if 'medical_analysis' in analysis_results and analysis_results['medical_analysis']:
                medical_chart_path = self.visualization_manager.create_medical_analysis_chart(
                    analysis_results, video_name
                )
                if medical_chart_path:
                    self.logger.info(f"Gráfico médico criado: {medical_chart_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao criar visualizações para {video_name}: {str(e)}")
    
    def accumulate_results(self, analysis_results, frame_results, frame_number):
        """Acumula resultados de cada frame na análise global"""
        for category, data in frame_results.items():
            if category not in analysis_results:
                analysis_results[category] = []
            
            analysis_results[category].append({
                'frame': frame_number,
                'timestamp': frame_number / 30.0,  # Assumindo 30 FPS
                'data': data
            })
    
    def run_analysis(self):
        """Executa a análise completa"""
        print("\n" + "="*60)
        print("🎬 SISTEMA DE ANÁLISE DE VÍDEO AVANÇADA")
        print("="*60)
        
        self.logger.info("Iniciando sistema de análise de vídeo")
        
        # Buscar vídeos
        print("🔍 Buscando vídeos para análise...")
        video_files = self.get_video_files()
        
        if not video_files:
            print("⚠️  Nenhum arquivo de vídeo encontrado na pasta de entrada")
            print(f"📁 Pasta: {self.config['video']['input_path']}")
            print(f"🎥 Formatos suportados: {', '.join(self.config['video']['supported_formats'])}")
            self.logger.warning("Nenhum arquivo de vídeo encontrado")
            return {}
        
        print(f"✅ Encontrados {len(video_files)} vídeo(s) para análise:")
        for i, video_file in enumerate(video_files, 1):
            file_size = video_file.stat().st_size / (1024 * 1024)  # MB
            print(f"  {i}. {video_file.name} ({file_size:.1f} MB)")
        
        print("\n" + "-"*60)
        
        # Analisar cada vídeo
        all_results = {}
        successful_analyses = 0
        failed_analyses = 0
        
        for video_index, video_path in enumerate(video_files, 1):
            try:
                print(f"\n📹 PROCESSANDO VÍDEO {video_index}/{len(video_files)}")
                print(f"   Arquivo: {video_path.name}")
                
                # Executar análise
                video_results = self.analyze_video(video_path)
                
                # Verificar se a análise foi bem-sucedida
                if video_results.get('metadata', {}).get('analysis_success', False):
                    all_results[video_path.stem] = video_results
                    successful_analyses += 1
                    
                    # Gerar relatório individual
                    if self.config['output']['generate_report']:
                        try:
                            report_path = self.report_generator.generate_report(
                                video_results, video_path.stem
                            )
                            if report_path:
                                print(f"📄 Relatório salvo: {Path(report_path).name}")
                        except Exception as e:
                            self.logger.error(f"Erro ao gerar relatório para {video_path.stem}: {str(e)}")
                    
                    print(f"✅ Análise concluída para: {video_path.name}")
                    
                else:
                    failed_analyses += 1
                    print(f"❌ Falha na análise de: {video_path.name}")
                
            except KeyboardInterrupt:
                print("\n⏹️  Análise interrompida pelo usuário")
                break
            except Exception as e:
                failed_analyses += 1
                print(f"❌ Erro ao analisar {video_path.name}: {str(e)}")
                self.logger.error(f"Erro ao analisar {video_path}: {str(e)}")
                continue
        
        # Gerar relatório consolidado
        if len(all_results) > 1:
            print(f"\n📊 Gerando relatório consolidado...")
            try:
                consolidated_path = self.report_generator.generate_consolidated_report(all_results)
                if consolidated_path:
                    print(f"📄 Relatório consolidado salvo: {Path(consolidated_path).name}")
            except Exception as e:
                self.logger.error(f"Erro ao gerar relatório consolidado: {str(e)}")
        
        # Resumo final
        print("\n" + "="*60)
        print("📈 RESUMO DA ANÁLISE")
        print("="*60)
        print(f"✅ Vídeos analisados com sucesso: {successful_analyses}")
        print(f"❌ Vídeos com falha: {failed_analyses}")
        print(f"📊 Total de vídeos processados: {successful_analyses + failed_analyses}")
        
        if successful_analyses > 0:
            print(f"\n📁 Resultados salvos em:")
            print(f"   📄 Relatórios: output/reports/")
            print(f"   🖼️  Frames: output/frames/")
            print(f"   📊 Visualizações: output/visualizations/")
            print(f"   📝 Logs: output/analysis.log")
        
        self.logger.info(f"Análise completa finalizada - Sucessos: {successful_analyses}, Falhas: {failed_analyses}")
        
        return all_results
    
    def get_current_timestamp(self):
        """Retorna timestamp atual"""
        from datetime import datetime
        return datetime.now().isoformat()

def display_system_info():
    """Exibe informações do sistema"""
    print("💻 INFORMAÇÕES DO SISTEMA")
    print("-" * 30)
    
    # Verificar disponibilidade de módulos
    modules_status = {
        "Análise Médica": MEDICAL_ANALYZER_AVAILABLE,
        "Visualizações": VISUALIZATION_AVAILABLE,
        "Numpy": True,  # Já foi importado se chegou até aqui
        "PIL": True,    # Usado no video_processor
        "Matplotlib": True  # Usado no video_processor
    }
    
    for module, available in modules_status.items():
        status = "✅ Disponível" if available else "❌ Não disponível"
        print(f"   {module}: {status}")
    
    print()

def main():
    """Função principal"""
    try:
        # Exibir informações do sistema
        display_system_info()
        
        # Inicializar sistema
        analyzer = VideoAnalysisSystem()
        
        # Executar análise
        results = analyzer.run_analysis()
        
        # Mensagem final
        if results:
            print(f"\n🎉 Análise concluída com sucesso!")
            print(f"📁 Verifique a pasta 'output/' para os resultados detalhados.")
        else:
            print(f"\n⚠️  Nenhuma análise foi completada.")
            print(f"📝 Verifique o arquivo 'output/analysis.log' para mais detalhes.")
        
    except KeyboardInterrupt:
        print("\n⏹️  Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro crítico durante a execução: {str(e)}")
        logging.error(f"Erro crítico: {str(e)}")
        print("📝 Verifique o arquivo 'output/analysis.log' para mais detalhes.")

if __name__ == "__main__":
    main()