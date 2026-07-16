from PIL import Image, ImageDraw
import random
import os
import json

# ===== CONFIGURAÇÕES =====
LARGURA = 900
ALTURA = 500
MAX_FRAMES = 60          # Número máximo de quadros no GIF
ARQUIVO_JSON = 'positions.json'
ARQUIVO_GIF = 'race.gif'

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

# ===== LER OU CRIAR JSON DE POSIÇÕES =====
if os.path.exists(ARQUIVO_JSON):
    with open(ARQUIVO_JSON, 'r') as f:
        posicoes = json.load(f)
else:
    # Posições iniciais aleatórias
    posicoes = [random.randint(60, LARGURA-100) for _ in range(4)]

# ===== ANDAR (INCREMENTAR POSIÇÃO) =====
# Cada carro anda um pouco, com sorte diferente
for i in range(len(posicoes)):
    andar = random.randint(5, 25)   # anda entre 5 e 25 pixels
    nova_pos = posicoes[i] + andar
    if nova_pos > LARGURA - 50:
        nova_pos = 60  # se passar do fim, volta para o início
    posicoes[i] = nova_pos

# ===== SALVAR POSIÇÕES ATUALIZADAS =====
with open(ARQUIVO_JSON, 'w') as f:
    json.dump(posicoes, f)

# ===== CRIAR O NOVO FRAME =====
novo_frame = desenhar_frame(posicoes)

# ===== CARREGAR GIF EXISTENTE OU CRIAR NOVO =====
frames = []
if os.path.exists(ARQUIVO_GIF):
    # Abrir o GIF existente e extrair os quadros
    gif_antigo = Image.open(ARQUIVO_GIF)
    for frame in range(gif_antigo.n_frames):
        gif_antigo.seek(frame)
        frames.append(gif_antigo.copy())
else:
    # Se não existe GIF, os frames começarão vazios
    pass

# Adicionar o novo frame
frames.append(novo_frame)

# Se exceder o limite, remover o primeiro frame (mais antigo)
if len(frames) > MAX_FRAMES:
    frames = frames[-MAX_FRAMES:]

# ===== SALVAR GIF =====
if len(frames) > 0:
    # Salvar como GIF animado
    frames[0].save(
        ARQUIVO_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=200,           # 200ms por frame
        loop=0,
        optimize=False
    )
    print(f"✅ GIF atualizado com {len(frames)} frames!")
else:
    print("❌ Nenhum frame para salvar.")

print("🏁 Corrida atualizada!")
