"""Testes de corretude e benchmark: Parte 1 (listas) x Parte 2 (AVL).

Uso (a partir da raiz do projeto):  python parte2/benchmark.py
"""
import gc
import os
import random
import statistics
import sys
import time

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "..", "parte1"))

import TDE_parte1 as p1  # noqa: E402
import TDE_parte2 as p2  # noqa: E402

SEMENTE = 42
TAMANHOS = [500, 1000, 2000, 4000, 8000]
REPETICOES = 5


# ----------------------------------------------------------------------
# Testes de corretude
# ----------------------------------------------------------------------
def testar():
    rnd = random.Random(SEMENTE)

    # AVL: invariantes após inserções/remoções aleatórias + percursos.
    arv = p2.ArvoreAVL()
    ref = {}
    for _ in range(5000):
        k = rnd.randint(0, 800)
        if rnd.random() < 0.6:
            arv.inserir(k, k * 2)
            ref[k] = k * 2
        else:
            assert arv.remover(k) == (k in ref)
            ref.pop(k, None)
        assert arv.tamanho == len(ref)
    arv.validar()
    assert arv.em_ordem() == [ref[k] for k in sorted(ref)]
    assert sorted(arv.pre_ordem()) == sorted(arv.pos_ordem()) == arv.em_ordem()
    for k in range(-5, 810):
        assert arv.buscar(k) == ref.get(k)

    # Inserção sequencial (pior caso da BST) mantém altura logarítmica.
    seq = p2.ArvoreAVL()
    for k in range(1, 4096):
        seq.inserir(k, k)
    seq.validar()
    assert seq.altura() <= 13, seq.altura()

    # Pré-ordem / pós-ordem em árvore conhecida.
    pequena = p2.ArvoreAVL()
    for k in [2, 1, 3]:
        pequena.inserir(k, k)
    assert pequena.pre_ordem() == [2, 1, 3]
    assert pequena.pos_ordem() == [1, 3, 2]
    assert pequena.em_ordem() == [1, 2, 3]

    # Merge sort: igual ao sorted estável por potência decrescente.
    lista = [{"codigo": i, "potencia_kw": rnd.choice([7, 11, 22, 50, 150])}
             for i in range(3000)]
    esperado = sorted(lista, key=lambda c: -c["potencia_kw"])
    assert p2.merge_sort_carregadores(lista) == esperado
    assert p2.merge_sort_carregadores([]) == []

    # Fila: a Parte 2 atende na mesma ordem que a Parte 1 (simulação).
    d2 = p2.Dados()
    for i in range(20):
        p2.criar_carregador(d2, f"c{i}", "x", 10.0 + i)
    fila1, hist1, codigo = [], [], 1
    for _ in range(4000):
        r = rnd.random()
        if r < 0.5:
            prio = rnd.randint(1, 3)
            o2 = p2.criar_ordem(d2, rnd.randint(1, 20), "d", prio)
            fila1.append({"codigo": o2["codigo"], "prioridade": prio,
                          "status": "pendente"})
        elif r < 0.85:
            o2 = p2.atender_proxima(d2)
            i1 = p1.indice_maior_prioridade(fila1)
            if i1 == -1:
                assert o2 is None
            else:
                o1 = fila1.pop(i1)
                hist1.append(o1)
                assert o1["codigo"] == o2["codigo"]
        else:
            o2 = p2.desfazer_ultimo(d2)
            if not hist1:
                assert o2 is None
            else:
                o1 = hist1.pop()
                fila1.append(o1)
                assert o1["codigo"] == o2["codigo"]
    d2.fila_prioridade.validar()
    print("Testes de corretude: OK")


# ----------------------------------------------------------------------
# Medição
# ----------------------------------------------------------------------
def medir(funcao_preparo, funcao_medida):
    """Mediana (ms) de REPETICOES execuções; o preparo não entra no tempo."""
    tempos = []
    for _ in range(REPETICOES):
        estado = funcao_preparo()
        gc.collect()
        gc.disable()
        t0 = time.perf_counter()
        funcao_medida(estado)
        t1 = time.perf_counter()
        gc.enable()
        tempos.append((t1 - t0) * 1000)
    return statistics.median(tempos)


def potencias_aleatorias(n, rnd):
    return [round(rnd.uniform(3.7, 350.0), 1) for _ in range(n)]


def montar_v1_carregadores(n, rnd):
    return [{"codigo": i, "nome": "n", "local": "l", "potencia_kw": p}
            for i, p in enumerate(potencias_aleatorias(n, rnd), start=1)]


def montar_v2_dados(n, rnd):
    dados = p2.Dados()
    for p in potencias_aleatorias(n, rnd):
        p2.criar_carregador(dados, "n", "l", p)
    return dados


def cenario_busca(n):
    """1000 buscas por código (metade existentes, metade ausentes)."""
    rnd = random.Random(SEMENTE)
    codigos = [rnd.randint(1, n) if i % 2 == 0 else n + rnd.randint(1, n)
               for i in range(1000)]
    lista = montar_v1_carregadores(n, random.Random(SEMENTE))
    dados = montar_v2_dados(n, random.Random(SEMENTE))

    def v1(_):
        for c in codigos:
            p1.buscar_indice_carregador(lista, c)

    def v2(_):
        for c in codigos:
            p2.buscar_carregador(dados, c)

    return medir(lambda: None, v1), medir(lambda: None, v2)


