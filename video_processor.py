import cv2
import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict

class VideoProcessor:
    """Processa vídeos para detecção de pessoas e geração de relatórios.
    
    Attributes:
        detector: Instância do detector de pessoas
        alert_threshold: Limite de pessoas para gerar alertas
        history: Lista de histórico de detecções
        alerts: Lista de alertas gerados
        alert_id: Contador de alertas
    """
    
    def __init__(self, detector, alert_threshold: int):
        """Inicializa o processador de vídeo.
        
        Args:
            detector: Instância do detector de pessoas
            alert_threshold: Limite de pessoas para gerar alertas
        """
        self.detector = detector
        self.alert_threshold = alert_threshold
        self.history: List[Dict] = []
        self.alerts: List[Dict] = []
        self.alert_id: int = 0
    
    def process_video(self, video_path: str) -> Tuple[str, List, List]:
        """Processa o vídeo frame a frame.
        
        Args:
            video_path: Caminho para o vídeo de entrada
            
        Returns:
            tuple: (caminho do vídeo de saída, dados de histórico, dados de alertas)
        """
        # Validar caminho de saída
        output_dir = Path('output_results')
        output_dir.mkdir(exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Não foi possível abrir o arquivo de vídeo")
        
        # Obter propriedades do vídeo
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Preparar writer de vídeo
        output_path = str(output_dir / 'output_video.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_id = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detectar pessoas
                boxes, _ = self.detector.detect(frame)
                people_count = len(boxes)
                
                # Atualizar histórico
                self.history.append({
                    "id": frame_id,
                    "count": people_count
                })
                
                # Verificar alertas
                if people_count >= self.alert_threshold:
                    self.alerts.append({
                        "id": self.alert_id,
                        "frame_id": frame_id,
                        "count": people_count,
                        "timestamp": datetime.now().isoformat()
                    })
                    self.alert_id += 1
                
                # Desenhar caixas delimitadoras
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Adicionar contagem de pessoas no frame
                cv2.putText(frame, f"Pessoas: {people_count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Escrever frame no vídeo de saída
                out.write(frame)
                
                frame_id += 1
                print(f"Processado frame {frame_id}/{total_frames} - Pessoas: {people_count}")
                
        except Exception as e:
            print(f"Erro durante o processamento do vídeo: {str(e)}")
            raise
        finally:
            # Liberar recursos
            cap.release()
            out.release()
        
        return output_path, self.history, self.alerts