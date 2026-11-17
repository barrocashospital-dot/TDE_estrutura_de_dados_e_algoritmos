# ERP de Carregadores Elétricos

Sistema em Python (terminal) para gerenciar carregadores elétricos e suas ordens de serviço: cadastro, consulta, alteração e remoção de registros, fila de atendimento por prioridade, histórico com desfazer e relatórios.

O projeto tem duas versões, mantidas lado a lado para comparar o desempenho:

| Versão | Arquivo | Estruturas principais |
|---|---|---|
| Parte 1 | [`parte1/TDE_parte1.py`](parte1/TDE_parte1.py) | Listas, busca linear, Insertion Sort |
| Parte 2 (otimizada) | [`parte2/TDE_parte2.py`](parte2/TDE_parte2.py) | Árvore AVL, percursos, busca na árvore, Merge Sort |

Só a biblioteca padrão do Python 3 é usada, e todas as estruturas e algoritmos são implementados manualmente.

## Como executar

```bash
python parte2/TDE_parte2.py   # versão otimizada
python parte1/TDE_parte1.py   # versão original
```

Cadastre um carregador (opção **2**), crie uma ordem (opção **6**), atenda a próxima (opção **10**) e veja os relatórios (opção **12**).

## Funcionalidades

- Cadastro, consulta, alteração e remoção de carregadores (nome, local, potência em kW);
- Cadastro, consulta, alteração e remoção de ordens de serviço pendentes;
- Prioridades: 1 (crítica), 2 (alta) e 3 (normal), com ordem de chegada no empate;
- Atendimento da próxima ordem e histórico em pilha, com desfazer do último atendimento;
- Relatórios: listagens, filtro por status, fila de prioridade, histórico e carregadores por potência;
- Validação das entradas. Um carregador com ordens associadas não pode ser removido.

## Parte 2: o que foi otimizado

- **Árvore AVL** (balanceada, manual) como armazenamento principal de carregadores, ordens e da fila de prioridade. Inserir, remover e buscar custam O(log n) no pior caso.
- **Travessias** em ordem (listagens ordenadas e fila), pré-ordem e pós-ordem (relatórios 7 e 8 mostram os carregadores e a altura da árvore).
- **Busca** binária manual sobre a árvore, por código.
- **Merge Sort** (divisão e conquista, estável) no relatório por potência: O(n log n), contra O(n²) do Insertion Sort.
- **Otimização extra:** cada carregador guarda a quantidade de ordens associadas (a checagem de remoção passa de O(m) para O(1)), e o relatório por potência fica em cache até que um carregador seja cadastrado, alterado ou removido.

### Complexidade

| Operação | Parte 1 | Parte 2 |
|---|---|---|
| Buscar por código | O(n) | O(log n) |
| Atender próxima ordem | O(n) | O(log n) |
| Mostrar a fila na ordem de atendimento | O(n²) | O(n) |
| Relatório por potência | O(n²) | O(n log n) (O(1) com cache) |
| Carregador tem ordens? | O(m) | O(1) |
| Cadastrar ordem | O(1) | O(log n) |

## Desempenho

O arquivo [`parte2/benchmark.py`](parte2/benchmark.py) roda testes de corretude (invariantes da AVL, percursos, Merge Sort contra `sorted` e equivalência da fila com a Parte 1) e compara as duas versões. Resultado completo em [`parte2/resultados_benchmark.md`](parte2/resultados_benchmark.md).

Com n = 8000 (mediana de 5 execuções):

| Operação | Parte 1 | Parte 2 |
|---|---:|---:|
| 1000 buscas por código | 247 ms | 0,6 ms |
| Ordenar por potência (entrada aleatória) | 1973 ms | 17 ms |
| Atender todas as ordens | 2416 ms | 43 ms |
| Checar "carregador tem ordens?" (200 consultas) | 64 ms | 0,04 ms |
| Cadastrar 8000 ordens | 2 ms | 123 ms |

A Parte 2 perde no cadastro, porque a AVL paga o balanceamento a cada inserção, e na ordenação de uma entrada já decrescente, em que o Insertion Sort faz uma única passada.

```bash
python parte2/benchmark.py
```

## Contexto acadêmico

Trabalho Discente Efetivo (TDE) da disciplina **Algoritmos e Estruturas de Dados** (2026.2), no **UNIFAN — Centro Universitário Nobre**. A Parte 1 reúne listas, pilha, fila de prioridade e busca e ordenação manuais. A Parte 2 otimiza o sistema com árvore balanceada, travessias, busca, divisão e conquista e medição de desempenho.
