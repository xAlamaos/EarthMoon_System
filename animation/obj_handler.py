def parse_obj_file(filename):
    """
    Função para analisar um ficheiro '.obj' e extrair os vértices e faces
    :param filename: Nome do ficheiro '.obj' a ser analisado
    :return: Uma tuplo contendo as listas de vértices e faces do ficheiro
    """
    vertices = []  # Lista para armazenar os vértices
    faces = []  # Lista para armazenar as faces

    # Abertura do ficheiro '.obj' para leitura
    for line in open(filename, 'r'):
        # Ignorar comentários dentro do ficheiro
        if line.startswith('#'):
            continue
        # Dividir as linhas em valores separados por um espaço
        values = line.split()
        # Se a linha estiver vazia, irá ser ignorada
        if not values:
            continue

        # Se a linha começar com 'v', significa que é um vértice
        if values[0] == 'v':
            # Adicionar os valores de vértice à lista (convertidos para float)
            vertices.append(list(map(float, values[1:4])))
        # Se a linha começar com 'f', significa que é uma face
        elif values[0] == 'f':
            face = []  # Inicialização da lista para armazenar os índices dos vértices da face
            # Para cada índice de vértice na definição de face
            for v in values[1:]:
                # Divisão de índices por '/'
                w = v.split('/')
                # Subtrair 1, porque o Python indexa a partir de 0 enquanto os arquivos .obj indexam a partir de 1
                face.append(int(w[0]) - 1)
            # Adicionar a face à lista de faces
            faces.append(face)
    return vertices, faces
