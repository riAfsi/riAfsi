from PIL import Image, ImageDraw
import random
import os

# Tamanho da imagem
LARGURA = 900
ALTURA = 500

# Cria uma imagem com fundo cinza-escuro (alcatrão)
img = Image.new('RGB', (LARGURA, ALTURA), color=(50, 50, 50))
draw = ImageDraw.Draw(img)

# ----- LINHA TRACEJADA BRANCA (meio da pista) -----
# Desenha traços brancos espaçados
for x in range(0, LARGURA, 60):
    draw.rectangle([x, ALTURA//2 - 3, x+30, ALTURA//2 + 3], fill=(255, 255, 255))

# ----- BORDA DA PISTA (faixas laterais) -----
# Faixa superior
draw.rectangle([0, 30, LARGURA, 35], fill=(255, 255, 255))
# Faixa inferior
draw.rectangle([0, ALTURA-35, LARGURA, ALTURA-30], fill=(255, 255, 255))

# ----- DADOS DOS CARRINHOS -----
carros = [
    {'nome': 'Ferrari',   'cor_carro': (255, 50, 50),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Mercedes',  'cor_carro': (50, 150, 255),  'cor_cockpit': (200, 200, 200)},
    {'nome': 'McLaren',   'cor_carro': (255, 150, 0),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Red Bull',  'cor_carro': (255, 255, 50),  'cor_cockpit': (200, 200, 200)},
]

# ----- POSIÇÕES ALEATÓRIAS (simula andar) -----
posicoes = [random.randint(60, LARGURA-100) for _ in range(4)]

# ----- DESENHA OS CARRINHOS -----
for i, (carro, pos_x) in enumerate(zip(carros, posicoes)):
    y = 60 + i * 100  # posição vertical (um embaixo do outro)
    
    # 1. Desenha a carroceria (retângulo principal)
    carro_largura = 80
    carro_altura = 40
    x1 = pos_x - carro_largura//2
    y1 = y - carro_altura//2
    x2 = pos_x + carro_largura//2
    y2 = y + carro_altura//2
    draw.rectangle([x1, y1, x2, y2], fill=carro['cor_carro'], outline='black', width=2)
    
    # 2. Desenha o cockpit (quadrado dentro do carro)
    cockpit_tamanho = 20
    cx1 = pos_x - cockpit_tamanho//2
    cy1 = y - cockpit_tamanho//2
    cx2 = pos_x + cockpit_tamanho//2
    cy2 = y + cockpit_tamanho//2
    draw.rectangle([cx1, cy1, cx2, cy2], fill=carro['cor_cockpit'], outline='black', width=1)
    
    # 3. Escreve o nome do carro (acima)
    draw.text((pos_x - 30, y - 55), carro['nome'], fill='white')

# ----- TÍTULO -----
draw.text((LARGURA//2 - 100, 10), "🏎️ CORRIDA DE CARRINHOS", fill='white', stroke_width=1, stroke_fill='black')

# Salva a imagem
img.save('race.png')
print("✅ Imagem da corrida gerada com sucesso!")
