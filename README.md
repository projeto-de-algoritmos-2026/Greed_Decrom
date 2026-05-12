# Decrom (Decimal to Roman)

**Número da Lista:** 37<br>
**Conteúdo da Disciplina:** Algoritmos Ambiciosos (Greedy)<br>

## Apresentação

[Link Apresentação](https://youtu.be/4KiY5tEHL44)

Decrom (Decimal to Roman) é um conversor de números decimais para algarismos romanos com alta configurabilidade. O software foi desenvolvido para suportar não apenas a numeração padrão, mas uma vasta gama de representações históricas, acadêmicas e tipográficas. Utiliza o **algorítmo de contador (Cashier's algorithm)** para montar o valor em algarismos romanos. Sendo capaz de converter de números inteiros comuns até frações com o sistema romano base-12 e números de grande escala (milhares e milhões). Esse motor pode ser acessado por interface CLI ou GUI em website local.

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 21/1029512  |  Laís Cecília Soares Paes |
| 22/1008697  |  Sunamita Vitória Rodrigues dos Santos |

## Sobre 

### Objetivo
O objetivo central é demonstrar a aplicação de um algoritmo ambicioso na resolução do problema de decomposição numérica. Enquanto conversores comuns são limitados ao sistema subtrativo moderno (IV, IX, etc.), este projeto integra "flags" que alteram dinamicamente a tabela de símbolos disponível, forçando o algoritmo a tomar decisões baseadas em diferentes contextos históricos e matemáticos.

### Como funciona o Algoritmo do Contador (Cashier's Algorithm)
O núcleo do sistema (no arquivo `engine.py`) implementa um **Greedy Algorithm**. A cada iteração, o algoritmo:
1. Analisa o valor decimal atual.
2. Varre a lista de símbolos (gerada dinamicamente pelo `symbols.py`) em ordem decrescente.
3. Escolhe a "maior peça" que cabe no valor restante.
4. Concatena essa peça ao resultado e subtrai seu valor do total.
5. Repete o processo até que o resto seja zero ou o limite de precisão seja atingido.

Para que seja possível utilizar o algoritmo de contador para isso, é necessária que a lista de símbolos ("moedas") inclua não só os símbolos comuns (I,X,V,C,D, etc), como também todas as subtrações entre eles (IV, IX, XC, CD, etc)

### Representações Não Padrões e Flags
O projeto integra as seguintes lógicas integradas ao front-end:
* **Lógica Aditiva:** Representações como `IIII` (4) e `VIIII` (9) em vez de `IV` e `IX`.
* **Superstição (Please Jupiter):** Substituição de `IV` por `IIII` apenas quando o valor é exatamente 4, respeitando o tabu religioso romano.
* **Notações de Grande Escala:**
   * **Vinculum:** Uso de barras superiores para multiplicar valores por 1.000.
   * **Apostrophus:** Sistema clássico de `C|Ɔ` para milhares e quinhentos.
* **Frações Unciais:** Decomposição de decimais em base 12 (Sextans, Quadrans, Semis), utilizando símbolos como pontos `·` e a letra `S`.
* **Estética Tipográfica:** Flags para J-Final (uso de `J` no último caractere), Unicode dedicado e faces de relógio.
* **Entre outras...**


## Instalação 
**Linguagem:** Python 3.10+<br>
**Framework:** Streamlit (para interface web)

### Pré-requisitos
Certifique-se de ter o Python e o gerenciador de pacotes `pip` instalados. Para poder utilizar a interface gráfica, execute:

```bash
pip install streamlit
```

## Uso
O projeto pode ser utilizado de duas maneiras distintas:

### 1. Interface Web (Recomendado):

(pode ter problemas no windows)

A interface gráfica oferece uma visão clara das flags e explicações sobre cada funcionalidade. Para iniciar, execute:

```bash
streamlit run app.py
```

Passo a passo na Interface:

Sidebar: Utilize as abas laterais para configurar as regras do algoritmo.

Entrada: Digite o número decimal no campo central (ex: 2026 ou 14.5).

Conversão: Clique no botão Executar Conversão. O resultado será exibido em um card estilizado com a tipografia escolhida.

### 2. Interface de Linha de Comando (CLI):

Para usuários que preferem o terminal ou precisam de saídas rápidas para scripts:

```bash
python ./decrom.py [numero] [flags]
```
-h: exibe todas as opções e informações adicionais

-a: Ativa a forma aditiva geral (ex: 4 = IIII).

-u: Utiliza caracteres Unicode dedicados.

-j: Ativa o J-Final (ex: VIII vira VIIJ).

-v: Ativa a notação Vinculum para números acima de 3.999.

--DEBUG: Imprime a tabela de símbolos que o algoritmo "ambicioso" usou para aquela conversão específica.

## Screenshots

Menu de ajuda no CLI:
<img width="1575" height="871" alt="image" src="https://github.com/user-attachments/assets/57db1f62-7d44-4493-941a-9b66795f33ae" />

Exemplo de tabela de símbolos:
<img width="688" height="640" alt="image" src="https://github.com/user-attachments/assets/d19206b9-2d1a-4cfc-836e-f83c14367591" />

Resultado símples no CLI:
<img width="688" height="28" alt="image" src="https://github.com/user-attachments/assets/312da4b4-3407-44a3-864b-9e8ccb4447ff" />


Erro de incompatibilidade no CLI:
<img width="1195" height="148" alt="image" src="https://github.com/user-attachments/assets/a754e048-fa43-425a-9e22-603a460cdb4d" />

Exportação de configurações:
<img width="814" height="858" alt="image" src="https://github.com/user-attachments/assets/98e44dce-b22d-4301-adaa-614450e43094" />

Flags no GUI:
<img width="197" height="933" alt="image" src="https://github.com/user-attachments/assets/7328b0b6-e1eb-493f-9de9-afec5a4b5c10" />

Número grande (vinculum) no GUI:
<img width="1818" height="880" alt="image" src="https://github.com/user-attachments/assets/a34f259f-971f-458b-b153-eb2e8670b6d5" />

Número grande (apostrophus) no GUI:
<img width="1813" height="676" alt="image" src="https://github.com/user-attachments/assets/db2e1420-f4b3-4096-8fc0-a394e5449082" />

Número fracionário no GUI:
<img width="1805" height="532" alt="image" src="https://github.com/user-attachments/assets/4a800063-a563-4525-af54-8ebbd4a76f7e" />

Erro de incompatibilidade no GUI:
<img width="1813" height="715" alt="image" src="https://github.com/user-attachments/assets/b47ae806-cae3-4bbf-8a7d-422056b6cb44" />






## Outros

Tratamento de Exceções: O sistema previne estouros de repetição de caracteres através da flag --max-largest. 
Caso um número exija mais repetições do que o permitido (ex: 4000 sem notação Vinculum e com limite 3), um erro de tempo de execução amigável é retornado.

Precisão Decimal: O motor utiliza arredondamento de precisão $10^{-10}$ para evitar inconsistências comuns de ponto flutuante em Python durante as subtrações sucessivas.


