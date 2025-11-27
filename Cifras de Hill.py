# Cifras de Hill com matriz 2x2

def criar_alfabeto_hill():
    """
    Cria a tabela de conversão: troca letras por números (A=1, B=2... Z=0).
    """
    alfabeto_numeracao = {}
    
    # Executa um loop (repetição) 25 vezes para criar as letras de A até Y
    for i in range(25):
        letra = chr(ord('A') + i)  # Gera a letra atual
        numero = i + 1             # Define o número correspondente (A=1, B=2...)
        alfabeto_numeracao[letra] = numero # Salva na tabela
        
    # Define manualmente que a letra Z vale 0
    alfabeto_numeracao['Z'] = 0
    return alfabeto_numeracao


# Teste:
# print(criar_alfabeto_hill())


def receber_matriz_codificadora():
    """
    Pede ao usuário a 'senha' (chave): 4 números que vão embaralhar a mensagem.
    """
    A = []
    print("Digite os valores da Matriz multiplicadora 2x2.")
    
    # Executa um loop para preencher as 2 linhas da matriz
    for i in range(2):
        linha = []
        # Executa um loop interno para preencher as 2 colunas de cada linha
        for j in range(2):
            # Pede o número para o usuário e converte para número inteiro
            valor = int(input(f"Escreva o valor de a[{i+1}][{j+1}]: "))
            linha.append(valor) # Adiciona o número na linha atual
        A.append(linha) # Adiciona a linha completa na matriz
    return A


# Teste
# receber_matriz_codificadora()


def receber_palavra():
    """
    Pede a palavra que será transformada em código.
    """
    # Exibe a mensagem na tela e aguarda o usuário digitar
    return input("Digite a palavra para ser codificada: ")


# Teste:
# print(receber_palavra())


def separar_palavra(palavra):
    """
    Divide a palavra em duplas de letras. Ex: 'CASA' vira 'CA' e 'SA'.
    """
    # Cria uma lista pegando pedaços da palavra de 2 em 2
    return [palavra[i:i+2] for i in range(0, len(palavra), 2)]


# Teste:
# print(separar_palavra("algebralinear"))


def atribuir_numero_correspondente(palavra_separada, alfabeto):
    """
    Troca as letras pelos números da tabela. Se sobrar letra sozinha, adiciona um 0.
    """
    palavra_numerica = []
    
    # Executa um loop para processar cada par de letras (ex: "CA")
    for par in palavra_separada:
        par = par.upper()  # Garante que a letra seja maiúscula
        vetor = []
        
        # Executa um loop para converter cada letra do par em número
        for letra in par:
            if letra in alfabeto:
                vetor.append(alfabeto[letra]) # Adiciona o número correspondente
            else:
                raise ValueError(f"Caractere inválido: {letra}")

        # Verifica se sobrou uma letra sozinha (ímpar) e adiciona 0 para completar o par
        if len(vetor) == 1:
            vetor.append(0)
            
        palavra_numerica.append(vetor)
    return palavra_numerica


# Teste:
# print(atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill()))


def codificar_palavra(matriz_codificadora, palavra_numerada):
    """
    Faz a conta matemática para misturar a mensagem.
    """
    palavra_codificada_numeros = []
    n = len(matriz_codificadora) # Define o tamanho da matriz (2)

    # Executa um loop para cada par de números da mensagem original
    for vetor in palavra_numerada:
        novo_vetor = [0] * n
        
        # Executa loops para fazer a multiplicação de matrizes (Linha x Coluna)
        for i in range(n):
            soma = 0
            for j in range(n):
                # Multiplica o número da chave pelo número da letra e soma
                soma += matriz_codificadora[i][j] * vetor[j]
            
            # Aplica o resto da divisão por 26 para garantir que vire uma letra válida (0-25)
            novo_vetor[i] = soma % 26
            
        palavra_codificada_numeros.append(novo_vetor)

    return palavra_codificada_numeros


# Teste:
# palavra_numerada = atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill())
# print(codificar_palavra([[1, 2], [3, 5]], palavra_numerada))


