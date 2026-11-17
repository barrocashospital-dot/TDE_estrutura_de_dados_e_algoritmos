from math import isfinite


# ======================================================================
# ESTRUTURAS DE DADOS (implementadas manualmente)
# ======================================================================

class NoAVL:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esq = None
        self.dir = None
        self.altura = 1


def _altura(no):
    return no.altura if no is not None else 0


def _atualizar(no):
    ae = _altura(no.esq)
    ad = _altura(no.dir)
    no.altura = (ae if ae > ad else ad) + 1


def _fator(no):
    return _altura(no.esq) - _altura(no.dir)


def _rotacao_direita(y):
    x = y.esq
    y.esq = x.dir
    x.dir = y
    _atualizar(y)
    _atualizar(x)
    return x


def _rotacao_esquerda(x):
    y = x.dir
    x.dir = y.esq
    y.esq = x
    _atualizar(x)
    _atualizar(y)
    return y


# Restaura o equilíbrio do nó (fator entre -1 e 1). O(1).
def _balancear(no):
    _atualizar(no)
    fator = _fator(no)
    if fator > 1:
        if _fator(no.esq) < 0:
            no.esq = _rotacao_esquerda(no.esq)
        return _rotacao_direita(no)
    if fator < -1:
        if _fator(no.dir) > 0:
            no.dir = _rotacao_direita(no.dir)
        return _rotacao_esquerda(no)
    return no


# Árvore AVL (balanceada) com chaves únicas e comparáveis.
# Inserir, remover e buscar: O(log n) no pior caso, pois a altura
# nunca passa de ~1,44·log2(n). Percursos: O(n).
# A recursão tem profundidade O(log n), então não há risco de estouro.
class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0

    def inserir(self, chave, valor):
        self.raiz = self._inserir(self.raiz, chave, valor)

    def _inserir(self, no, chave, valor):
        if no is None:
            self.tamanho += 1
            return NoAVL(chave, valor)
        if chave < no.chave:
            no.esq = self._inserir(no.esq, chave, valor)
        elif chave > no.chave:
            no.dir = self._inserir(no.dir, chave, valor)
        else:
            no.valor = valor
            return no
        return _balancear(no)

    def remover(self, chave):
        tamanho_antes = self.tamanho
        self.raiz = self._remover(self.raiz, chave)
        return self.tamanho < tamanho_antes

    def _remover(self, no, chave):
        if no is None:
            return None
        if chave < no.chave:
            no.esq = self._remover(no.esq, chave)
        elif chave > no.chave:
            no.dir = self._remover(no.dir, chave)
        else:
            if no.esq is None or no.dir is None:
                self.tamanho -= 1
                return no.esq if no.esq is not None else no.dir
            sucessor = no.dir
            while sucessor.esq is not None:
                sucessor = sucessor.esq
            no.chave = sucessor.chave
            no.valor = sucessor.valor
            no.dir = self._remover(no.dir, sucessor.chave)
        return _balancear(no)

    # Busca binária na árvore (iterativa). O(log n).
    def buscar(self, chave, padrao=None):
        no = self.raiz
        while no is not None:
            if chave == no.chave:
                return no.valor
            no = no.esq if chave < no.chave else no.dir
        return padrao

    # Menor chave = nó mais à esquerda. O(log n).
    def minimo(self):
        no = self.raiz
        if no is None:
            return None
        while no.esq is not None:
            no = no.esq
        return no.valor

    def altura(self):
        return _altura(self.raiz)

    # Esquerda, raiz, direita: valores em ordem crescente de chave. O(n).
    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, saida):
        if no is None:
            return
        self._em_ordem(no.esq, saida)
        saida.append(no.valor)
        self._em_ordem(no.dir, saida)

    # Raiz, esquerda, direita: mostra a estrutura da árvore. O(n).
    def pre_ordem(self):
        resultado = []
        self._pre_ordem(self.raiz, resultado)
        return resultado

    def _pre_ordem(self, no, saida):
        if no is None:
            return
        saida.append(no.valor)
        self._pre_ordem(no.esq, saida)
        self._pre_ordem(no.dir, saida)

    # Esquerda, direita, raiz: filhos antes dos pais. O(n).
    def pos_ordem(self):
        resultado = []
        self._pos_ordem(self.raiz, resultado)
        return resultado

    def _pos_ordem(self, no, saida):
        if no is None:
            return
        self._pos_ordem(no.esq, saida)
        self._pos_ordem(no.dir, saida)
        saida.append(no.valor)

    # Verifica as invariantes (ordem das chaves, alturas e fator de
    # balanceamento). Usada nos testes. Devolve a altura ou levanta erro.
    def validar(self):
        return self._validar(self.raiz, None, None)

    def _validar(self, no, minimo, maximo):
        if no is None:
            return 0
        if minimo is not None and not no.chave > minimo:
            raise AssertionError("chave fora da ordem (esquerda)")
        if maximo is not None and not no.chave < maximo:
            raise AssertionError("chave fora da ordem (direita)")
        ae = self._validar(no.esq, minimo, no.chave)
        ad = self._validar(no.dir, no.chave, maximo)
        if abs(ae - ad) > 1:
            raise AssertionError("árvore desbalanceada")
        if no.altura != max(ae, ad) + 1:
            raise AssertionError("altura armazenada incorreta")
        return no.altura


