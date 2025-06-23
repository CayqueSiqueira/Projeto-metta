# Detecção de Pessoas em Vídeos
Como instalar as dependências e executar o código do repositório.

## Pré-requisitos
---
#### 1. Instalar o Python (3.8 ou superior)

Windows:
Baixe em python.org/downloads <br>
Marque a opção Add Python to PATH durante a instalação.

Linux (Debian/Ubuntu): <br>
bash <br>
sudo apt update <br>
sudo apt install python3 python3-pip

#### 2. Instalar o Git (para clonar o repositório)

Windows: git-scm.com/download/win

Linux:<br>
bash<br>
sudo apt install git<br>

#### 3. Instalar o Microsoft Visual C++ (Windows apenas)

O PyTorch precisa do C++ Redistributable <br>
Baixe e instale: Microsoft Visual C++ Redistributable <br>
https://learn.microsoft.com/pt-br/cpp/windows/latest-supported-vc-redist?view=msvc-170

Caso ocorra falha ou dificuldade na instação por essa via tente instalar o visual studio <br>
E o kit de desenvolvimento para desktop com c++ <br>
https://visualstudio.microsoft.com/pt-br/downloads/

## Requisitos
---
Serão instalados no passo 3 da Instalação
- Python 3.8+
- torch
- torchvision
- opencv-python
- matplotlib
- pillow
<br>
se quise conferir se já possui os pacotes no terminal digite:<br>
python -m pip list | findstr "torch torchvision opencv-python matplotlib pillow"

## Instalação
---
### Passo 1 Clonar o repositório
Abra o cmd e digite:<br>
git clone https://github.com/CayqueSiqueira/Projeto-metta.git<br>
cd Projeto-metta<br>
code .<br>

Caso o "code." não funcione basta clicar com botão direito no projeto e abrir com vscode

### Passo 2 Ambiente virtual (Opcional)
##### Após abrir o projeto no visual studio, em um novo terminal digite:<br>
python -m venv venv
### Ativação no Windows:
No terminal digite:<br>
venv\Scripts\activate
### Ativação no Linux/Mac:
No terminal digite:<br>
source venv/bin/activate

### Passo 3 Instale as dependências do Python
No terminal digite:<br>
pip install -r requirements.txt<br>

#### Após instalar os requisitos escolha como ira processar o video:No terminal digite:<br>

##### Se for executar com a cpu:<br>
No terminal digite:<br>
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu <br>

##### Se for executar com a gpu:<br>
No terminal digite:<br>
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121<br>

### Passo 4 Execute o projeto
No terminal digite:<br>
python main.py --video_path "caminho para o arquivo de video na pasta sample" --threshold 5


### Se ja definiu uma maneira da maquina processar o video e decidiu mudar:
No terminal digite:<br>
pip uninstall torch torchvision -y<br>

##### Se quiser executar pela gpu no terminal digite:<br>
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121<br>

ou<br>

##### Se quiser executar pela cpu no terminal digite:<br>
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