def cenario_ordenacao(n, ordem):
    """Relatório por potência. ordem: aleatorio | crescente | decrescente."""
    rnd = random.Random(SEMENTE)
    potencias = potencias_aleatorias(n, rnd)
    if ordem == "crescente":
        potencias.sort()
    elif ordem == "decrescente":
        potencias.sort(reverse=True)
    lista = [{"codigo": i, "potencia_kw": p}
             for i, p in enumerate(potencias, start=1)]

    return (medir(lambda: None, lambda _: p1.insertion_sort_carregadores(lista)),
            medir(lambda: None, lambda _: p2.merge_sort_carregadores(lista)))


def cenario_atendimento(n):
    """Atende as n ordens pendentes (prioridades aleatórias)."""
    prioridades = [random.Random(SEMENTE).randint(1, 3) for _ in range(1)]
    rnd = random.Random(SEMENTE)
    prioridades = [rnd.randint(1, 3) for _ in range(n)]

    def prep_v1():
        return [{"codigo": i, "prioridade": p, "status": "pendente"}
                for i, p in enumerate(prioridades, start=1)]

    def med_v1(fila):
        while fila:
            fila.pop(p1.indice_maior_prioridade(fila))

    def prep_v2():
        dados = p2.Dados()
        p2.criar_carregador(dados, "n", "l", 11.0)
        for p in prioridades:
            p2.criar_ordem(dados, 1, "d", p)
        return dados

    def med_v2(dados):
        while p2.atender_proxima(dados) is not None:
            pass

    return medir(prep_v1, med_v1), medir(prep_v2, med_v2)


def cenario_insercao_ordens(n):
    """Cadastro de n ordens (inclui enfileirar). Custo de manter a árvore."""
    rnd = random.Random(SEMENTE)
    prioridades = [rnd.randint(1, 3) for _ in range(n)]

    def med_v1(_):
        ordens, fila = [], []
        for i, p in enumerate(prioridades, start=1):
            o = {"codigo": i, "carregador_id": 1, "prioridade": p,
                 "status": "pendente"}
            ordens.append(o)
            fila.append(o)

    def prep_v2():
        dados = p2.Dados()
        p2.criar_carregador(dados, "n", "l", 11.0)
        return dados

    def med_v2(dados):
        for p in prioridades:
            p2.criar_ordem(dados, 1, "d", p)

    return medir(lambda: None, med_v1), medir(prep_v2, med_v2)


def cenario_remocao_carregador(n):
    """Verificar se o carregador pode ser removido (há ordens associadas?).
    Pior caso: carregador sem ordens, com n ordens de outros carregadores."""
    ordens = [{"codigo": i, "carregador_id": 2} for i in range(1, n + 1)]
    dados = p2.Dados()
    p2.criar_carregador(dados, "a", "l", 1.0)
    p2.criar_carregador(dados, "b", "l", 2.0)
    for _ in range(n):
        p2.criar_ordem(dados, 2, "d", 3)

    def v1(_):
        for _ in range(200):
            for o in ordens:
                if o["carregador_id"] == 1:
                    break

    def v2(_):
        for _ in range(200):
            p2.buscar_carregador(dados, 1)["qtd_ordens"] > 0

    return medir(lambda: None, v1), medir(lambda: None, v2)


def altura_arvore(n):
    dados = p2.Dados()
    for _ in range(n):
        p2.criar_carregador(dados, "n", "l", 11.0)  # códigos sequenciais
    return dados.carregadores.altura()


def tabela(titulo, linhas, rotulo_v1="Parte 1 (ms)", rotulo_v2="Parte 2 (ms)"):
    print(f"\n### {titulo}")
    print(f"| n | {rotulo_v1} | {rotulo_v2} | Speedup |")
    print("|---:|---:|---:|---:|")
    for n, a, b in linhas:
        print(f"| {n} | {a:.3f} | {b:.3f} | {a / b:.2f}x |")


def main():
    testar()
    print("\nMediana de", REPETICOES, "execuções; semente", SEMENTE)

    tabela("Busca por código (1000 buscas)",
           [(n, *cenario_busca(n)) for n in TAMANHOS])
    for ordem in ("aleatorio", "crescente", "decrescente"):
        tabela(f"Ordenação por potência decrescente - entrada {ordem} "
               "(Insertion Sort x Merge Sort)",
               [(n, *cenario_ordenacao(n, ordem)) for n in TAMANHOS])
    tabela("Atender todas as ordens da fila",
           [(n, *cenario_atendimento(n)) for n in TAMANHOS])
    tabela("Cadastro de n ordens (custo de inserção)",
           [(n, *cenario_insercao_ordens(n)) for n in TAMANHOS])
    tabela("Checagem 'carregador tem ordens?' (200 consultas, pior caso)",
           [(n, *cenario_remocao_carregador(n)) for n in TAMANHOS])

    print("\n### Altura da AVL com chaves sequenciais")
    print("| n | altura AVL | ceil(log2(n+1)) |")
    print("|---:|---:|---:|")
    for n in TAMANHOS:
        print(f"| {n} | {altura_arvore(n)} | {(n + 1 - 1).bit_length()} |")


if __name__ == "__main__":
    main()
