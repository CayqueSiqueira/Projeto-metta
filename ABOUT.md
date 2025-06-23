# 📘 ABOUT.md — Detecção de Pessoas com Análise em Vídeo

## 🎯 Objetivo da Solução
A aplicação foi desenvolvida para processar um vídeo de entrada, detectar pessoas em cada frame utilizando uma **rede neural pré-treinada (Faster R-CNN)** e gerar análises com contagens e alertas(contagens acima do limiar) em arquivos `.json`. Além disso, uma interface gráfica exibe o vídeo processado e um gráfico com o histórico de detecções.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Tecnologia      | Uso Principal                                      |
|-----------------|---------------------------------------------------|
| **Python 3.10+** | Linguagem base                                    |
| **OpenCV**       | Leitura e escrita de vídeos; manipulação de frames|
| **PyTorch**      | Execução do modelo de rede neural pré-treinado    |
| **Torchvision**  | Acesso ao modelo Faster R-CNN                     |
| **Tkinter**      | Construção da GUI                                 |
| **Matplotlib**   | Geração de gráfico de detecção na GUI             |
| **Pillow**       | Exibição de imagens no Tkinter                    |

---

## 🧠 Abordagem Técnica

### ✅ 1. Arquitetura Modular

O projeto foi dividido em módulos especializados para garantir manutenibilidade e reutilização de código.

| Arquivo             | Função Principal                                       |
|---------------------|--------------------------------------------------------|
| `detector.py`       | Detecta pessoas com Faster R-CNN                       |
| `video_processor.py`| Processa frames, registra histórico e alertas         |
| `gui.py`            | Apresenta GUI com vídeo e gráfico                     |
| `main.py`           | Coordena a execução da aplicação                       |

---

### ✅ 2. Rede Neural Pré-Treinada

O modelo utilizado é o `Faster R-CNN` com backbone `ResNet-50 FPN`, pré-treinado no dataset COCO. Esse modelo foi escolhido por:

- Alta acurácia na detecção de pessoas
- Integração direta via `torchvision.models.detection`
- Compatibilidade com CPU e GPU

---

## 🧪 Funcionalidades Implementadas

- 🔁 Leitura frame a frame de um vídeo de entrada
- 👤 Detecção de pessoas com bounding boxes
- 📊 Registro por frame da contagem de pessoas (`history.json`)
- 🚨 Geração de alertas (`alerts.json`) quando o número de pessoas ultrapassa um limite definido via argumento
- 🎞️ Vídeo final com as detecções desenhadas (`output_video.mp4`)
- 🖥️ Interface gráfica com player de vídeo + gráfico de contagem por frame


## Passos da Execução do Sistema de Detecção

1. **Especificar o caminho do vídeo**  
   <img src="images/image.png" alt="Especificação do caminho do vídeo" width="600">

2. **Configurar os parâmetros de entrada**  
   <img src="images/image-1.png" alt="Configuração dos parâmetros" width="600">

3. **Inicialização do detector de pessoas**  
   <img src="images/image-2.png" alt="Inicialização do detector" width="600">

4. **Processamento concluído - GUI disponível**  
   <img src="images/image-3.png" alt="Interface gráfica disponível na barra de tarefas" width="600">

5. **Visualização inicial na GUI**  
   <img src="images/image-4.png" alt="Gráfico e vídeo prontos para exibição" width="600">

6. **Reprodução do vídeo processado**  
   <img src="images/image-5.png" alt="Botão Play para iniciar a visualização" width="600">

7. **Controles de execução**  
   <img src="images/image-6.png" alt="Opções de Play, Pause e Reset" width="600">

8. **Finalização da GUI**  
   <img src="images/image-7.png" alt="Terminal liberado após fechar a interface" width="600">

9. **Arquivo de alertas gerado**  
   <img src="images/image-8.png" alt="Visualização do arquivo alerts.json" width="600">

10. **Histórico de detecções**  
    <img src="images/image-9.png" alt="Visualização do arquivo history.json" width="600">

11. **Vídeo processado**  
    <img src="images/image-10.png" alt="Visualização do vídeo de saída" width="600">