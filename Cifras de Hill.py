# Cifras de Hill com matriz 2x2


def criar_alfabeto_hill():
    """
    Cria o alfabeto usado na Cifra de Hill.

    Regras:
    - A → 1, B → 2, ..., Y → 25
    - Z → 0
    """
    alfabeto_numeracao = {}
    for i in range(25):
        letra = chr(ord('A') + i)
        numero = i + 1
        alfabeto_numeracao[letra] = numero
    alfabeto_numeracao['Z'] = 0
    return alfabeto_numeracao


# Teste:
# print(criar_alfabeto_hill())


def receber_matriz_codificadora():
    """
    Lê do usuário os 4 valores da matriz codificadora 2x2.
    """

    A = []
    print("Digite os valores da Matriz multiplicadora 2x2.")
    for i in range(2):
        linha = []
        for j in range(2):
            valor = int(input(f"Escreva o valor de a[{i+1}][{j+1}]: "))
            linha.append(valor)
        A.append(linha)
    return A


# Teste
# receber_matriz_codificadora()


def receber_palavra():
    """
    Obtém a palavra que será codificada pelo usuário.
    """
    return input("Digite a palavra para ser codificada: ")


# Teste:
# print(receber_palavra())


def separar_palavra(palavra):
    """
    Separa a palavra em blocos de 2 letras.
    """
    return [palavra[i:i+2] for i in range(0, len(palavra), 2)]


# Teste:
# print(separar_palavra("algebralinear"))


def atribuir_numero_correspondente(palavra_separada, alfabeto):
    """
    Converte cada par de caracteres para seus números equivalentes no alfabeto Hill.
    """
    palavra_numerica = []
    for par in palavra_separada:
        par = par.upper()  # Converte para letra maiúscula
        vetor = []
        for letra in par:
            if letra in alfabeto:
                vetor.append(alfabeto[letra])
            else:
                raise ValueError(f"Caractere inválido: {letra}")

        if len(vetor) == 1:
            vetor.append(0)
        palavra_numerica.append(vetor)
    return palavra_numerica


# Teste:
# print(atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill()))


def codificar_palavra(matriz_codificadora, palavra_numerada):
    """
    Aplica a multiplicação matricial entre a matriz codificadora e cada vetor da palavra.
    """
    palavra_codificada_numeros = []
    n = len(matriz_codificadora)

    for vetor in palavra_numerada:
        novo_vetor = [0] * n
        for i in range(n):
            soma = 0
            for j in range(n):
                soma += matriz_codificadora[i][j] * vetor[j]
            novo_vetor[i] = soma % 26
        palavra_codificada_numeros.append(novo_vetor)

    return palavra_codificada_numeros


# Teste:
# palavra_numerada = atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill())
# print(codificar_palavra([[1, 2], [3, 5]], palavra_numerada))


def atribuir_letras(palavra_codificada_numeros, alfabeto):
    """
    Converte uma lista de números de volta para letras do alfabeto Hill.
    """
    inverso = {v: k for k, v in alfabeto.items()}
    palavra = "".join("".join(inverso[num] for num in vetor)
                      for vetor in palavra_codificada_numeros)
    return palavra


# Teste
# palavra_numerada = atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill())
# palavra_codificada = codificar_palavra([[1, 2], [3, 5]], palavra_numerada)
# print(atribuir_letras(palavra_codificada, criar_alfabeto_hill()))


def calcular_determinante_2x2(matriz):
    """
    Calcula o determinante de uma matriz 2x2 no módulo 26.
    """
    a, b = matriz[0]
    c, d = matriz[1]
    return (a*d - b*c) % 26


# Teste
# print(calcular_determinante_2x2([[1, 2], [3, 5]]))  # 25


def inverso_multiplicativo_mod26(numero):
    """
    Calcula o inverso multiplicativo no módulo 26.
    """
    for x in range(26):
        if (numero * x) % 26 == 1:
            return x
    raise ValueError(f"Não existe inverso multiplicativo para {numero} no módulo 26.")


# Teste:
# print(inverso_multiplicativo_mod26(25))  # 25


def calcular_matriz_inversa_2x2(matriz):
    """
    Calcula a matriz inversa 2x2 no módulo 26.
    """
    det = calcular_determinante_2x2(matriz)
    inv_det = inverso_multiplicativo_mod26(det)

    a, b = matriz[0]
    c, d = matriz[1]

    return [
        [(d * inv_det) % 26, (-b * inv_det) % 26],
        [(-c * inv_det) % 26, (a * inv_det) % 26]
    ]


# Teste:
# print(calcular_matriz_inversa_2x2([[1, 2], [3, 5]]))


def decodificar_palavra(matriz_inversa, palavra_codificada_numeros):
    """
    Decodifica a palavra multiplicando cada vetor pela matriz inversa.
    """
    palavra = []
    n = len(matriz_inversa)

    for vetor in palavra_codificada_numeros:
        novo = [0] * n
        for i in range(n):
            soma = 0
            for j in range(n):
                soma += matriz_inversa[i][j] * vetor[j]
            novo[i] = soma % 26
        palavra.append(novo)

    return palavra


# Teste
# alfabeto = criar_alfabeto_hill()
# matriz = [[1, 2], [3, 5]]
#
# palavra = "algebralinear"
# print(f"Palavra original: {palavra}")
#
# separada = separar_palavra(palavra)
# numerada = atribuir_numero_correspondente(separada, alfabeto)
# codificada = codificar_palavra(matriz, numerada)
# matriz_inv = calcular_matriz_inversa_2x2(matriz)
# decodificada_num = decodificar_palavra(matriz_inv, codificada)
#
# decodificada = decodificar_palavra(matriz_inv, codificada)
# print("Decodificada (números):", decodificada)
# print("Decodificada (letras):", atribuir_letras(decodificada, alfabeto))


def main():
    """
    Função principal do programa:
    - Cria o alfabeto
    - Lê a matriz codificadora
    - Lê a palavra
    - Codifica
    - Decodifica
    """
    alfabeto = criar_alfabeto_hill()
    matriz = receber_matriz_codificadora()
    palavra = receber_palavra()
    print(f"Palavra original: {palavra.upper()}")

    palavra_separada = separar_palavra(palavra)
    palavra_numerada = atribuir_numero_correspondente(palavra_separada, alfabeto)

    codificada = codificar_palavra(matriz, palavra_numerada)
    print("Cifrada:", atribuir_letras(codificada, alfabeto))

    matriz_inv = calcular_matriz_inversa_2x2(matriz)
    decodificada_num = decodificar_palavra(matriz_inv, codificada)
    print("Decodificada:", atribuir_letras(decodificada_num, alfabeto))


main()
