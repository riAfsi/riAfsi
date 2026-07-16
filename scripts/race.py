import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime
import os

# Configuração da corrida
CARROS = ["🚗 Você", "🚙 Adversário"]
CORES = ["#ff6b6b", "#4ecdc4"]
POSICOES = [0, 0]
PISTA_LENGTH = 100

def atualizar_corrida():
    """Atualiza as posições dos carros com movimento aleatório"""
    global POSICOES
    # Movimento aleatório: cada carro avança entre 1-15 passos
    POSICOES[0] += np.random.randint(1, 15)
    POSICOES[1] += np.random.randint(1, 15)
    # Limita para não ultrapassar o final da pista
    POSICOES = [min(p, PISTA_LENGTH) for p in POSICOES]

def gerar_gif():
    """Gera um GIF animado da corrida"""
    # Cria a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, PISTA_LENGTH)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f"🏁 Corrida de Carrinhos - {datetime.now().strftime('%d/%m/%Y')}")
    
    # Desenha a pista
    ax.axhline(y=0.5, color='gray', linestyle='-', linewidth=2)
    ax.axvline(x=PISTA_LENGTH, color='red', linestyle='--', linewidth=3, label='Chegada')
    ax.legend(loc='upper right')
    
    # Lista para armazenar os frames
    frames = []
    
    # Executa a corrida por 20 passos
    for passo in range(20):
        atualizar_corrida()
        
        # Limpa os elementos anteriores
        ax.clear()
        ax.set_xlim(0, PISTA_LENGTH)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(f"🏁 Corrida de Carrinhos - {datetime.now().strftime('%d/%m/%Y')}")
        ax.axhline(y=0.5, color='gray', linestyle='-', linewidth=2)
        ax.axvline(x=PISTA_LENGTH, color='red', linestyle='--', linewidth=3, label='Chegada')
        ax.legend(loc='upper right')
        
        # Desenha os carros
        for i, (carro, pos, cor) in enumerate(zip(CARROS, POSICOES, CORES)):
            y_pos = 0.3 if i == 0 else 0.7
            ax.text(pos, y_pos, carro, fontsize=20, color=cor, fontweight='bold')
            ax.plot([pos, pos], [y_pos-0.1, y_pos+0.1], 'o', color=cor, markersize=10)
        
        # Salva o frame
        plt.draw()
        frames.append(plt.gcf())
    
    # Converte os frames em um GIF
    filename = 'race.gif'
    frames[0].save(filename, 
                   save_all=True, 
                   append_images=frames[1:], 
                   duration=300, 
                   loop=0, 
                   format='gif',
                   dpi=100)
    
    print(f"✅ GIF gerado com sucesso: {filename}")

if __name__ == "__main__":
    gerar_gif()
