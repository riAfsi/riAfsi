from PIL import Image, ImageDraw
import random
import os

# ===== CONFIGURAÇÕES =====
LARGURA = 900
ALTURA = 500
NUM_FRAMES = 25           # Quantos frames (quanto mais, mais suave)
VELOCIDADE_MAX = 10       # Máximo de pixels por frame (ajuste para andar mais rápido)

# ===== DADOS DOS CARRINHOS =====
carros = [
    {'nome': 'Ferrari',   'cor_carro': (255, 50, 50),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Mercedes',  'cor_carro': (50, 150, 255),  'cor_cockpit': (200, 200, 200)},
    {'nome': 'McLaren',   'cor_carro': (255, 150, 0),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Red Bull',  'cor_carro': (255, 255, 50),  'cor_cockpit': (200, 200, 200)},
]

# ===== FUNÇÃO PARA DESENHAR UM FRAME =====
def desenhar_frame(posicoes):
    img = Image.new('RGB', (LARGURA, ALTURA), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)

    # Linha tracejada central
    for x in range(0, LARGURA, 60):
        draw.rectangle([x, ALTURA//2 - 3, x+30, ALTURA//2 + 3], fill=(255, 255, 255))

    # Bordas da pista
    draw.rectangle([0, 30, LARGURA, 35], fill=(255, 255, 255))
    draw.rectangle([0, ALTURA-35, LARGURA, ALTURA-30], fill=(255, 255, 255))

    # Desenha cada carro
    for i, (carro, pos_x) in enumerate(zip(carros, posicoes)):
        y = 60 + i * 100
        carro_largura = 80
        carro_altura = 40
        x1 = pos_x - carro_largura//2
        y1 = y - carro_altura//2
        x2 = pos_x + carro_largura//2
        y2 = y + carro_altura//2

        draw.rectangle([x1, y1, x2, y2], fill=carro['cor_carro'], outline='black', width=2)

        cockpit_tamanho = 20
        cx1 = pos_x - cockpit_tamanho//2
        cy1 = y - cockpit_tamanho//2
        cx2 = pos_x + cockpit_tamanho//2
        cy2 = y + cockpit_tamanho//2
        draw.rectangle([cx1, cy1, cx2, cy2], fill=carro['cor_cockpit'], outline='black', width=1)

        draw.text((pos_x - 30, y - 55), carro['nome'], fill='white')

    # Título
    draw.text((LARGURA//2 - 100, 10), "🏎️ CORRIDA DE CARRINHOS", fill='white', stroke_width=1, stroke_fill='black')
    return img

# ===== GERAR POSIÇÕES INICIAIS =====
# Cada carro começa em uma posição diferente, próximo ao início
posicoes = [random.randint(40, 120) for _ in range(4)]

# ===== GERAR MÚLTIPLOS FRAMES =====
frames = []
pos_atual = posicoes.copy()

for frame_num in range(NUM_FRAMES):
    # Avançar as posições (cada carro anda uma distância aleatória)
    for i in range(len(pos_atual)):
        # Cada carro tem uma velocidade diferente (alguns mais rápidos)
        andar = random.randint(5, VELOCIDADE_MAX)
        nova_pos = pos_atual[i] + andar
        # Se passar do fim da pista, para no final (não volta)
        if nova_pos > LARGURA - 60:
            nova_pos = LARGURA - 60
        pos_atual[i] = nova_pos
    
    # Desenha o frame atual
    img = desenhar_frame(pos_atual)
    frames.append(img)

# ===== SALVAR GIF ANIMADO =====
if frames:
    frames[0].save(
        'race.gif',
        save_all=True,
        append_images=frames[1:],
        duration=120,        # 120ms entre frames (mais suave)
        loop=0,
        optimize=False
    )
    print(f"✅ GIF gerado com {len(frames)} frames!")
else:
    print("❌ Nenhum frame gerado.")
