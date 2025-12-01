
# Cifra de Hill

import math


# 1. Funções Matemáticas Auxiliares (Aritmética Modular e Matrizes)
def mdc_estendido(a, b):
    """
    Algoritmo de Euclides Estendido.
    Retorna (g, x, y) tal que a*x + b*y = g = mdc(a, b).
    Necessário para calcular o inverso modular.
    """
    # Caso base da recursão: se 'a' for 0, o MDC é 'b' e os coeficientes são 0 e 1
    if a == 0:
        return b, 0, 1
    else:
        # Chamada recursiva: continua dividindo até chegar no caso base
        g, y, x = mdc_estendido(b % a, a)
        # Retorna o MDC e atualiza os coeficientes x e y
        return g, x - (b // a) * y, y


def inverso_modular(a, m):
    """
    Calcula o inverso multiplicativo de 'a' módulo 'm'.
    Retorna x tal que (a * x) % m == 1.
    """
    # Chama o algoritmo de Euclides estendido para encontrar o MDC e os coeficientes
    g, x, y = mdc_estendido(a, m)

    # Verifica se o MDC é 1 (condição para existir inverso)
    if g != 1:
        return None  # Não existe inverso se não forem primos entre si
    else:
        # Garante que o resultado seja positivo usando o operador módulo
        return (x % m + m) % m


def criar_matriz_nula(linhas, colunas):
    """Cria uma matriz preenchida com zeros."""
    matriz = []
    # Executa um loop para criar cada linha da matriz
    for _ in range(linhas):
        # Cria uma lista de zeros com o tamanho das colunas e adiciona à matriz
        matriz.append([0] * colunas)
    return matriz


def transposta(matriz):
    """Calcula a transposta de uma matriz (troca linhas por colunas)."""
    linhas = len(matriz)
    colunas = len(matriz[0])
    # Cria uma matriz nula para armazenar o resultado
    t = criar_matriz_nula(colunas, linhas)

    # Executa um loop para percorrer as linhas da matriz original
    for i in range(linhas):
        # Executa um loop aninhado para percorrer as colunas
        for j in range(colunas):
            # Troca os índices: o elemento [i][j] vira [j][i] na transposta
            t[j][i] = matriz[i][j]
    return t


def menor_complementar(matriz, i, j):
    """
    Retorna a submatriz removendo a linha i e a coluna j.
    Necessário para o cálculo de determinantes (Laplace) e matriz de cofatores.
    """
    submatriz = []
    # Executa um loop para percorrer todas as linhas da matriz original
    for linha_idx in range(len(matriz)):
        # Se a linha atual for a que deve ser removida (i), pula para a próxima
        if linha_idx == i: continue

        nova_linha = []
        # Executa um loop para percorrer todas as colunas
        for col_idx in range(len(matriz[0])):
            # Se a coluna atual for a que deve ser removida (j), pula
            if col_idx == j: continue

            # Adiciona o elemento à nova linha
            nova_linha.append(matriz[linha_idx][col_idx])

        # Adiciona a linha construída à submatriz
        submatriz.append(nova_linha)
    return submatriz


def calcular_determinante(matriz):
    """
    Calcula o determinante de uma matriz n x n recursivamente (Expansão de Laplace).
    """
    n = len(matriz)
    # Caso base 1: matriz 1x1, o determinante é o próprio elemento
    if n == 1: return matriz[0][0]
    # Caso base 2: matriz 2x2, aplica a fórmula ad - bc
    if n == 2: return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    det = 0
    # Executa um loop para aplicar a Expansão de Laplace na primeira linha
    for j in range(n):
        # Alterna o sinal (+, -, +, ...) dependendo da posição da coluna
        sinal = (-1) ** j
        # Chama recursivamente a função para calcular o determinante da submatriz menor
        sub_det = calcular_determinante(menor_complementar(matriz, 0, j))
        # Soma ao total: elemento * sinal * sub-determinante
        det += sinal * matriz[0][j] * sub_det
    return det


def matriz_adjunta(matriz):
    """
    Calcula a matriz adjunta (transposta da matriz de cofatores).
    """
    n = len(matriz)
    cofatores = criar_matriz_nula(n, n)

    if n == 1: return [[1]]

    # Executa um loop para percorrer as linhas
    for i in range(n):
        # Executa um loop aninhado para percorrer as colunas
        for j in range(n):
            # Obtém a submatriz removendo linha i e coluna j
            menor = menor_complementar(matriz, i, j)
            # Calcula o determinante dessa submatriz
            det_menor = calcular_determinante(menor)
            # Aplica a regra de sinais dos cofatores
            sinal = (-1) ** (i + j)
            # Armazena o cofator na posição correspondente
            cofatores[i][j] = sinal * det_menor

    # Retorna a transposta da matriz de cofatores (que é a adjunta)
    return transposta(cofatores)


def matriz_inversa_modular(matriz, m):
    """
    Calcula a inversa da matriz módulo m.
    Fórmula: K^-1 = (det^-1) * adj(K) (mod m)
    """
    # Calcula o determinante da matriz original
    det = calcular_determinante(matriz)
    # Aplica o módulo m ao determinante
    det = det % m

    # Tenta encontrar o inverso modular do determinante
    inv_det = inverso_modular(det, m)

    # Se não houver inverso (ex: determinante é 0 ou tem fator comum com m), retorna erro
    if inv_det is None: return None

    # Calcula a matriz adjunta
    adj = matriz_adjunta(matriz)
    n = len(matriz)
    inversa = criar_matriz_nula(n, n)

    # Executa loops aninhados para multiplicar a adjunta pelo inverso do determinante
    for i in range(n):
        for j in range(n):
            # Aplica a multiplicação e o módulo m para cada elemento
            inversa[i][j] = (adj[i][j] * inv_det) % m

    return inversa


def multiplicar_matriz_vetor(matriz, vetor, m):
    """
    Multiplica uma matriz n x n por um vetor coluna n x 1, módulo m.
    """
    n = len(matriz)
    resultado = [0] * n

    # Executa um loop para percorrer cada linha da matriz
    for i in range(n):
        soma = 0
        # Executa um loop aninhado para multiplicar linha da matriz pela coluna do vetor
        for j in range(n):
            soma += matriz[i][j] * vetor[j]
        # Armazena o resultado aplicando o módulo m
        resultado[i] = soma % m

    return resultado


# 2. Funções de Texto e Interface (CORRIGIDAS PARA A=1...Z=0)
def texto_para_numeros(texto):
    """
    Converte letras A-Z para números seguindo a regra:
    A=1, B=2, ..., Y=25, Z=0
    """
    numeros = []
    # Executa um loop para percorrer cada caractere da string
    for char in texto:
        if 'A' <= char <= 'Z':
            # Calcula o valor numérico: A(ASCII 65) vira 1
            val = ord(char) - ord('A') + 1
            # Se o valor for 26, converte para 0 (letra Z)
            if val == 26: val = 0
            numeros.append(val)
    return numeros


def numeros_para_texto(numeros):
    """
    Converte números 0-25 para letras A-Z seguindo a regra:
    1=A, ..., 25=Y, 0=Z
    """
    texto = ""
    # Executa um loop para percorrer cada número da lista
    for num in numeros:
        # Se for 0, converte manualmente para 'Z'
        if num == 0:
            texto += 'Z'
        else:
            # Se for 1-25, converte para caractere ASCII (1 vira A, 2 vira B...)
            texto += chr(num - 1 + ord('A'))
    return texto


def receber_matriz_usuario(n, m):
    """Pede ao usuário os elementos da matriz n x n."""
    print(f"\nDigite os elementos da Matriz Chave ({n}x{n}) linha por linha:")
    matriz = []

    # Executa um loop para preencher cada linha (i)
    for i in range(n):
        linha = []
        print(f"Linha {i + 1}:")
        # Executa um loop para preencher cada coluna (j) dessa linha
        for j in range(n):
            while True:
                try:
                    val = int(input(f"  Elemento [{i + 1},{j + 1}]: "))
                    # Adiciona o valor à linha já aplicando o módulo para garantir validade
                    linha.append(val % m)
                    break
                except ValueError:
                    print("  Erro: Digite um número inteiro.")
        # Adiciona a linha completa à matriz
        matriz.append(linha)
    return matriz


# 3. Função Principal
def main():
    print("=== Cifra de Hill Generalizada (A=1...Z=0) ===")
    print("Requisitos: Matriz n x n, Módulo m, Inversibilidade.\n")

    # 1. Entrada de Parâmetros
    while True:
        try:
            m = int(input("1. Digite o módulo m (ex: 26): "))
            if m < 2: raise ValueError
            break
        except ValueError:
            print("Por favor, digite um inteiro válido maior que 1.")

    while True:
        try:
            n = int(input("2. Digite a ordem da matriz n (ex: 2 ou 3): "))
            if n < 1: raise ValueError
            break
        except ValueError:
            print("Por favor, digite um inteiro positivo.")

    # 2. Leitura e Validação da Matriz
    # Executa um loop infinito até que o usuário forneça uma matriz válida (invertível)
    while True:
        A = receber_matriz_usuario(n, m)
        print(f"\nMatriz lida:\n{A}")

        # Calcula o determinante para verificar inversibilidade
        det = calcular_determinante(A) % m
        mdc_val, _, _ = mdc_estendido(det, m)

        print(f"Determinante: {det}")
        print(f"MDC(det, m): {mdc_val}")

        # Se o MDC entre o determinante e o módulo for 1, a matriz tem inversa
        if mdc_val == 1:
            print("-> SUCESSO: Matriz é invertível módulo", m)
            # Calcula a matriz inversa para uso futuro na decodificação
            A_inv = matriz_inversa_modular(A, m)
            print(f"-> Matriz Inversa calculada:\n{A_inv}\n")
            break
        else:
            print(f"-> ERRO: Matriz NÃO é invertível (mdc != 1).")
            opt = input("Deseja tentar outra matriz? (S/N): ").upper()
            if opt != 'S':
                return

    # 3. Leitura e Preparação da Mensagem
    texto_raw = input("3. Digite a mensagem (apenas letras A-Z): ").upper().replace(" ", "")
    # Cria uma nova string contendo apenas caracteres que são letras
    texto_limpo = "".join([c for c in texto_raw if c.isalpha()])

    # Ajuste de tamanho (Padding com Z) para completar o bloco
    resto = len(texto_limpo) % n
    if resto != 0:
        faltam = n - resto
        texto_limpo += 'Z' * faltam  # Adiciona Zs ao final
        print(f"-> Texto ajustado (completado com Z): {texto_limpo}")

    # Converte o texto limpo para vetor numérico
    vetor_numerico = texto_para_numeros(texto_limpo)

    # 4. Cifragem e Decifragem
    print("\n--- RESULTADOS ---")
    print(f"Mensagem Original: {texto_limpo}")

    blocos_cifrados = []
    # Executa um loop pulando de n em n para processar cada bloco da mensagem
    for i in range(0, len(vetor_numerico), n):
        # Seleciona o bloco atual (fatia da lista)
        bloco = vetor_numerico[i:i + n]
        # Multiplica a Matriz Chave pelo bloco atual
        bloco_cifrado = multiplicar_matriz_vetor(A, bloco, m)
        # Adiciona o resultado à lista final
        blocos_cifrados.extend(bloco_cifrado)

    # Converte os números cifrados de volta para letras
    msg_cifrada = numeros_para_texto(blocos_cifrados)
    print(f"Mensagem Cifrada:  {msg_cifrada}")

    # Decifragem (Prova Real)
    blocos_decifrados = []
    # Executa um loop similar para decifrar, usando a Matriz Inversa
    for i in range(0, len(blocos_cifrados), n):
        bloco = blocos_cifrados[i:i + n]
        # Multiplica a Matriz Inversa pelo bloco cifrado
        bloco_decifrado = multiplicar_matriz_vetor(A_inv, bloco, m)
        blocos_decifrados.extend(bloco_decifrado)

    msg_decodificada = numeros_para_texto(blocos_decifrados)
    print(f"Decodificada:      {msg_decodificada}")

    # Verifica se a decodificação retornou ao texto original
    if msg_decodificada == texto_limpo:
        print("\n[SUCESSO] A mensagem decodificada corresponde à original.")
    else:
        print("\n[FALHA] Houve algum erro no processo matemático.")


if __name__ == "__main__":
    main()
