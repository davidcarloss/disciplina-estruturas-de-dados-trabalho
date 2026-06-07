# main.py
from estruturas import No, Fila, Pilha, ListaDuplamenteEncadeada

class MotorDeNegociacao:
    """
    Motor de Negociação que gerencia as ordens e o casamento (match).
    Responsável: Pessoa 3
    """
    def __init__(self):
        self.fila_entrada = Fila() 
        self.pilha_desfazer = Pilha() # Sistema de Undo
        
        # Livros de ofertas independentes
        self.livro_compras = ListaDuplamenteEncadeada()
        self.livro_vendas = ListaDuplamenteEncadeada()

    def receber_ordem(self, id_ordem: int, tipo: str, preco: float, quantidade: int, timestamp: float):
        """
        Cria o nó da ordem e coloca na Fila de Entrada para aguardar processamento.
        """
        nova_ordem = No(id_ordem, tipo, preco, quantidade, timestamp)
        self.fila_entrada.enfileirar(nova_ordem)

    def processar_fila(self):
        """
        Loop principal que retira da fila_entrada e tenta executar o casamento (match).
        Se não der match ou sobrar quantidade, chama a inserção no livro.
        """
        while not self.fila_entrada.esta_vazia():
            ordem_atual = self.fila_entrada.desenfileirar()
            
            # 1. Tenta cruzar a ordem com o livro oposto
            self._tentar_casamento(ordem_atual)
            
            # 2. Se a ordem não foi totalmente executada, vai para o livro
            if ordem_atual.quantidade > 0:
                self._inserir_no_livro(ordem_atual)

    def _tentar_casamento(self, nova_ordem: No):
        """
        Lógica interna para comparar a nova ordem com o topo do livro oposto.
        Verifica se os preços cruzam e abate as quantidades.
        """
        if nova_ordem.tipo == 'C':
            livro_oposto = self.livro_vendas
            # Match: Preço de Compra >= Preço de Venda
            condicao_match = lambda o_nova, o_livro: o_nova.preco >= o_livro.preco
        else: # 'V'
            livro_oposto = self.livro_compras
            # Match: Preço de Venda <= Preço de Compra
            condicao_match = lambda o_nova, o_livro: o_nova.preco <= o_livro.preco

        atual = livro_oposto.obter_inicio()

        while atual is not None and nova_ordem.quantidade > 0:
            if condicao_match(nova_ordem, atual):
                # Calcula quanto da ordem pode ser executada
                qtd_negociada = min(nova_ordem.quantidade, atual.quantidade)
                
                # Abate as quantidades
                nova_ordem.quantidade -= qtd_negociada
                atual.quantidade -= qtd_negociada
                
                # Se a ordem do livro foi 100% executada (zerou), removemos ela
                if atual.quantidade == 0:
                    proximo_no = atual.proximo
                    livro_oposto.remover(atual)
                    atual = proximo_no
                else:
                    # O topo do livro ainda tem saldo, mas a nova ordem zerou, então encerramos
                    break 
            else:
                # Como o livro está ordenado, se não deu match com o topo (melhor preço), 
                # não dará com os próximos.
                break

    def _inserir_no_livro(self, ordem: No):
        """
        Insere a ordem na ListaDuplamenteEncadeada correspondente (Compra ou Venda)
        e salva o ID na pilha_desfazer.
        """
        if ordem.tipo == 'C':
            self.livro_compras.inserir_ordenado(ordem, decrescente=True)
        else:
            self.livro_vendas.inserir_ordenado(ordem, decrescente=False)
            
        # Registra a ação na pilha de Undo
        self.pilha_desfazer.empilhar(ordem.id_ordem)

    def desfazer_ultima_acao(self):
        """Puxa o último ID da pilha_desfazer e remove do livro correspondente."""
        id_alvo = self.pilha_desfazer.desempilhar()
        
        if id_alvo is None:
            return # Pilha vazia, nada a desfazer

        # Varre o livro de compras para encontrar e remover
        atual = self.livro_compras.obter_inicio()
        while atual is not None:
            if atual.id_ordem == id_alvo:
                self.livro_compras.remover(atual)
                return
            atual = atual.proximo

        # Se não estava em compras, varre o livro de vendas
        atual = self.livro_vendas.obter_inicio()
        while atual is not None:
            if atual.id_ordem == id_alvo:
                self.livro_vendas.remover(atual)
                return
            atual = atual.proximo


if __name__ == "__main__":
    # Testes básicos para validar a lógica
    motor = MotorDeNegociacao()
    print("Iniciando o simulador de Livro de Ofertas...")
    
    # Exemplo de teste:
    # 1. Chega uma ordem de Venda de 10 ações a R$ 40.0
    motor.receber_ordem(1, 'V', 40.0, 10, 1000.0)
    
    # 2. Chega uma ordem de Compra de 5 ações a R$ 41.0 (Cruza com a venda acima!)
    motor.receber_ordem(2, 'C', 41.0, 5, 1001.0)
    
    motor.processar_fila()
    
    topo_vendas = motor.livro_vendas.obter_inicio()
    if topo_vendas:
        print(f"Sobrou na Venda: ID {topo_vendas.id_ordem} com Qtd {topo_vendas.quantidade}")