from math import isfinite


# Busca linear manual. Melhor caso: O(1); pior caso: O(n).
def buscar_indice_carregador(carregadores, codigo):
    for indice in range(len(carregadores)):
        if carregadores[indice]["codigo"] == codigo:
            return indice
    return -1


# Busca linear manual para as ordens. Melhor: O(1); pior: O(n).
def buscar_indice_ordem(ordens, codigo):
    for indice in range(len(ordens)):
        if ordens[indice]["codigo"] == codigo:
            return indice
    return -1


# Mostra um carregador sem alterar a lista.
def exibir_carregador(carregador):
    print(f"\nCódigo: {carregador['codigo']}")
    print(f"Nome: {carregador['nome']}")
    print(f"Local: {carregador['local']}")
    print(f"Potência: {carregador['potencia_kw']:g} kW")


# Cadastra um carregador. Inserção no fim: O(1) amortizado.
def cadastrar_carregador(carregadores, codigo):
    print("\n===== CADASTRO DE CARREGADOR =====")
    nome = input("Nome: ").strip()
    local = input("Local de instalação: ").strip()

    if not nome or not local:
        print("Erro: nome e local são obrigatórios.")
        return False

    try:
        potencia = float(input("Potência em kW: ").strip().replace(",", "."))
    except ValueError:
        print("Erro: digite uma potência válida.")
        return False

    if not isfinite(potencia) or potencia <= 0:
        print("Erro: a potência deve ser positiva e finita.")
        return False

    carregadores.append({
        "codigo": codigo,
        "nome": nome,
        "local": local,
        "potencia_kw": potencia
    })
    print(f"Carregador cadastrado! Código: {codigo}")
    return True


# Percorre e mostra todos os carregadores. O(n).
def listar_carregadores(carregadores):
    print("\n===== CARREGADORES =====")
    if not carregadores:
        print("Nenhum carregador cadastrado.")
        return

    for carregador in carregadores:
        exibir_carregador(carregador)


