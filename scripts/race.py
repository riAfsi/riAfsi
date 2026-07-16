from PIL import Image, ImageDraw
import random
import os

# ===== CONFIGURAÇÕES =====
LARGURA = 900
ALTURA = 500
NUM_FRAMES = 30           # Quantos frames (mais = mais suave)

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

    draw.text((LARGURA//2 - 100, 10), "🏎️ CORRIDA DE CARRINHOS", fill='white', stroke_width=1, stroke_fill='black')
    return img

# ===== GERAR POSIÇÕES INICIAIS =====
# Cada carro começa em uma posição diferente, perto do início
posicoes_iniciais = [random.randint(40, 120) for _ in range(4)]

# ===== GERAR FRAMES (CORRIDA COMPLETA) =====
frames = []
pos_atual = posicoes_iniciais.copy()

# Para cada carro, definir uma "velocidade" fixa (diferente)
# Quanto maior, mais rápido chega ao fim
velocidades = [random.uniform(0.8, 1.2) for _ in range(4)]

for frame_num in range(NUM_FRAMES):
    # Progresso de 0 a 1 (0 = início, 1 = fim)
    progresso = frame_num / (NUM_FRAMES - 1)
    
    # Cada carro anda de acordo com sua velocidade
    for i in range(len(pos_atual)):
        # Posição final = LARGURA - 60 (para não sair da pista)
        pos_final = LARGURA - 60
        # A posição atual é uma interpolação entre início e fim, com pequeno desvio aleatório
        # Usamos a velocidade individual para dar diferença
        progresso_real = progresso * velocidades[i]
        if progresso_real > 1.0:
            progresso_real = 1.0
        pos_atual[i] = int(posicoes_iniciais[i] + progresso_real * (pos_final - posicoes_iniciais[i]))
    
    # Desenha o frame atual
    img = desenhar_frame(pos_atual)
    frames.append(img)

# ===== SALVAR GIF ANIMADO =====
if frames:
    frames[0].save(
        'race.gif',
        save_all=True,
        append_images=frames[1:],
        duration=120,        # 120ms entre frames
        loop=0,
        optimize=False
    )
    print(f"✅ GIF gerado com {len(frames)} frames!")
else:
    print("❌ Nenhum frame gerado.")
