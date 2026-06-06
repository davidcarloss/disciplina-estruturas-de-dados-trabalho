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
        pass

    def processar_fila(self):
        """
        Loop principal que retira da fila_entrada e tenta executar o casamento (match).
        Se não der match ou sobrar quantidade, chama a inserção no livro.
        """
        pass

    def _tentar_casamento(self, nova_ordem: No):
        """
        Lógica interna para comparar a nova ordem com o topo do livro oposto.
        Verifica se os preços cruzam e abate as quantidades.
        """
        pass

    def _inserir_no_livro(self, ordem: No):
        """
        Insere a ordem na ListaDuplamenteEncadeada correspondente (Compra ou Venda)
        e salva o ID na pilha_desfazer.
        """
        pass

    def desfazer_ultima_acao(self):
        """Puxa o último ID da pilha_desfazer e remove do livro correspondente."""
        pass

if __name__ == "__main__":
    # Testes manuais básicos para validar a lógica
    motor = MotorDeNegociacao()
    print("Iniciando o simulador de Livro de Ofertas...")
    # motor.receber_ordem(1, 'C', 40.0, 5, 1000.0)
    # motor.processar_fila()