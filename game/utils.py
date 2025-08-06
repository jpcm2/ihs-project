import os
from fcntl import ioctl
from time import sleep

# TODO: Verificar esse número
RD_PBUTTONS = 24930

# TODO: Verificar esse path
PATH = '/dev/mydev'

# TODO: Configurar o dicionario para fazer os movimentos corretos de 
BUTTONS_OPTIONS = {
    '0b1110': "UP", 
    '0b1101': "LEFT",
    '0b1011': "RIGHT",
    '0b111': "DOWN",
    '0b1111': "IDLE",
    '0b0000': 'QUIT'
}

# TODO: Método que le o botão.
def read_button(fd, show_output_msg):
    ioctl(fd, RD_PBUTTONS)
    button = os.read(fd, 4)
    button = bin(int.from_bytes(button, 'little'))

    if show_output_msg:
        print(f'>>> button {button}')

    return button