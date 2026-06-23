class No:
    """
    Representa uma ordem e atua como o nó base para as estruturas encadeadas.
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
    """
    def __init__(self):
        self.inicio = None
        self.fim = None

    def esta_vazia(self) -> bool:
        """Verifica se a fila está vazia."""
        return self.inicio is None

    def enfileirar(self, no: No):
        """Insere uma nova ordem no final da fila (enqueue)."""
        # Garante que o nó inserido não tenha resíduos de ponteiros antigos
        no.proximo = None 
        no.anterior = None

        if self.esta_vazia():
            # Se a fila está vazia, o novo nó é o início e o fim
            self.inicio = no
            self.fim = no
        else:
            # Se não, adiciona ao final e atualiza o ponteiro de fim
            self.fim.proximo = no
            no.anterior = self.fim
            self.fim = no

    def desenfileirar(self) -> No:
        """Remove e retorna a ordem do início da fila (dequeue)."""
        if self.esta_vazia():
            return None
        
        no_removido = self.inicio
        self.inicio = self.inicio.proximo
        
        if self.inicio is None:
            # Se a fila esvaziou após a remoção, o fim também deve ser None
            self.fim = None
        else:
            # Remove a referência do novo início para o nó removido
            self.inicio.anterior = None
            
        # Isola completamente o nó removido para evitar problemas de referência
        no_removido.proximo = None
        no_removido.anterior = None
        
        return no_removido


class NoPilha:
    """
    Classe auxiliar para o funcionamento encadeado da Pilha de Undo.
    Armazena apenas o ID da ordem.
    """
    def __init__(self, id_ordem: int):
        self.id_ordem = id_ordem
        self.proximo = None


class Pilha:
    """
    Sistema de Undo (LIFO) - Complexidade O(1)
    """
    def __init__(self):
        self.topo = None

    def esta_vazia(self) -> bool:
        """Verifica se a pilha está vazia."""
        return self.topo is None

    def empilhar(self, id_ordem: int):
        """Armazena o ID de uma ordem recém-inserida (push)."""
        novo_no = NoPilha(id_ordem)
        
        # O próximo do novo nó aponta para o antigo topo
        novo_no.proximo = self.topo
        
        # O novo nó se torna o novo topo
        self.topo = novo_no

    def desempilhar(self) -> int:
        """Remove e retorna o último ID inserido (pop)."""
        if self.esta_vazia():
            return None
            
        id_removido = self.topo.id_ordem
        
        # O topo passa a ser o nó abaixo dele
        self.topo = self.topo.proximo
        
        return id_removido

class ListaDuplamenteEncadeada:
    """
    Lista Duplamente Encadeada para o Livro de Ofertas.
    """
    def __init__(self):
        self.inicio = None
        self.fim = None

    def obter_inicio(self) -> No:
        """Retorna a ordem no topo do livro (melhor preço de compra ou venda)."""
        return self.inicio

    def inserir_ordenado(self, no: No, decrescente: bool):
        """
        Insere o nó na posição correta varrendo a lista - Complexidade O(n).
        Se decrescente=True, insere do maior para o menor preço (Lista de Compras).
        Se decrescente=False, insere do menor para o maior preço (Lista de Vendas).
        """
        # Limpa qualquer lixo de memória nos ponteiros antes de inserir
        no.proximo = None
        no.anterior = None

        # Cenário 1: Lista Vazia
        if self.inicio is None:
            self.inicio = no
            self.fim = no
            return

        atual = self.inicio

        # Varredura com custo O(n) para achar a posição correta
        while atual is not None:
            if decrescente:
                # Livro de Compras: Procuramos o primeiro preço MENOR que o novo nó
                # Se o preço for IGUAL, o 'while' continua para garantir o FIFO (chegou depois, fica atrás)
                if no.preco > atual.preco:
                    break
            else:
                # Livro de Vendas: Procuramos o primeiro preço MAIOR que o novo nó
                if no.preco < atual.preco:
                    break
            
            atual = atual.proximo

        # Cenário 2: Inserção no Fim (varreu toda a lista e não parou no 'break')
        if atual is None:
            self.fim.proximo = no
            no.anterior = self.fim
            self.fim = no
            return

        # Cenário 3: Inserção no Início (parou no primeiro nó)
        if atual == self.inicio:
            no.proximo = self.inicio
            self.inicio.anterior = no
            self.inicio = no
            return

        # Cenário 4: Inserção no Meio (vai entrar antes do nó 'atual')
        # A ordem dessas 4 linhas é vital para não perdermos a referência de memória
        no.proximo = atual
        no.anterior = atual.anterior
        atual.anterior.proximo = no
        atual.anterior = no

    def remover(self, no: No):
        """
        Remove um nó específico (usado quando a ordem é 100% executada) 
        religando os ponteiros (proximo/anterior) corretamente.
        Complexidade: O(1) dado que já temos a referência do nó.
        """
        if no is None: 
            return

        # Ajuste do ponteiro da esquerda (anterior)
        if no.anterior is not None:
            # O vizinho da esquerda passa a apontar para o vizinho da direita
            no.anterior.proximo = no.proximo
        else:
            # Se não tem vizinho da esquerda, ele era o início da lista
            self.inicio = no.proximo

        # Ajuste do ponteiro da direita (proximo)
        if no.proximo is not None:
            # O vizinho da direita passa a apontar para o vizinho da esquerda
            no.proximo.anterior = no.anterior
        else:
            # Se não tem vizinho da direita, ele era o fim da lista
            self.fim = no.anterior

        # Isola o nó completamente garantindo que não haverá 'nós fantasmas'
        no.proximo = None
        no.anterior = None