def atribuir_letras(palavra_codificada_numeros, alfabeto):
    """
    Transforma os números (já misturados) de volta em letras para exibir o código.
    """
    # Cria uma tabela invertida para procurar a Letra através do Número
    inverso = {v: k for k, v in alfabeto.items()}
    
    # Junta todos os caracteres encontrados em uma única frase
    palavra = "".join("".join(inverso[num] for num in vetor)
                      for vetor in palavra_codificada_numeros)
    return palavra


# Teste
# palavra_numerada = atribuir_numero_correspondente(separar_palavra("algebralinear"), criar_alfabeto_hill())
# palavra_codificada = codificar_palavra([[1, 2], [3, 5]], palavra_numerada)
# print(atribuir_letras(palavra_codificada, criar_alfabeto_hill()))


def calcular_determinante_2x2(matriz):
    """
    Cálculo necessário para saber se é possível decifrar (desfazer) o código depois.
    """
    a, b = matriz[0]
    c, d = matriz[1]
    # Fórmula matemática do determinante com módulo 26
    return (a*d - b*c) % 26


# Teste
# print(calcular_determinante_2x2([[1, 2], [3, 5]]))  # 25


def inverso_multiplicativo_mod26(numero):
    """
    Encontra um número especial necessário para a matemática da decodificação funcionar.
    """
    # Testa números de 0 a 25 para ver qual serve como inverso
    for x in range(26):
        if (numero * x) % 26 == 1:
            return x # Retorna o número se encontrar
            
    # Se terminar o loop e não achar, avisa que deu erro
    raise ValueError(f"Não existe inverso multiplicativo para {numero} no módulo 26.")


# Teste:
# print(inverso_multiplicativo_mod26(25))  # 25


def calcular_matriz_inversa_2x2(matriz):
    """
    Cria a 'chave inversa' que serve para desfazer a bagunça e ler a mensagem original.
    """
    # Calcula os valores auxiliares necessários
    det = calcular_determinante_2x2(matriz)
    inv_det = inverso_multiplicativo_mod26(det)

    a, b = matriz[0]
    c, d = matriz[1]

    # Monta a nova matriz trocando posições e sinais, ajustando pelo módulo 26
    return [
        [(d * inv_det) % 26, (-b * inv_det) % 26],
        [(-c * inv_det) % 26, (a * inv_det) % 26]
    ]


# Teste:
# print(calcular_matriz_inversa_2x2([[1, 2], [3, 5]]))


def decodificar_palavra(matriz_inversa, palavra_codificada_numeros):
    """
    Usa a chave inversa para transformar o código bagunçado de volta nos números originais.
    """
    palavra = []
    n = len(matriz_inversa)

    # Executa a mesma lógica da codificação, mas usando a matriz inversa
    for vetor in palavra_codificada_numeros:
        novo = [0] * n
        for i in range(n):
            soma = 0
            for j in range(n):
                soma += matriz_inversa[i][j] * vetor[j]
            novo[i] = soma % 26 # Garante o intervalo 0-25
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
    Função principal: Organiza a execução de todas as etapas.
    """
    # 1. Gera o alfabeto
    alfabeto = criar_alfabeto_hill()
    
    # 2. Pede os dados para o usuário
    matriz = receber_matriz_codificadora()
    palavra = receber_palavra()
    print(f"Palavra original: {palavra.upper()}")

    # 3. Prepara a palavra (separa e converte para números)
    palavra_separada = separar_palavra(palavra)
    palavra_numerada = atribuir_numero_correspondente(palavra_separada, alfabeto)

    # 4. Cifra a palavra (transforma em código secreto)
    codificada = codificar_palavra(matriz, palavra_numerada)
    print("Cifrada:", atribuir_letras(codificada, alfabeto))

    # 5. Decifra a palavra (traz de volta ao original para confirmar)
    matriz_inv = calcular_matriz_inversa_2x2(matriz)
    decodificada_num = decodificar_palavra(matriz_inv, codificada)
    print("Decodificada:", atribuir_letras(decodificada_num, alfabeto))


# Inicia o programa
main()
