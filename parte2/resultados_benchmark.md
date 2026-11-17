Testes de corretude: OK

Mediana de 5 execuções; semente 42

### Busca por código (1000 buscas)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 14.079 | 0.409 | 34.40x |
| 1000 | 26.890 | 0.697 | 38.60x |
| 2000 | 65.638 | 0.511 | 128.37x |
| 4000 | 117.217 | 0.606 | 193.40x |
| 8000 | 247.391 | 0.576 | 429.72x |

### Ordenação por potência decrescente - entrada aleatorio (Insertion Sort x Merge Sort)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 5.310 | 0.726 | 7.31x |
| 1000 | 31.732 | 1.523 | 20.83x |
| 2000 | 83.863 | 3.319 | 25.27x |
| 4000 | 361.451 | 15.009 | 24.08x |
| 8000 | 1973.092 | 16.915 | 116.65x |

### Ordenação por potência decrescente - entrada crescente (Insertion Sort x Merge Sort)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 10.016 | 0.579 | 17.31x |
| 1000 | 83.135 | 2.392 | 34.76x |
| 2000 | 236.881 | 5.337 | 44.38x |
| 4000 | 874.871 | 6.470 | 135.22x |
| 8000 | 4157.248 | 12.837 | 323.86x |

### Ordenação por potência decrescente - entrada decrescente (Insertion Sort x Merge Sort)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 0.074 | 0.614 | 0.12x |
| 1000 | 0.099 | 1.278 | 0.08x |
| 2000 | 0.199 | 2.712 | 0.07x |
| 4000 | 0.404 | 5.786 | 0.07x |
| 8000 | 0.825 | 12.907 | 0.06x |

### Atender todas as ordens da fila
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 6.572 | 1.169 | 5.62x |
| 1000 | 26.320 | 2.539 | 10.37x |
| 2000 | 104.054 | 9.055 | 11.49x |
| 4000 | 584.869 | 19.658 | 29.75x |
| 8000 | 2415.972 | 43.018 | 56.16x |

### Cadastro de n ordens (custo de inserção)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 0.134 | 5.391 | 0.02x |
| 1000 | 0.264 | 11.923 | 0.02x |
| 2000 | 0.587 | 25.990 | 0.02x |
| 4000 | 1.049 | 56.630 | 0.02x |
| 8000 | 2.122 | 122.611 | 0.02x |

### Checagem 'carregador tem ordens?' (200 consultas, pior caso)
| n | Parte 1 (ms) | Parte 2 (ms) | Speedup |
|---:|---:|---:|---:|
| 500 | 3.907 | 0.039 | 100.17x |
| 1000 | 7.880 | 0.039 | 201.53x |
| 2000 | 15.921 | 0.039 | 408.23x |
| 4000 | 32.181 | 0.040 | 794.60x |
| 8000 | 63.743 | 0.040 | 1597.58x |

### Altura da AVL com chaves sequenciais
| n | altura AVL | ceil(log2(n+1)) |
|---:|---:|---:|
| 500 | 9 | 9 |
| 1000 | 10 | 10 |
| 2000 | 11 | 11 |
| 4000 | 12 | 12 |
| 8000 | 13 | 13 |
