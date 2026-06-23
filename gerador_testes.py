import random
import time

from estruturas import No, ListaDuplamenteEncadeada

def gerar_ordens_aleatorias(quantidade_ordens: int) -> list:
    """
    Gera uma massa de dados sintética para o teste de estresse.

    Os preços das ordens são gerados seguindo uma distribuição normal para forçar varreduras na lista.
    
    Nota: O uso de 'list' nativa aqui é permitido, pois este script 
    não faz parte das estruturas do projeto avaliadas no critério técnico.
    """
    ordens = []
    preco_base = 50.0  # Preço médio de referência do ativo
    timestamp_base = time.time()
    
    for i in range(quantidade_ordens):
        tipo = random.choice(['C', 'V'])
        
        # random.gauss gera uma curva normal com média 50 e desvio-padrão 2
        # Isso garante que haverá muitos matches e muita varredura no meio da lista
        preco = round(random.gauss(preco_base, 2.0), 2)
        
        # Quantidade em lotes (ex: 10, 20... 100)
        quantidade = random.randint(1, 10) * 10 
        
        # O timestamp cresce linearmente para manter a ordem cronológica
        timestamp = timestamp_base + i
        
        ordens.append({
            'id_ordem': i + 1,
            'tipo': tipo,
            'preco': preco,
            'quantidade': quantidade,
            'timestamp': timestamp
        })
        
    return ordens

def medir_tempo_processamento(motor, ordens: list):
    """
    Injeta a massa de ordens no motor e cronometra o tempo de execução.
    Estes dados serão exportados para gerar os gráficos empíricos no Jupyter Notebook.
    """

    # Carrega a fila de entrada primeiro. Não cronometramos isso porque a inserção na fila é O(1).
    for o in ordens:
        motor.receber_ordem(o['id_ordem'], o['tipo'], o['preco'], o['quantidade'], o['timestamp'])
        
    inicio_cronometro = time.perf_counter()
    
    # Executa o processamento e o casamento de ordens
    motor.processar_fila()
    
    fim_cronometro = time.perf_counter()
    
    return fim_cronometro - inicio_cronometro

def medir_tempo_insercao_isolada(ordens: list) -> float:
    """
    Isola a Lista Duplamente Encadeada para provar o custo O(n) de inserção.
    """
    livro_teste = ListaDuplamenteEncadeada()
    
    # Criamos os nós fora do cronômetro para medir apenas a lógica da estrutura
    nos_para_inserir = [No(o['id_ordem'], o['tipo'], o['preco'], o['quantidade'], o['timestamp']) for o in ordens]
    
    inicio_timer = time.perf_counter()
    
    for no in nos_para_inserir:
        # Simulamos a inserção no Livro de Compras (ordem decrescente escolhida arbitrariamente)
        livro_teste.inserir_ordenado(no, decrescente=True)
        
    fim_timer = time.perf_counter()
    
    return fim_timer - inicio_timer