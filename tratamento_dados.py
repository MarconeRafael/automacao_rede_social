import pandas as pd

def process_csv(csv_path, minimo_seguidores, maximo_seguidores):
    """
    Processa um arquivo CSV para:
    - Renomear colunas específicas.
    - Remover linhas com valores nulos em colunas críticas ('bio', 'Niche').
    - Filtrar apenas colunas que não possuem valores nulos.
    - Filtrar contas empresariais e dentro do intervalo de seguidores.
    - Selecionar variáveis desejadas.
    - Salvar o resultado em um novo arquivo CSV.
    
    Parâmetros:
    - csv_path (str): Caminho do arquivo CSV de entrada.
    - minimo_seguidores (int): Número mínimo de seguidores.
    - maximo_seguidores (int): Número máximo de seguidores.

    Retorna:
    - filtered_csv_path (str): Caminho do arquivo CSV filtrado gerado.
    """
    # Carrega o arquivo CSV em um DataFrame
    dataset = pd.read_csv(csv_path)

    # Renomeia colunas
    rename_columns = {
        'username': 'Username',
        'biography': 'bio',
        'followersCount': 'seguidores',
        'businessCategoryName': 'Niche'
    }
    dataset.rename(columns=rename_columns, inplace=True)

    # Garante que as colunas 'bio' e 'Niche' estejam presentes no DataFrame
    required_columns = ['bio', 'Niche']
    for col in required_columns:
        if col not in dataset.columns:
            raise ValueError(f"A coluna obrigatória '{col}' não foi encontrada no dataset.")

    # Remove linhas com valores nulos em 'bio' e 'Niche'
    dataset = dataset.dropna(subset=required_columns)

    # Filtra apenas as colunas que não têm valores nulos, mas mantém as obrigatórias
    non_null_columns = dataset.dropna(axis=1).columns
    essential_columns = set(required_columns).intersection(dataset.columns)
    filtered_columns = list(essential_columns.union(non_null_columns))
    filtered_dataset = dataset[filtered_columns]

    # Selecionar apenas as variáveis desejadas
    variaveis_desejadas = ['seguidores', 'fullName', 'isBusinessAccount', 'private', 'url', 'username', 'bio', 'Niche']
    selected_columns = [col for col in variaveis_desejadas if col in filtered_dataset.columns]
    filtered_subset = filtered_dataset[selected_columns]

    # **Nova filtragem**
    # Filtrar por contas empresariais
    if 'isBusinessAccount' in filtered_subset.columns:
        filtered_subset = filtered_subset[filtered_subset['isBusinessAccount'] == True]

    # Filtrar pelo número de seguidores
    if 'seguidores' in filtered_subset.columns:
        filtered_subset = filtered_subset[
            (filtered_subset['seguidores'] >= minimo_seguidores) &
            (filtered_subset['seguidores'] <= maximo_seguidores)
        ]

    # Exibir um exemplo de cada coluna selecionada
    print("\nExemplo de cada coluna (após remoção de nulos, renomeação e filtros):")
    for feature in filtered_subset.columns:
        print(f"{feature}: {filtered_subset[feature].iloc[0] if not filtered_subset[feature].empty else 'N/A'}")

    # Exibe informações do DataFrame filtrado
    print("\nInformações do Dataset filtrado:")
    print(filtered_subset.info())

    # Salva o DataFrame filtrado em um novo arquivo CSV
    filtered_csv_path = "csvs/dados.csv"
    filtered_subset.to_csv(filtered_csv_path, index=False)
    print(f"\nNovo arquivo CSV salvo em: {filtered_csv_path}")
    print(len(filtered_subset))
    return filtered_csv_path