# Consulta por código usando a busca manual.
def consultar_carregador(carregadores):
    print("\n===== CONSULTAR CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_carregador(carregadores, codigo)
    if indice == -1:
        print("Carregador não encontrado.")
        return
    exibir_carregador(carregadores[indice])


# Altera os campos, mantendo o valor quando ENTER é pressionado.
def alterar_carregador(carregadores):
    print("\n===== ALTERAR CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_carregador(carregadores, codigo)
    if indice == -1:
        print("Carregador não encontrado.")
        return

    carregador = carregadores[indice]
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
    print("Carregador alterado com sucesso!")


# Remove somente carregador sem ordem associada. O(n + m).
def remover_carregador(carregadores, ordens_servico):
    print("\n===== REMOVER CARREGADOR =====")
    try:
        codigo = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_carregador(carregadores, codigo)
    if indice == -1:
        print("Carregador não encontrado.")
        return

    for ordem in ordens_servico:
        if ordem["carregador_id"] == codigo:
            print("Não é possível remover: há uma ordem associada.")
            return

    exibir_carregador(carregadores[indice])
    if input("Confirmar remoção? (s/n): ").strip().lower() != "s":
        print("Remoção cancelada.")
        return

    carregadores.pop(indice)
    print("Carregador removido com sucesso!")


# Converte o número da prioridade em um texto mais claro.
def nome_prioridade(prioridade):
    if prioridade == 1:
        return "Crítica"
    if prioridade == 2:
        return "Alta"
    return "Normal"


# Mostra uma ordem e o carregador relacionado.
def exibir_ordem(ordem, carregadores):
    indice = buscar_indice_carregador(carregadores, ordem["carregador_id"])
    nome = "não encontrado"
    if indice != -1:
        nome = carregadores[indice]["nome"]

    print(f"\nCódigo da ordem: {ordem['codigo']}")
    print(f"Carregador: {ordem['carregador_id']} - {nome}")
    print(f"Descrição: {ordem['descricao']}")
    print(f"Prioridade: {nome_prioridade(ordem['prioridade'])}")
    print(f"Status: {ordem['status']}")


# Cadastra a ordem na lista e no fim da fila de prioridade.
def cadastrar_ordem(ordens_servico, carregadores, fila_prioridade, codigo):
    print("\n===== CADASTRO DE ORDEM =====")
    if not carregadores:
        print("Cadastre um carregador antes de criar uma ordem.")
        return False

    try:
        carregador_id = int(input("Código do carregador: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return False

    if buscar_indice_carregador(carregadores, carregador_id) == -1:
        print("Carregador não encontrado.")
        return False

    descricao = input("Descrição do serviço: ").strip()
    if not descricao:
        print("Erro: a descrição é obrigatória.")
        return False

    print("1 - Crítica | 2 - Alta | 3 - Normal")
    try:
        prioridade = int(input("Prioridade: ").strip())
    except ValueError:
        print("Erro: digite 1, 2 ou 3.")
        return False

    if prioridade < 1 or prioridade > 3:
        print("Erro: digite 1, 2 ou 3.")
        return False

    ordem = {
        "codigo": codigo,
        "carregador_id": carregador_id,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "pendente"
    }
    ordens_servico.append(ordem)
    fila_prioridade.append(ordem)
    print(f"Ordem cadastrada! Código: {codigo}")
    return True


# Percorre e mostra todas as ordens. O(n).
def listar_ordens(ordens_servico, carregadores):
    print("\n===== ORDENS DE SERVIÇO =====")
    if not ordens_servico:
        print("Nenhuma ordem cadastrada.")
        return

    for ordem in ordens_servico:
        exibir_ordem(ordem, carregadores)


# Consulta uma ordem pelo código com busca linear.
def consultar_ordem(ordens_servico, carregadores):
    print("\n===== CONSULTAR ORDEM =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_ordem(ordens_servico, codigo)
    if indice == -1:
        print("Ordem não encontrada.")
        return
    exibir_ordem(ordens_servico[indice], carregadores)


# Altera somente ordem pendente; a fila usa o mesmo dicionário.
def alterar_ordem(ordens_servico, carregadores):
    print("\n===== ALTERAR ORDEM PENDENTE =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_ordem(ordens_servico, codigo)
    if indice == -1:
        print("Ordem não encontrada.")
        return

    ordem = ordens_servico[indice]
    if ordem["status"] != "pendente":
        print("Não é permitido alterar uma ordem concluída.")
        return

    exibir_ordem(ordem, carregadores)
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
        if buscar_indice_carregador(carregadores, novo_carregador) == -1:
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

    ordem["descricao"] = descricao if descricao else ordem["descricao"]
    ordem["carregador_id"] = novo_carregador
    ordem["prioridade"] = nova_prioridade
    print("Ordem alterada com sucesso!")


# Remove uma ordem pendente tanto da lista quanto da fila.
def remover_ordem(ordens_servico, fila_prioridade, carregadores):
    print("\n===== REMOVER ORDEM PENDENTE =====")
    try:
        codigo = int(input("Código da ordem: ").strip())
    except ValueError:
        print("Erro: digite um código inteiro.")
        return

    indice = buscar_indice_ordem(ordens_servico, codigo)
    if indice == -1:
        print("Ordem não encontrada.")
        return

    ordem = ordens_servico[indice]
    if ordem["status"] != "pendente":
        print("Somente ordens pendentes podem ser removidas.")
        return

    exibir_ordem(ordem, carregadores)
    if input("Confirmar remoção? (s/n): ").strip().lower() != "s":
        print("Remoção cancelada.")
        return

    indice_fila = buscar_indice_ordem(fila_prioridade, codigo)
    if indice_fila != -1:
        fila_prioridade.pop(indice_fila)
    ordens_servico.pop(indice)
    print("Ordem removida da lista e da fila de prioridade!")


# Localiza a maior prioridade; empate mantém a ordem de chegada.
def indice_maior_prioridade(fila_prioridade):
    if not fila_prioridade:
        return -1

    melhor = 0
    for indice in range(1, len(fila_prioridade)):
        if fila_prioridade[indice]["prioridade"] < fila_prioridade[melhor]["prioridade"]:
            melhor = indice
    return melhor


# Atende a ordem mais prioritária e a empilha no histórico. O(n).
def atender_proxima_ordem(fila_prioridade, historico, carregadores):
    print("\n===== ATENDER PRÓXIMA ORDEM =====")
    indice = indice_maior_prioridade(fila_prioridade)
    if indice == -1:
        print("Não há ordens pendentes na fila.")
        return

    ordem = fila_prioridade.pop(indice)
    ordem["status"] = "concluida"
    historico.append(ordem)
    print("Ordem atendida e adicionada ao histórico:")
    exibir_ordem(ordem, carregadores)


# Desfaz somente o último atendimento, respeitando a pilha LIFO.
def desfazer_atendimento(fila_prioridade, historico, carregadores):
    print("\n===== DESFAZER ÚLTIMO ATENDIMENTO =====")
    if not historico:
        print("O histórico está vazio.")
        return

    ordem = historico.pop()
    ordem["status"] = "pendente"
    fila_prioridade.append(ordem)
    print("Atendimento desfeito; a ordem voltou para a fila:")
    exibir_ordem(ordem, carregadores)


# Filtra manualmente pelo status informado. O(n).
def filtrar_ordens_status(ordens_servico, carregadores):
    print("\n===== FILTRAR ORDENS =====")
    status = input("Status (pendente/concluida): ").strip().lower()
    if status != "pendente" and status != "concluida":
        print("Status inválido.")
        return

    encontrou = False
    for ordem in ordens_servico:
        if ordem["status"] == status:
            exibir_ordem(ordem, carregadores)
            encontrou = True

    if not encontrou:
        print(f"Nenhuma ordem com status '{status}'.")


# Exibe uma cópia da fila na sequência real de atendimento.
def mostrar_fila_prioridade(fila_prioridade, carregadores):
    print("\n===== FILA DE PRIORIDADE =====")
    if not fila_prioridade:
        print("A fila está vazia.")
        return

    copia = fila_prioridade.copy()
    posicao = 1
    while copia:
        indice = indice_maior_prioridade(copia)
        ordem = copia.pop(indice)
        print(f"\n--- Posição {posicao} ---")
        exibir_ordem(ordem, carregadores)
        posicao += 1


# Mostra a pilha do topo para a base, sem retirar elementos.
def mostrar_historico(historico, carregadores):
    print("\n===== HISTÓRICO (TOPO -> BASE) =====")
    if not historico:
        print("O histórico está vazio.")
        return

    for indice in range(len(historico) - 1, -1, -1):
        exibir_ordem(historico[indice], carregadores)


# Insertion Sort manual, em potência decrescente.
# Melhor caso: O(n); pior caso: O(n²); espaço: O(n) pela cópia.
def insertion_sort_carregadores(carregadores):
    ordenados = carregadores.copy()

    for indice in range(1, len(ordenados)):
        atual = ordenados[indice]
        anterior = indice - 1

        while anterior >= 0 and ordenados[anterior]["potencia_kw"] < atual["potencia_kw"]:
            ordenados[anterior + 1] = ordenados[anterior]
            anterior -= 1

        ordenados[anterior + 1] = atual

    return ordenados


# Relatório que aplica o Insertion Sort implementado acima.
def listar_carregadores_por_potencia(carregadores):
    print("\n===== CARREGADORES POR POTÊNCIA (MAIOR -> MENOR) =====")
    if not carregadores:
        print("Nenhum carregador cadastrado.")
        return

    ordenados = insertion_sort_carregadores(carregadores)
    for carregador in ordenados:
        exibir_carregador(carregador)


# Reúne os cinco relatórios exigidos no enunciado.
def menu_relatorios(carregadores, ordens_servico, fila_prioridade, historico):
    while True:
        print("\n===== RELATÓRIOS =====")
        print("1 - Listar carregadores")
        print("2 - Listar ordens")
        print("3 - Filtrar ordens por status")
        print("4 - Mostrar fila de prioridade")
        print("5 - Mostrar histórico da pilha")
        print("6 - Carregadores ordenados por potência")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar_carregadores(carregadores)
        elif opcao == "2":
            listar_ordens(ordens_servico, carregadores)
        elif opcao == "3":
            filtrar_ordens_status(ordens_servico, carregadores)
        elif opcao == "4":
            mostrar_fila_prioridade(fila_prioridade, carregadores)
        elif opcao == "5":
            mostrar_historico(historico, carregadores)
        elif opcao == "6":
            listar_carregadores_por_potencia(carregadores)
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


# Menu principal e estruturas mantidas durante a execução.
def main():
    carregadores = []
    ordens_servico = []
    fila_prioridade = []
    historico = []
    proximo_codigo_carregador = 1
    proximo_codigo_ordem = 1

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
            print(f"\nCarregadores: {len(carregadores)}")
            print(f"Ordens: {len(ordens_servico)}")
            print(f"Fila: {len(fila_prioridade)}")
            print(f"Histórico: {len(historico)}")
        elif opcao == "2":
            if cadastrar_carregador(carregadores, proximo_codigo_carregador):
                proximo_codigo_carregador += 1
        elif opcao == "3":
            consultar_carregador(carregadores)
        elif opcao == "4":
            alterar_carregador(carregadores)
        elif opcao == "5":
            remover_carregador(carregadores, ordens_servico)
        elif opcao == "6":
            if cadastrar_ordem(
                ordens_servico, carregadores, fila_prioridade,
                proximo_codigo_ordem
            ):
                proximo_codigo_ordem += 1
        elif opcao == "7":
            consultar_ordem(ordens_servico, carregadores)
        elif opcao == "8":
            alterar_ordem(ordens_servico, carregadores)
        elif opcao == "9":
            remover_ordem(ordens_servico, fila_prioridade, carregadores)
        elif opcao == "10":
            atender_proxima_ordem(fila_prioridade, historico, carregadores)
        elif opcao == "11":
            desfazer_atendimento(fila_prioridade, historico, carregadores)
        elif opcao == "12":
            menu_relatorios(
                carregadores, ordens_servico, fila_prioridade, historico
            )
        elif opcao == "0":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