# Merge Sort (divisão e conquista), estável. Ordena em potência decrescente;
# empate mantém a ordem original (por código). O(n log n) em todos os
# casos; espaço extra O(n).
def merge_sort_carregadores(carregadores):
    if len(carregadores) <= 1:
        return list(carregadores)
    meio = len(carregadores) // 2
    esquerda = merge_sort_carregadores(carregadores[:meio])
    direita = merge_sort_carregadores(carregadores[meio:])
    return _mesclar(esquerda, direita)


def _mesclar(esquerda, direita):
    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        # <= na comparação inversa garante estabilidade.
        if esquerda[i]["potencia_kw"] >= direita[j]["potencia_kw"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado


# Agrupa as estruturas do ERP:
#  - carregadores / ordens_servico: AVL com chave = código (armazenamento
#    principal, busca O(log n));
#  - fila_prioridade: AVL com chave (prioridade, sequência de entrada);
#  - historico: pilha (lista com append/pop no fim);
#  - cache_potencia: relatório por potência já ordenado (otimização extra),
#    invalidado quando um carregador é cadastrado, alterado ou removido.
class Dados:
    def __init__(self):
        self.carregadores = ArvoreAVL()
        self.ordens_servico = ArvoreAVL()
        self.fila_prioridade = ArvoreAVL()
        self.historico = []
        self.cache_potencia = None
        self.proximo_codigo_carregador = 1
        self.proximo_codigo_ordem = 1
        self.proxima_sequencia_fila = 1


# ======================================================================
# OPERAÇÕES (lógica sem entrada/saída, reutilizada pelo menu e pelos testes)
# ======================================================================

def chave_fila(ordem):
    return (ordem["prioridade"], ordem["sequencia_fila"])


def enfileirar(dados, ordem):
    ordem["sequencia_fila"] = dados.proxima_sequencia_fila
    dados.proxima_sequencia_fila += 1
    dados.fila_prioridade.inserir(chave_fila(ordem), ordem)


def buscar_carregador(dados, codigo):
    return dados.carregadores.buscar(codigo)


def buscar_ordem(dados, codigo):
    return dados.ordens_servico.buscar(codigo)


def criar_carregador(dados, nome, local, potencia):
    codigo = dados.proximo_codigo_carregador
    carregador = {
        "codigo": codigo,
        "nome": nome,
        "local": local,
        "potencia_kw": potencia,
        "qtd_ordens": 0
    }
    dados.carregadores.inserir(codigo, carregador)
    dados.cache_potencia = None
    dados.proximo_codigo_carregador += 1
    return carregador


def criar_ordem(dados, carregador_id, descricao, prioridade):
    carregador = buscar_carregador(dados, carregador_id)
    codigo = dados.proximo_codigo_ordem
    ordem = {
        "codigo": codigo,
        "carregador_id": carregador_id,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "pendente"
    }
    dados.ordens_servico.inserir(codigo, ordem)
    carregador["qtd_ordens"] += 1
    enfileirar(dados, ordem)
    dados.proximo_codigo_ordem += 1
    return ordem


def atender_proxima(dados):
    ordem = dados.fila_prioridade.minimo()
    if ordem is None:
        return None
    dados.fila_prioridade.remover(chave_fila(ordem))
    ordem["status"] = "concluida"
    dados.historico.append(ordem)
    return ordem


def desfazer_ultimo(dados):
    if not dados.historico:
        return None
    ordem = dados.historico.pop()
    ordem["status"] = "pendente"
    enfileirar(dados, ordem)
    return ordem


# Relatório por potência: percurso em ordem (por código) + Merge Sort.
# O(n log n) na primeira chamada; O(1) enquanto o cache for válido.
def carregadores_por_potencia(dados):
    if dados.cache_potencia is None:
        dados.cache_potencia = merge_sort_carregadores(
            dados.carregadores.em_ordem()
        )
    return dados.cache_potencia


# ======================================================================
# INTERFACE (menu no terminal)
# ======================================================================

def exibir_carregador(carregador):
    print(f"\nCódigo: {carregador['codigo']}")
    print(f"Nome: {carregador['nome']}")
    print(f"Local: {carregador['local']}")
    print(f"Potência: {carregador['potencia_kw']:g} kW")


def cadastrar_carregador(dados):
    print("\n===== CADASTRO DE CARREGADOR =====")
    nome = input("Nome: ").strip()
    local = input("Local de instalação: ").strip()

    if not nome or not local:
        print("Erro: nome e local são obrigatórios.")
        return

    try:
        potencia = float(input("Potência em kW: ").strip().replace(",", "."))
    except ValueError:
        print("Erro: digite uma potência válida.")
        return

    if not isfinite(potencia) or potencia <= 0:
        print("Erro: a potência deve ser positiva e finita.")
        return

    carregador = criar_carregador(dados, nome, local, potencia)
    print(f"Carregador cadastrado! Código: {carregador['codigo']}")


# Lista os carregadores em ordem de código (percurso em ordem). O(n).
def listar_carregadores(dados):
    print("\n===== CARREGADORES =====")
    if dados.carregadores.tamanho == 0:
        print("Nenhum carregador cadastrado.")
        return

    for carregador in dados.carregadores.em_ordem():
        exibir_carregador(carregador)


# Mesma listagem usando pré-ordem ou pós-ordem (mostra a forma da árvore).
def listar_carregadores_percurso(dados, nome_percurso):
    print(f"\n===== CARREGADORES ({nome_percurso.upper()}) =====")
    if dados.carregadores.tamanho == 0:
        print("Nenhum carregador cadastrado.")
        return

    if nome_percurso == "pré-ordem":
        carregadores = dados.carregadores.pre_ordem()
    else:
        carregadores = dados.carregadores.pos_ordem()
    for carregador in carregadores:
        exibir_carregador(carregador)
    print(f"\nAltura da árvore: {dados.carregadores.altura()}")


def consultar_carregador(dados):
    print("\n===== CONSULTAR CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    carregador = buscar_carregador(dados, codigo)
    if carregador is None:
        print("Carregador não encontrado.")
        return
    exibir_carregador(carregador)


def alterar_carregador(dados):
    print("\n===== ALTERAR CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    carregador = buscar_carregador(dados, codigo)
    if carregador is None:
        print("Carregador não encontrado.")
        return

    exibir_carregador(carregador)
    print("\nPressione ENTER para manter o valor atual.")
    nome = input("Novo nome: ").strip()
    local = input("Novo local: ").strip()
    entrada_potencia = input("Nova potência em kW: ").strip()

    nova_potencia = carregador["potencia_kw"]
    if entrada_potencia:
        try:
            nova_potencia = float(entrada_potencia.replace(",", "."))
        except ValueError:
            print("Erro: potência inválida. Nada foi alterado.")
            return
        if not isfinite(nova_potencia) or nova_potencia <= 0:
            print("Erro: a potência deve ser positiva e finita.")
            return

    carregador["nome"] = nome if nome else carregador["nome"]
    carregador["local"] = local if local else carregador["local"]
    carregador["potencia_kw"] = nova_potencia
    dados.cache_potencia = None
    print("Carregador alterado com sucesso!")


# A verificação "há ordens associadas?" é O(1) com o contador do carregador
# (antes: percorrer todas as ordens, O(m)); a remoção na árvore é O(log n).
def remover_carregador(dados):
    print("\n===== REMOVER CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    carregador = buscar_carregador(dados, codigo)
    if carregador is None:
        print("Carregador não encontrado.")
        return

    if carregador["qtd_ordens"] > 0:
        print("Não é possível remover: há uma ordem associada.")
        return

    exibir_carregador(carregador)
    if input("Confirmar remoção? (s/n): ").strip().lower() != "s":
        print("Remoção cancelada.")
        return

    dados.carregadores.remover(codigo)
    dados.cache_potencia = None
    print("Carregador removido com sucesso!")


def nome_prioridade(prioridade):
    if prioridade == 1:
        return "Crítica"
    if prioridade == 2:
        return "Alta"
    return "Normal"


def exibir_ordem(ordem, dados):
    carregador = buscar_carregador(dados, ordem["carregador_id"])
    nome = "não encontrado"
    if carregador is not None:
        nome = carregador["nome"]

    print(f"\nCódigo da ordem: {ordem['codigo']}")
    print(f"Carregador: {ordem['carregador_id']} - {nome}")
    print(f"Descrição: {ordem['descricao']}")
    print(f"Prioridade: {nome_prioridade(ordem['prioridade'])}")
    print(f"Status: {ordem['status']}")


def cadastrar_ordem(dados):
    print("\n===== CADASTRO DE ORDEM =====")
    if dados.carregadores.tamanho == 0:
        print("Cadastre um carregador antes de criar uma ordem.")
        return

    try:
        carregador_id = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    if buscar_carregador(dados, carregador_id) is None:
        print("Carregador não encontrado.")
        return

    descricao = input("Descrição do serviço: ").strip()
    if not descricao:
        print("Erro: a descrição é obrigatória.")
        return

    print("1 - Crítica | 2 - Alta | 3 - Normal")
    try:
        prioridade = int(input("Prioridade: ").strip())
    except ValueError:
        print("Erro: digite 1, 2 ou 3.")
        return

    if prioridade < 1 or prioridade > 3:
        print("Erro: digite 1, 2 ou 3.")
        return

    ordem = criar_ordem(dados, carregador_id, descricao, prioridade)
    print(f"Ordem cadastrada! Código: {ordem['codigo']}")


def listar_ordens(dados):
    print("\n===== ORDENS DE SERVIÇO =====")
    if dados.ordens_servico.tamanho == 0:
        print("Nenhuma ordem cadastrada.")
        return

    for ordem in dados.ordens_servico.em_ordem():
        exibir_ordem(ordem, dados)


def consultar_ordem(dados):
    print("\n===== CONSULTAR ORDEM =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    ordem = buscar_ordem(dados, codigo)
    if ordem is None:
        print("Ordem não encontrada.")
        return
    exibir_ordem(ordem, dados)


# A prioridade faz parte da chave da fila: remove e reinsere o nó,
# mantendo a sequência de chegada. O(log n).
def alterar_ordem(dados):
    print("\n===== ALTERAR ORDEM PENDENTE =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    ordem = buscar_ordem(dados, codigo)
    if ordem is None:
        print("Ordem não encontrada.")
        return

    if ordem["status"] != "pendente":
        print("Não é permitido alterar uma ordem concluída.")
        return

    exibir_ordem(ordem, dados)
    print("\nPressione ENTER para manter o valor atual.")
    descricao = input("Nova descrição: ").strip()
    entrada_carregador = input("Novo código do carregador: ").strip()
    entrada_prioridade = input("Nova prioridade (1, 2 ou 3): ").strip()

    novo_carregador = ordem["carregador_id"]
    if entrada_carregador:
        try:
            novo_carregador = int(entrada_carregador)
        except ValueError:
            print("Erro: código de carregador inválido. Nada foi alterado.")
            return
        if buscar_carregador(dados, novo_carregador) is None:
            print("Erro: carregador não encontrado. Nada foi alterado.")
            return

    nova_prioridade = ordem["prioridade"]
    if entrada_prioridade:
        try:
            nova_prioridade = int(entrada_prioridade)
        except ValueError:
            print("Erro: prioridade inválida. Nada foi alterado.")
            return
        if nova_prioridade < 1 or nova_prioridade > 3:
            print("Erro: a prioridade deve ser 1, 2 ou 3.")
            return

    antigo = ordem["carregador_id"]
    if novo_carregador != antigo:
        buscar_carregador(dados, antigo)["qtd_ordens"] -= 1
        buscar_carregador(dados, novo_carregador)["qtd_ordens"] += 1

    dados.fila_prioridade.remover(chave_fila(ordem))
    ordem["descricao"] = descricao if descricao else ordem["descricao"]
    ordem["carregador_id"] = novo_carregador
    ordem["prioridade"] = nova_prioridade
    dados.fila_prioridade.inserir(chave_fila(ordem), ordem)
    print("Ordem alterada com sucesso!")


def remover_ordem(dados):
    print("\n===== REMOVER ORDEM PENDENTE =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    ordem = buscar_ordem(dados, codigo)
    if ordem is None:
        print("Ordem não encontrada.")
        return

    if ordem["status"] != "pendente":
        print("Somente ordens pendentes podem ser removidas.")
        return

    exibir_ordem(ordem, dados)
    if input("Confirmar remoção? (s/n): ").strip().lower() != "s":
        print("Remoção cancelada.")
        return

    dados.fila_prioridade.remover(chave_fila(ordem))
    dados.ordens_servico.remover(codigo)
    buscar_carregador(dados, ordem["carregador_id"])["qtd_ordens"] -= 1
    print("Ordem removida da lista e da fila de prioridade!")


def atender_proxima_ordem(dados):
    print("\n===== ATENDER PRÓXIMA ORDEM =====")
    ordem = atender_proxima(dados)
    if ordem is None:
        print("Não há ordens pendentes na fila.")
        return
    print("Ordem atendida e adicionada ao histórico:")
    exibir_ordem(ordem, dados)


def desfazer_atendimento(dados):
    print("\n===== DESFAZER ÚLTIMO ATENDIMENTO =====")
    ordem = desfazer_ultimo(dados)
    if ordem is None:
        print("O histórico está vazio.")
        return
    print("Atendimento desfeito; a ordem voltou para a fila:")
    exibir_ordem(ordem, dados)


def filtrar_ordens_status(dados):
    print("\n===== FILTRAR ORDENS =====")
    status = input("Status (pendente/concluida): ").strip().lower()
    if status != "pendente" and status != "concluida":
        print("Status inválido.")
        return

    encontrou = False
    for ordem in dados.ordens_servico.em_ordem():
        if ordem["status"] == status:
            exibir_ordem(ordem, dados)
            encontrou = True

    if not encontrou:
        print(f"Nenhuma ordem com status '{status}'.")


# Percurso em ordem da fila: já sai na sequência de atendimento. O(n).
def mostrar_fila_prioridade(dados):
    print("\n===== FILA DE PRIORIDADE =====")
    if dados.fila_prioridade.tamanho == 0:
        print("A fila está vazia.")
        return

    posicao = 1
    for ordem in dados.fila_prioridade.em_ordem():
        print(f"\n--- Posição {posicao} ---")
        exibir_ordem(ordem, dados)
        posicao += 1


def mostrar_historico(dados):
    print("\n===== HISTÓRICO (TOPO -> BASE) =====")
    if not dados.historico:
        print("O histórico está vazio.")
        return

    for indice in range(len(dados.historico) - 1, -1, -1):
        exibir_ordem(dados.historico[indice], dados)


def listar_carregadores_por_potencia(dados):
    print("\n===== CARREGADORES POR POTÊNCIA (MAIOR -> MENOR) =====")
    if dados.carregadores.tamanho == 0:
        print("Nenhum carregador cadastrado.")
        return

    for carregador in carregadores_por_potencia(dados):
        exibir_carregador(carregador)


def menu_relatorios(dados):
    while True:
        print("\n===== RELATÓRIOS =====")
        print("1 - Listar carregadores (em ordem)")
        print("2 - Listar ordens (em ordem)")
        print("3 - Filtrar ordens por status")
        print("4 - Mostrar fila de prioridade")
        print("5 - Mostrar histórico da pilha")
        print("6 - Carregadores ordenados por potência")
        print("7 - Carregadores em pré-ordem")
        print("8 - Carregadores em pós-ordem")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar_carregadores(dados)
        elif opcao == "2":
            listar_ordens(dados)
        elif opcao == "3":
            filtrar_ordens_status(dados)
        elif opcao == "4":
            mostrar_fila_prioridade(dados)
        elif opcao == "5":
            mostrar_historico(dados)
        elif opcao == "6":
            listar_carregadores_por_potencia(dados)
        elif opcao == "7":
            listar_carregadores_percurso(dados, "pré-ordem")
        elif opcao == "8":
            listar_carregadores_percurso(dados, "pós-ordem")
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


def main():
    dados = Dados()

    while True:
        print("\n===== ERP DE CARREGADORES =====")
        print("1 - Quantidade de registros")
        print("2 - Cadastrar carregador")
        print("3 - Consultar carregador")
        print("4 - Alterar carregador")
        print("5 - Remover carregador")
        print("6 - Cadastrar ordem")
        print("7 - Consultar ordem")
        print("8 - Alterar ordem pendente")
        print("9 - Remover ordem pendente")
        print("10 - Atender próxima ordem")
        print("11 - Desfazer último atendimento")
        print("12 - Relatórios")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            print(f"\nCarregadores: {dados.carregadores.tamanho}")
            print(f"Ordens: {dados.ordens_servico.tamanho}")
            print(f"Fila: {dados.fila_prioridade.tamanho}")
            print(f"Histórico: {len(dados.historico)}")
        elif opcao == "2":
            cadastrar_carregador(dados)
        elif opcao == "3":
            consultar_carregador(dados)
        elif opcao == "4":
            alterar_carregador(dados)
        elif opcao == "5":
            remover_carregador(dados)
        elif opcao == "6":
            cadastrar_ordem(dados)
        elif opcao == "7":
            consultar_ordem(dados)
        elif opcao == "8":
            alterar_ordem(dados)
        elif opcao == "9":
            remover_ordem(dados)
        elif opcao == "10":
            atender_proxima_ordem(dados)
        elif opcao == "11":
            desfazer_atendimento(dados)
        elif opcao == "12":
            menu_relatorios(dados)
        elif opcao == "0":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
