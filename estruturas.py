# estruturas.py

class No:
    """
    Representa uma ordem e atua como o nó base para as estruturas encadeadas.
    Responsável: Pessoa 1
    """
    def __init__(self, id_ordem: int, tipo: str, preco: float, quantidade: int, timestamp: float):
        self.id_ordem = id_ordem
        self.tipo = tipo  # 'C' para Compra, 'V' para Venda
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp
        
        # Ponteiros para navegação nas estruturas (next / prev)
        self.proximo = None
        self.anterior = None


class Fila:
    """
    Fila de Entrada (FIFO) - Complexidade O(1)
    Responsável: Pessoa 1
    """
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, no: No):
        """Insere uma nova ordem no final da fila (enqueue)."""
        pass

    def desenfileirar(self) -> No:
        """Remove e retorna a ordem do início da fila (dequeue)."""
        pass

    def esta_vazia(self) -> bool:
        """Verifica se a fila está vazia."""
        pass


class Pilha:
    """
    Sistema de Undo (LIFO) - Complexidade O(1)
    Responsável: Pessoa 1
    """
    def __init__(self):
        self.topo = None

    def empilhar(self, id_ordem: int):
        """Armazena o ID de uma ordem recém-inserida (push)."""
        pass

    def desempilhar(self) -> int:
        """Remove e retorna o último ID inserido (pop)."""
        pass
        
    def esta_vazia(self) -> bool:
        """Verifica se a pilha está vazia."""
        pass


class ListaDuplamenteEncadeada:
    """
    Lista Duplamente Encadeada para o Livro de Ofertas.
    Responsável: Pessoa 2
    """
    def __init__(self):
        self.inicio = None
        self.fim = None

    def inserir_ordenado(self, no: No, decrescente: bool):
        """
        Insere o nó na posição correta varrendo a lista - Complexidade O(n).
        Se decrescente=True, insere do maior para o menor preço (Lista de Compras).
        Se decrescente=False, insere do menor para o maior preço (Lista de Vendas).
        """
        pass

    def remover(self, no: No):
        """
        Remove um nó específico (usado quando a ordem é 100% executada) 
        religando os ponteiros (proximo/anterior) corretamente.
        """
        pass

    def obter_inicio(self) -> No:
        """Retorna a ordem no topo do livro (melhor preço de compra ou venda)."""
        pass