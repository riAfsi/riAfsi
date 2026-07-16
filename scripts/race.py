from PIL import Image, ImageDraw
import random
import os
import json

# Configurações
LARGURA = 900
ALTURA = 500
MAX_FRAMES = 20  # Número de frames no GIF
ARQUIVO_ESTADO = 'estado.json'
ARQUIVO_GIF = 'race.gif'

# Dados dos carros
carros = [
    {'nome': 'Ferrari',   'cor_carro': (255, 50, 50),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Mercedes',  'cor_carro': (50, 150, 255),  'cor_cockpit': (200, 200, 200)},
    {'nome': 'McLaren',   'cor_carro': (255, 150, 0),   'cor_cockpit': (200, 200, 200)},
    {'nome': 'Red Bull',  'cor_carro': (255, 255, 50),  'cor_cockpit': (200, 200, 200)},
]

# Carrega ou cria o estado da corrida
if os.path.exists(ARQUIVO_ESTADO):
    with open(ARQUIVO_ESTADO, 'r') as f:
        estado = json.load(f)
else:
    # Primeira execução: cria estado inicial
    estado = {
        'posicoes': [random.randint(60, LARGURA-100) for _ in range(4)],
        'frames': []  # Lista de caminhos de frames
    }

# Atualiza posições (avanço aleatório)
for i in range(len(estado['posicoes'])):
    avanco = random.randint(5, 30)  # cada carro anda de 5 a 30 pixels
    estado['posicoes'][i] = min(estado['posicoes'][i] + avanco, LARGURA-60)
    # Se ultrapassar a linha de chegada, volta ao início (dá uma volta)
    if estado['posicoes'][i] >= LARGURA-60:
        estado['posicoes'][i] = 60

# --- Função para desenhar um frame ---
def desenhar_frame(posicoes):
    img = Image.new('RGB', (LARGURA, ALTURA), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    
    # Linha tracejada central
    for x in range(0, LARGURA, 60):
        draw.rectangle([x, ALTURA//2 - 3, x+30, ALTURA//2 + 3], fill=(255, 255, 255))
    
    # Bordas da pista
    draw.rectangle([0, 30, LARGURA, 35], fill=(255, 255, 255))
    draw.rectangle([0, ALTURA-35, LARGURA, ALTURA-30], fill=(255, 255, 255))
    
    # Desenha carros
    for i, (carro, pos_x) in enumerate(zip(carros, posicoes)):
        y = 60 + i * 100
        # Carroceria
        x1 = pos_x - 40
        y1 = y - 20
        x2 = pos_x + 40
        y2 = y + 20
        draw.rectangle([x1, y1, x2, y2], fill=carro['cor_carro'], outline='black', width=2)
        # Cockpit
        cx1 = pos_x - 10
        cy1 = y - 10
        cx2 = pos_x + 10
        cy2 = y + 10
        draw.rectangle([cx1, cy1, cx2, cy2], fill=carro['cor_cockpit'], outline='black', width=1)
        # Nome
        draw.text((pos_x - 30, y - 55), carro['nome'], fill='white')
    
    draw.text((LARGURA//2 - 100, 10), "🏎️ CORRIDA DE CARRINHOS", fill='white', stroke_width=1, stroke_fill='black')
    return img

# Gera o frame atual
frame = desenhar_frame(estado['posicoes'])
nome_frame = f'frame_{len(estado["frames"])}.png'
frame.save(nome_frame)
estado['frames'].append(nome_frame)

# Mantém apenas os últimos MAX_FRAMES frames
if len(estado['frames']) > MAX_FRAMES:
    remover = estado['frames'].pop(0)
    if os.path.exists(remover):
        os.remove(remover)

# Salva o estado atualizado
with open(ARQUIVO_ESTADO, 'w') as f:
    json.dump(estado, f)

# --- Cria o GIF a partir dos frames salvos ---
if len(estado['frames']) > 1:
    imagens = [Image.open(f) for f in estado['frames']]
    # Salva como GIF animado (dura 200ms por frame)
    imagens[0].save(ARQUIVO_GIF,
                    save_all=True,
                    append_images=imagens[1:],
                    duration=200,
                    loop=0)
    print(f"✅ GIF animado gerado com {len(imagens)} frames.")
else:
    # Se só tem um frame, salva como PNG estático
    frame.save(ARQUIVO_GIF)
    print("✅ Apenas um frame disponível. GIF ainda não animado.")
