def criar_alfabeto_hill():
    alfabeto_numeracao = {}
    for i in range(25):
        letra = chr(ord('A') + i)
        numero = i + 1
        alfabeto_numeracao[letra] = numero
    alfabeto_numeracao['Z'] = 0
    return alfabeto_numeracao


def receber_matriz_codificadora():
    A = []
    for i in range(2):
        linha = []
        for j in range(2):
            valor = int(input(f"Escreva o valor de a[{i+1}][{j+1}]: "))
            linha.append(valor)
        A.append(linha)
    return A


def receber_palavra():
    return input("Digite a palavra para ser codificada: ")


def separar_palavra(palavra):
    return [palavra[i:i+2] for i in range(0, len(palavra), 2)]


def atribuir_numero_correspondente(palavra_separada, alfabeto):
    palavra_numerica = []
    for par in palavra_separada:
        par = par.upper()
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


def codificar_palavra(matriz_codificadora, palavra_numerada):
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


def atribuir_letras(palavra_codificada_numeros, alfabeto):
    inverso = {v: k for k, v in alfabeto.items()}
    palavra = "".join("".join(inverso[num] for num in vetor)
                      for vetor in palavra_codificada_numeros)
    return palavra


def calcular_determinante_2x2(matriz):
    a, b = matriz[0]
    c, d = matriz[1]
    return (a*d - b*c) % 26


def inverso_multiplicativo_mod26(numero):
    for x in range(26):
        if (numero * x) % 26 == 1:
            return x
    raise ValueError(f"Não existe inverso multiplicativo para {numero} no módulo 26.")


def calcular_matriz_inversa_2x2(matriz):
    det = calcular_determinante_2x2(matriz)
    inv_det = inverso_multiplicativo_mod26(det)

    a, b = matriz[0]
    c, d = matriz[1]

    return [
        [(d * inv_det) % 26, (-b * inv_det) % 26],
        [(-c * inv_det) % 26, (a * inv_det) % 26]
    ]


def decodificar_palavra(matriz_inversa, palavra_codificada_numeros):
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


def main():
    alfabeto = criar_alfabeto_hill()
    matriz = receber_matriz_codificadora()
    palavra = receber_palavra()
    print(f"Palavra original: {palavra.upper()}")

    palavra_separada = separar_palavra(palavra)
    palavra_numerada = atribuir_numero_correspondente(palavra_separada, alfabeto)

    codificada = codificar_palavra(matriz, palavra_numerada)
    print("Codificada:", atribuir_letras(codificada, alfabeto))

    matriz_inv = calcular_matriz_inversa_2x2(matriz)
    decodificada_num = decodificar_palavra(matriz_inv, codificada)
    print("Decodificada:", atribuir_letras(decodificada_num, alfabeto))


main()
