import cli
from symbols import getPrintable, getPleaseJupiter, getClockFace

def run_counter(valor, symbols, a):
    """
    O Algoritmo do Contador:
    Percorre a lista de símbolos (maior pro menor) e vai subtraindo
    o valor decimal enquanto concatena a representação romana.
    """
    
    # Caso Especial: Zero
    if valor == 0:
        return "Nulla" if a.nulla else "N"

    # Caso Especial: Please Jupiter (-J)
    if a.please_jupiter and valor == 4:
        return getPrintable(getPleaseJupiter()[0]['reps'], a.lowercase, a.unicode)

    # Caso Especial: Clock Face (-c)
    if a.clock and 1 <= valor <= 12 and valor == int(valor):
        clock_symbols = getClockFace()
        return getPrintable(clock_symbols[int(valor)-1]['reps'], a.lowercase, a.unicode)

    resultado = ""
    restante = valor
    primeiro_simbolo = True
    contagem_maior = 0

    # o loop
    for s in symbols:
        valor_s = s['valor']
        representacao = getPrintable(s['reps'], a.lowercase, a.unicode)

        while restante >= valor_s:
            # Validação da flag --max-largest
            if primeiro_simbolo and a.max_largest > 0:
                contagem_maior += 1
                if contagem_maior > a.max_largest:
                    raise RuntimeError(f"O maior símbolo foi repetido {contagem_maior} vezes, ultrapassando o limite de {a.max_largest}.")

            resultado += representacao
            restante -= valor_s
            # Round para evitar imprecisão de ponto flutuante (0.0000000001)
            restante = round(restante, 10) 
            
        if resultado != "": 
            primeiro_simbolo = False 


    # Final J (-j): Substitui o último 'i' por 'j'
    if a.final_j and resultado.endswith(('I', 'i', 'Ⅰ', 'ⅰ')):
        map_j = {'I': 'J', 'i': 'j', 'Ⅰ': 'J', 'ⅰ': 'j'} # J unicode é raro, usamos latino
        for char, j_char in map_j.items():
            if resultado.endswith(char):
                resultado = resultado[:-1] + j_char
                break

    # Implied Fractions (-i): Risca o último símbolo se tiver resto fracionário
    # (Como o contador consome tudo, checamos se o INPUT original tinha fração)
    if a.implied_fractions and (valor % 1 != 0):
        if resultado:
            ultimo = resultado[-1]
            resultado = resultado[:-1] + cli.color.CROSS + ultimo + cli.color.RESET

    return resultado