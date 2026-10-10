# ERP de Carregadores Elétricos

Este projeto consiste em um sistema desenvolvido em Python para gerenciar carregadores elétricos e suas ordens de serviço. A proposta é aplicar conceitos de ERP (Enterprise Resource Planning, ou sistema integrado de gestão empresarial) ao cadastro de equipamentos, à organização dos atendimentos e ao acompanhamento dos serviços realizados.

O programa funciona pelo terminal, utilizando menus interativos para cadastrar registros, consultar informações, atender ordens por prioridade e gerar relatórios.

## Funcionalidades

- Cadastro, consulta, alteração e remoção de carregadores;
- Registro do nome, local de instalação e potência de cada carregador;
- Cadastro e consulta de ordens de serviço vinculadas aos carregadores;
- Alteração e remoção de ordens pendentes;
- Classificação das ordens nas prioridades crítica, alta e normal;
- Atendimento da próxima ordem conforme sua prioridade;
- Histórico dos serviços concluídos;
- Opção para desfazer o último atendimento;
- Filtragem de ordens pelo status;
- Exibição da fila na sequência de atendimento;
- Listagem de carregadores ordenados por potência;
- Consulta da quantidade de registros cadastrados.

## Tecnologias e conceitos utilizados

- Linguagem Python;
- Listas e dicionários;
- Pilha para o histórico de atendimentos;
- Fila de prioridade para organizar as ordens;
- Busca linear implementada manualmente;
- Insertion Sort implementado manualmente;
- Funções, estruturas condicionais e laços de repetição;
- Validação de dados inseridos pelo usuário.

## Organização dos atendimentos

As ordens de serviço recebem uma prioridade no momento do cadastro:

- **1 — Crítica:** atendida primeiro;
- **2 — Alta:** atendida após as ordens críticas;
- **3 — Normal:** atendida após as ordens de maior prioridade.

Quando duas ordens possuem a mesma prioridade, o sistema mantém a ordem de chegada. Ao concluir um atendimento, a ordem é retirada da fila e adicionada ao histórico. A opção de desfazer utiliza o comportamento de uma pilha: somente o atendimento mais recente é revertido.

## Busca e ordenação

A consulta por código utiliza busca linear, percorrendo os registros até encontrar o item solicitado. Esse algoritmo possui melhor caso **O(1)** e pior caso **O(n)**.

O relatório de carregadores por potência utiliza Insertion Sort para apresentar os equipamentos em ordem decrescente. A ordenação é realizada sobre uma cópia da lista, preservando a ordem original dos cadastros. Seu melhor caso é **O(n)** e seu pior caso é **O(n²)**.

A fila de prioridade é representada por uma lista. Para atender a próxima ordem, o programa percorre os elementos e identifica a maior prioridade, com complexidade **O(n)**.

## Regras e validações

O sistema exige nome e local de instalação para cadastrar um carregador, além de uma potência positiva e finita. Para cadastrar uma ordem, é necessário informar um carregador existente, uma descrição e uma prioridade válida.

Carregadores com ordens associadas não podem ser removidos. Ordens concluídas também não podem ser alteradas ou excluídas pelas operações de cadastro; o último atendimento pode ser revertido pela opção de desfazer.

## Como executar

É necessário ter Python 3 instalado. O projeto utiliza apenas a biblioteca padrão da linguagem, sem dependências externas.

Na pasta em que está o arquivo, execute:

```bash
python TDE.py
```

Após iniciar o programa, cadastre um carregador pela opção **2** e crie uma ordem de serviço pela opção **6**. Utilize a opção **10** para atender a próxima ordem e a opção **12** para acessar os relatórios.

## Objetivo do projeto

O objetivo é aplicar algoritmos e estruturas de dados em um contexto prático de gestão de carregadores elétricos. O sistema reúne operações de cadastro, consulta, alteração e remoção, além de priorização de serviços, histórico reversível e geração de relatórios.

## Contexto acadêmico

Este projeto foi desenvolvido como **Trabalho Discente Efetivo (TDE), Parte 1**, da disciplina **Algoritmos e Estruturas de Dados**, referente ao período **2026.2**, no **UNIFAN — Centro Universitário Nobre**.

O trabalho propõe o desenvolvimento de um ERP com listas, pilha, fila de prioridade e algoritmos de busca e ordenação implementados manualmente.

## Observações

Os dados são armazenados apenas na memória durante a execução. Ao encerrar o programa, os cadastros e o histórico são perdidos.

O código está organizado em funções e contém comentários sobre o funcionamento das operações e a complexidade dos algoritmos.

## Status do projeto

Versão acadêmica com interface de terminal. Entre as possibilidades de evolução estão a persistência dos dados em arquivos ou banco de dados, a organização do código em módulos e a criação de uma interface gráfica.
