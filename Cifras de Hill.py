def criar_alfabeto_hill():
    """
    Alfabeto de A-Z (Z=0, A=1, ... e Y=25), conforme a convenção da Cifra de Hill no texto.
    """
    alfabeto_numeracao = {}

    # Mapear A até Y para 1 até 25
    for i in range(25):
        letra = chr(ord('A') + i)  # Obtém a letra A, B, C, ... Y
        numero = i + 1  # Mapeia para 1, 2, 3, ... 25
        alfabeto_numeracao[letra] = numero

    # Mapear Z para 0
    alfabeto_numeracao['Z'] = 0

    return alfabeto_numeracao


def matriz_codificadora():
    A = []
    for i in range(2):
        linha = []
        for j in range(2):
            valor = input(f"Escreva o valor de a[{i+1}][{j+1}]: ")
            linha.append(valor)
        A.append(linha)
    return A


def receber_palavra():
    palavra = input("Digite a palavra para ser codificada: ")  # Ver se tem que ser em letra maiúscula

    return palavra


def separar_palavra(palavra):
    palavra_separada = []

    for i in range(0, len(palavra), 2):
        palavra_separada.append(palavra[i:i+2])

    return palavra_separada


def atribuir_numero_correspondente(palavra_separada, alfabeto):
    """
    Recebe a lista de pares ['VA', 'GA', ...] e converte cada letra para seu número
    usando o alfabeto da Cifra de Hill.
    Retorna uma lista de vetores numéricos, ex: [[22,1], [7,1], ...]
    """

    palavra_numerica = []

    for par in palavra_separada:
        par = par.upper()  # garantir maiúsculas
        vetor = []

        for letra in par:
            if letra in alfabeto:
                vetor.append(alfabeto[letra])
            else:
                raise ValueError(f"Caractere inválido: {letra}")

        # Se o par for só 1 letra (ex: palavra com quantidade ímpar), completar com Z=0
        if len(vetor) == 1:
            vetor.append(0)

        palavra_numerica.append(vetor)

    return palavra_numerica


def codificar_palavra(matriz_codificadora, palavra_numerada):

    palavra_codificada_numeros = []

    n = len(matriz_codificadora)  # dimensão da matriz (ex.: 2, 3, 4...)

    for vetor in palavra_numerada:
        # cria vetor resultado com zeros
        novo_vetor = [0] * n

        # multiplicação matricial generalizada
        for i in range(n):
            soma = 0
            for j in range(n):
                soma += matriz_codificadora[i][j] * vetor[j]

            novo_vetor[i] = soma % 26  # aplicar mod 26 (Cifra de Hill)

        palavra_codificada_numeros.append(novo_vetor)

    return palavra_codificada_numeros


def atribuir_letras(palavra_codificada_numeros, alfabeto):
    """
    Recebe vetores numéricos codificados (ex.: [[3, 14], [7, 2], ...])
    e converte cada número para a letra correspondente.

    Retorna:
    - lista de dígrafos codificados: ['CO', 'GB', ...]
    - string final: 'COGB...'
    """

    # Criar dicionário inverso: número → letra
    inverso = {v: k for k, v in alfabeto.items()}

    palavra_codificada_letras = []

    for vetor in palavra_codificada_numeros:
        silaba = ""

        for numero in vetor:
            if numero in inverso:
                silaba += inverso[numero]
            else:
                raise ValueError(f"Número inválido após codificação: {numero}")

        palavra_codificada_letras.append(silaba)

    palavra_final = "".join(palavra_codificada_letras)

    return [palavra_codificada_letras, palavra_final]


matriz_codificadora = [[1, 2], [3, 5]]
palavra_separada = separar_palavra("ALGEBRALINEAR")
palavra_numerada = atribuir_numero_correspondente(palavra_separada, criar_alfabeto_hill())

palavra_codificada = codificar_palavra(matriz_codificadora, palavra_numerada)
print(f"Palavra codificada: {palavra_codificada}")

print(atribuir_letras(palavra_codificada, criar_alfabeto_hill())[1])
