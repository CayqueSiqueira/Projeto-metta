import cv2
import torch
import numpy as np
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F

class PeopleDetector:
    """Detector de pessoas usando Faster R-CNN pré-treinado no COCO dataset.
    
    Attributes:
        device (torch.device): Dispositivo de processamento (CPU/GPU)
        model (torch.nn.Module): Modelo de detecção
        confidence_threshold (float): Limiar de confiança para detecções
    """
    
    def __init__(self, confidence_threshold: float = 0.5):
        """Inicializa o detector.
        
        Args:
            confidence_threshold: Limiar mínimo de confiança para considerar uma detecção
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Usando dispositivo: {self.device}")
        
        # Carregar modelo com pesos padrão
        self.model = fasterrcnn_resnet50_fpn(weights='DEFAULT')
        self.model.to(self.device)
        self.model.eval()
        
        self.confidence_threshold = confidence_threshold
    
    def detect(self, frame: np.ndarray) -> tuple:
        """Detecta pessoas em um frame de vídeo.
        
        Args:
            frame: Imagem no formato BGR (OpenCV)
            
        Returns:
            tuple: (caixas delimitadoras, scores de confiança)
                   Caixas no formato [x1, y1, x2, y2]
        """
        try:
            # Converter para RGB e tensor
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_tensor = F.to_tensor(img_rgb).to(self.device)
            
            # Fazer previsão
            with torch.no_grad():
                predictions = self.model([img_tensor])
            
            # Filtrar apenas detecções de pessoas (classe 1 no COCO)
            boxes = predictions[0]['boxes'].cpu().numpy()
            scores = predictions[0]['scores'].cpu().numpy()
            labels = predictions[0]['labels'].cpu().numpy()
            
            people_indices = [
                i for i, (label, score) in enumerate(zip(labels, scores)) 
                if label == 1 and score > self.confidence_threshold
            ]
            
            return boxes[people_indices], scores[people_indices]
            
        except Exception as e:
            print(f"Erro durante a detecção: {str(e)}")
            return np.array([]), np.array([])