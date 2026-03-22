# Tech Challenge FIAP — Fase 2
## Otimização de Modelo de Diagnóstico com Algoritmo Genético

# Objetivo

Otimizar um modelo de Machine Learning para diagnóstico de tumores (benigno vs maligno), priorizando a sensibilidade (recall)conforme o contexto clínico. A otimização foi realizada utilizando um Algoritmo Genético (GA) para ajuste automático de hiperparâmetros da Random Forest. Foram explorados ajustes também no threshold de decisão e no balanceamento de classes (class_weight).

Dataset utilizado foi Breast Cancer Wisconsin Dataset.

# Estrutura do Projeto

├── notebooks/
│   ├── 01_eda_baseline.ipynb
│   ├── 02_genetic_algorithm_rf.ipynb
│
├── data/
│   └── breast-cancer-wisconsin-data-set.csv
│
├── README.md

# Preparação de Ambiente

### 1) Criar um ambiente virtual (venv)

# Cria uma pasta `.venv/` contendo um Python “isolado” para este projeto.
# Evita conflitos de dependências entre projetos diferentes.  
python -m venv .venv

# Ativa ambiente virtual e troca o python terminal para dentro de .venv
.\.venv\Scripts\Activate.ps1

# Instala bibliotecas
pip install -r requirements.txt

# VS Code
"Select Kernel" (ou onde aparece a versão do Python, ex: "Python 3.10...")
"Python Environments...".
python ou ('venv': venv)

# Algoritmo Genético

O GA foi utilizado para otimizar os seguintes parâmetros:
- n_estimators
- max_depth
- min_samples_split
- min_samples_leaf
- max_features
- class_weight
- threshold (fronteira de decisão)

A função de fitness foi definida como:
fitness = 0.8 * F2-score + 0.2 * specificity

Foi utilizado F2-Score dada prioridade clínica de detecção:

Minimização de Falsos Negativos: 'Falso Negativo' (não detectar a doença presente) significa perda de tempo crítico para o tratamento da paciente
Ponderação Harmônica: Matematicamente, o F2-Score atribui mais importância ao Recall (Sensibilidade) do que à Precisão
Segurança Clínica: Enquanto a Precisão foca em não dar alarmes falsos, o F2-Score garante que o modelo seja 'conservador' e sensível o suficiente para identificar o maior número possível de casos malignos

O F2 prioriza recall e Specificity evita excesso de falsos positivos

# Experimentos

A Random Forest de Baseline utilizou os parâmetros

n_estimators=10
max_depth=2
min_samples_split=2
min_samples_leaf=1
max_features="sqrt"
class_weight=None
random_state=42

Foram realizados 3 experimentos com diferentes configurações:

Experimento	População	Gerações	Mutação
exp1	    20	        20	        0.10
exp2	    30	        25	        0.15
exp3	    40	        30	        0.20

Os parâmetros para ajustar os experimentos podem ser ajustados no bloco "Parametros Gerais do Algoritmo Genético"

# Genes
Os genes podem ser ajustados no bloco Gene Space, sendo parte em lista de itens e parte em faixa numérica

1. threshold: controla FN diretamente, maior impacto em recall
2. class_weight: influencia aprendizado da classe maligna
3. max_depth: controla complexidade da árvore
4. min_samples_leaf: suaviza ou agressiviza decisões
5. n_estimators: melhora estabilidade
6. max_features: quantidade máxima de colunas (características) que cada árvore pode enxergar

# Conclusão

O modelo baseline apresentou desempenho elevado, com alta especificidade e precisão, porém com limitações na detecção de todos os casos malignos, resultando em mais falsos negativos

A aplicação do algoritmo genético permitiu explorar automaticamente diferentes combinações de hiperparâmetros da Random Forest

O modelo otimizado apresentou Aumento do recall, redução de falsos negativos e leve aumento de falsos positivos

Esse comportamento representa um trade-off esperado e aceitável no contexto de diagnóstico médico, no qual é preferível investigar casos adicionais do que deixar de identificar uma condição potencialmente grave

O algoritmo genético convergiu rapidamente para soluções de alta qualidade, indicando que o problema possui uma região ótima relativamente acessível no espaço de busca. Isso é coerente com o fato de que uma Random Forest simples já apresenta forte desempenho nesse dataset

Destaca-se o tamanho reduzido do dataset, que restringe o espaço de melhoria e pode levar a resultados altamente estáveis

Além disso, a convergência rápida do GA sugere que métodos mais simples de otimização poderiam atingir resultados semelhantes neste cenário específico

Apesar disso, o uso do algoritmo genético foi relevante para demonstrar uma abordagem automatizada de otimização, permitindo avaliar diferentes configurações de forma sistemática e alinhada ao objetivo clínico




