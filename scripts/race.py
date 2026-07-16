from PIL import Image, ImageDraw
import random
import os

# Cria uma imagem branca de 800x400 pixels
img = Image.new('RGB', (800, 400), color='white')
draw = ImageDraw.Draw(img)

# Nomes e cores dos carrinhos
carros = [
    {'nome': 'Ferrari', 'cor': (255, 0, 0)},    # Vermelho
    {'nome': 'Mercedes', 'cor': (0, 0, 255)},   # Azul
    {'nome': 'McLaren', 'cor': (0, 255, 0)},    # Verde
    {'nome': 'Red Bull', 'cor': (255, 255, 0)}, # Amarelo
]

# Simula a corrida: cada carro anda uma distância aleatória
posicoes = [random.randint(50, 700) for _ in range(4)]

# Desenha os carrinhos na imagem
for i, (carro, pos) in enumerate(zip(carros, posicoes)):
    y = 50 + i * 80  # Posição vertical (um embaixo do outro)
    x = pos          # Posição horizontal (aleatória)
    
    # Desenha o carrinho (um retângulo)
    draw.rectangle([x, y, x+60, y+30], fill=carro['cor'])
    
    # Escreve o nome do carro
    draw.text((x, y-20), carro['nome'], fill='black')

# Escreve um título na imagem
draw.text((300, 10), "🏎️ Corrida de Carrinhos", fill='black')

# Salva a imagem
img.save('race.png')
print("✅ Imagem da corrida gerada com sucesso!")
