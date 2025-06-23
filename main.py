import argparse
import json
import signal
import sys
from pathlib import Path
from detector import PeopleDetector
from video_processor import VideoProcessor
from gui import ApplicationGUI

def signal_handler(sig, frame):
    """Manipulador para Ctrl+C"""
    print('\nEncerrando a aplicação...')
    if 'app' in globals():
        app.on_close()
    sys.exit(0)

def validate_path(video_path: str) -> str:
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"O arquivo de vídeo {video_path} não foi encontrado")
    return str(path.resolve())

def main():
    parser = argparse.ArgumentParser(description='Detecção de Pessoas em Vídeos')
    parser.add_argument('--video_path', type=validate_path, required=True, 
                       help='Caminho para o vídeo de entrada')
    parser.add_argument('--threshold', type=int, required=True,
                       help='Limite de pessoas para gerar alertas')
    args = parser.parse_args()

    # Criar diretório de saída
    output_dir = Path('output_results')
    output_dir.mkdir(exist_ok=True)

    try:
        # Inicializar componentes
        detector = PeopleDetector()
        processor = VideoProcessor(detector, args.threshold)
        
        # Processar vídeo
        output_video_path, history_data, alerts_data = processor.process_video(args.video_path)
        
        # Salvar JSONs
        with open(output_dir / 'history.json', 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        with open(output_dir / 'alerts.json', 'w', encoding='utf-8') as f:
            json.dump(alerts_data, f, indent=2, ensure_ascii=False)
        
        # Iniciar GUI
        global app  # Tornando global para o signal_handler acessar
        app = ApplicationGUI(output_video_path, history_data)
        app.run()
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Configura o handler antes de executar
    main()