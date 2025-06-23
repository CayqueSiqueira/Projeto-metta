
import numpy as np  # Adicione esta linha
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from typing import Optional

class ApplicationGUI:
    def __init__(self, video_path: str, history_data: list):
        self.video_path = video_path
        self.history_data = history_data
        self.playing = False
        self.current_frame = 0
        
        # Configurar janela principal
        self.root = tk.Tk()
        self.root.title("Análise de Detecção de Pessoas")
        self.root.geometry("1200x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configurar layout
        self.setup_ui()
        
        # Carregar vídeo
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError("Não foi possível abrir o vídeo de saída")
        
        # Exibir primeiro frame
        self.update_video_frame()
    
    def setup_ui(self):
        # Frame do vídeo
        self.video_frame = ttk.LabelFrame(self.root, text="Vídeo", padding=10)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Controles
        self.controls_frame = ttk.Frame(self.video_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        self.play_button = ttk.Button(
            self.controls_frame, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(
            self.controls_frame, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(
            self.controls_frame, text="Reset", command=self.reset_video)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Frame do gráfico
        self.graph_frame = ttk.LabelFrame(self.root, text="Análise", padding=10)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_graph()
    
    def setup_graph(self):
        # Extrair dados para o gráfico
        frame_ids = [entry['id'] for entry in self.history_data]
        people_counts = [entry['count'] for entry in self.history_data]
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(frame_ids, people_counts, 'b-', linewidth=2)
        ax.set_title('Contagem de Pessoas por Frame', fontsize=12)
        ax.set_xlabel('Frame ID', fontsize=10)
        ax.set_ylabel('Número de Pessoas', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Adicionar ao Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_video_frame(self):
    #"""Atualiza o frame do vídeo com tratamento de erro"""
        if not hasattr(self, 'playing') or not self.playing:
            return
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                self.pause_video()
                return
            
            self.current_frame += 1
            self.display_frame(frame)
            
            # Armazena o ID do callback para poder cancelá-lo
            self._after_id = self.video_label.after(30, self.update_video_frame)
        except Exception as e:
            print(f"Erro ao atualizar frame: {str(e)}")
            self.on_close()
    
    def display_frame(self, frame: Optional[np.ndarray] = None):
        if frame is None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            ret, frame = self.cap.read()
            if not ret:
                return
        
        # Converter para formato adequado para exibição
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((640, 480), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
    
    def play_video(self):
        if not self.playing:
            self.playing = True
            self.update_video_frame()
    
    def pause_video(self):
        self.playing = False
    
    def reset_video(self):
        self.pause_video()
        self.current_frame = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.display_frame()
    
    def on_close(self):
    #"""Método seguro para encerrar a aplicação"""
        try:
            self.pause_video()
            self.playing = False
            
            # Cancela qualquer callback pendente de forma segura
            if hasattr(self, '_after_id'):
                try:
                    self.root.after_cancel(self._after_id)
                except:
                    pass
            
            # Libera recursos de vídeo com tratamento de erro
            if hasattr(self, 'cap'):
                try:
                    if self.cap.isOpened():
                        self.cap.release()
                except:
                    pass
            
            # Destruição segura da janela
            try:
                self.root.quit()
                if self.root.winfo_exists():  # Verifica se a janela ainda existe
                    self.root.destroy()
            except:
                pass
                
        except Exception as e:
            print(f"Erro ao fechar a aplicação: {str(e)}")


    def run(self):
        self.root.mainloop()