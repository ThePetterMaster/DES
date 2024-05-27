import itertools

# Tabelas de permutação e S-boxes para o DES
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 13, 15, 1, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

def permute(block, table):
    """
    Permuta os bits de 'block' de acordo com a tabela 'table'.
    """
    return [block[x-1] for x in table]

def sbox(input, sbox):
    """
    Aplica a substituição S-Box a um grupo de 6 bits.
    
    Parâmetros:
    - input: Grupo de 6 bits a ser transformado.
    - sbox: A S-Box a ser usada para a transformação.
    
    Retorna:
    - Lista de 4 bits resultantes da transformação.
    """
    # Determina a linha da S-Box usando o primeiro e último bit de entrada
    row = int(f"{input[0]}{input[5]}", 2)
    # Determina a coluna da S-Box usando os 4 bits do meio
    col = int(''.join([str(x) for x in input[1:5]]), 2)
    # Obtém o valor da S-Box correspondente à linha e coluna
    return [int(x) for x in f"{sbox[row][col]:04b}"]

def feistel(right, key):
    """
    Função Feistel: expansão, XOR, substituição e permutação.
    
    Parâmetros:
    - right: Metade direita do bloco (32 bits).
    - key: Subchave para a rodada atual (48 bits).
    
    Retorna:
    - A saída permutada de 32 bits após as operações Feistel.
    """
    # Expansão: A metade direita (32 bits) é expandida para 48 bits
    expanded = permute(right, E)
    
    # XOR: A metade direita expandida é XORed com a subchave de 48 bits
    xor_result = [expanded[i] ^ key[i] for i in range(48)]
    
    # Substituição (S-Boxes): Divide o resultado do XOR em 8 grupos de 6 bits
    sbox_result = []
    for i in range(8):
        sbox_input = xor_result[i * 6:(i + 1) * 6]
        sbox_output = sbox(sbox_input, S[i])
        sbox_result.extend(sbox_output)
    
    # Permutação: Permuta os 32 bits de saída das S-Boxes
    return permute(sbox_result, P)


def des_encrypt_block(block, keys):
    """
    Criptografa um bloco de 64 bits usando DES.
    """
    # Permutação inicial
    block = permute(block, IP)
    left, right = block[:32], block[32:]

    # 16 rodadas do DES
    for key in keys:
        new_right = [left[i] ^ x for i, x in enumerate(feistel(right, key))]
        left = right
        right = new_right

    # Permutação final
    return permute(right + left, FP)

def string_to_bit_array(text):
    """
    Converte uma string em um array de bits.
    """
    array = []
    for char in text:
        binval = bin(ord(char))[2:].zfill(8)
        array.extend([int(x) for x in binval])
    return array

def bit_array_to_string(array):
    """
    Converte um array de bits de volta para uma string.
    """
    result = []
    for i in range(0, len(array), 8):
        byte = array[i:i+8]
        result.append(chr(int(''.join([str(x) for x in byte]), 2)))
    return ''.join(result)

def pad(text):
    """
    Adiciona padding ao texto para que seu tamanho seja múltiplo de 8 bytes.
    """
    while len(text) % 8 != 0:
        text += ' '
    return text

def generate_keys(key):
    """
    Gera 16 subchaves para as 16 rodadas do DES.
    """
    return [key] * 16  # Simplificação: 16 chaves iguais

def des_encrypt(key, text):
    """
    Encripta um texto usando DES.
    """
    text = pad(text)
    bit_text = string_to_bit_array(text)
    keys = generate_keys(string_to_bit_array(key))
    encrypted_blocks = []
    for i in range(0, len(bit_text), 64):
        block = bit_text[i:i+64]
        encrypted_block = des_encrypt_block(block, keys)
        encrypted_blocks.extend(encrypted_block)
    return bit_array_to_string(encrypted_blocks)

def des_decrypt(key, text):
    """
    Decripta um texto usando DES.
    """
    bit_text = string_to_bit_array(text)
    keys = generate_keys(string_to_bit_array(key))[::-1]
    decrypted_blocks = []
    for i in range(0, len(bit_text), 64):
        print(i)
        block = bit_text[i:i+64]
        decrypted_block = des_encrypt_block(block, keys)
        decrypted_blocks.extend(decrypted_block)
    return bit_array_to_string(decrypted_blocks).strip()

# Exemplo de uso
key = '8bytekey'  # A chave deve ter 8 caracteres (64 bits)
text = 'Hello, World!'

encrypted = des_encrypt(key, text)
print(f"Encrypted: {encrypted}")

decrypted = des_decrypt(key, encrypted)
print(f"Decrypted: {decrypted}")
