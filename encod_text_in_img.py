import numpy as np
from PIL import Image
import os

def bytes_to_bits(data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in data)

def bits_to_bytes(bits: str) -> bytes:
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def embed_message(image_path, text_path, k, output_path):
    # 1. Открываем изображение
    img = Image.open(image_path).convert('L')
    arr = np.array(img)

    # 2. Читаем сообщение
    with open(text_path, 'rb') as f:
        data = f.read()

    bits = bytes_to_bits(data)

    # 3. Подготовка
    bit_index = k - 1
    flat = arr.flatten()

    max_bits = flat.size
    used_bits = min(len(bits), max_bits)

    # 4. Внедрение
    for i in range(used_bits):
        flat[i] = (flat[i] & ~(1 << bit_index)) | (int(bits[i]) << bit_index)

    # 5. Сохранение результата
    stego = flat.reshape(arr.shape)
    Image.fromarray(stego.astype(np.uint8)).save(output_path)

    print(f'Записано бит: {used_bits}')


def extract_bit_plane(image_path, k, output_path):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    print(arr)
    bit_index = k-1
    bit_plane = ((arr >> bit_index) & 1) * 255
    # print(bit_plane)
    Image.fromarray(bit_plane.astype(np.uint8)).save(output_path)


def extract_message(image_path, k, output_text_path):
    # 1. Открываем стего-изображение
    img = Image.open(image_path).convert('L')
    arr = np.array(img).flatten()  # одномерный массив пикселей

    bit_index = k - 1

    # 2. Извлекаем k-й бит каждого пикселя
    bits = ''.join(str((pixel >> bit_index) & 1) for pixel in arr)
    print(type(bits))
    # 5. Преобразуем биты обратно в байты
    message = bits_to_bytes(bits)

    # 6. Сохраняем файл
    with open(output_text_path, 'wb') as f:
        f.write(message)

    print(f'Сообщение восстановлено в файл: {output_text_path}')

path = os.getcwd()

path_imag = path + '/photo/BOSS_1.01/115.bmp'
path_imag_encod = path + '/encod.bmp'
# with open(path+'/text.txt', 'rb') as f:
#     text = f.read()
# # print(text)


# bits = bytes_to_bits(text)


# extract_bit_plane(path_imag, 8,  'ec.bmp')

embed_message(path_imag, path+'/text.txt', 1, 'encod.bmp')
extract_message(path_imag_encod, 1, 'decod.txt')

# byte_text = bits_to_text(bits)


# with open(path + '/text_decod.txt', 'wb') as f:
#     f.write(byte_text)


