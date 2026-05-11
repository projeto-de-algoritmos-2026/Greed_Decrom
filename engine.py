import math
import re
import cli
from symbols import sesuncia, getPrintable, getClockFace, getPleaseJupiter 
import sys

def run_counter(valor, symbols, a):
     # Caso Especial: Zero
    if valor == 0:
        if a.lowercase:
            return "nulla" if a.nulla else "n"
        else:
            return "Nulla" if a.nulla else "N"

    # Caso Especial: Please Jupiter (-J)
    if a.please_jupiter and valor.is_integer() and valor == 4:
        return getPrintable(getPleaseJupiter()[0]['reps'], a.lowercase, a.unicode)

    # Caso Especial: Clock Face (-c)
    if a.clock and valor.is_integer() and 1 <= valor <= 12:
        clock_symbols = getClockFace()
        return getPrintable(clock_symbols[int(valor)-1]['reps'], a.lowercase, True)
        

    valor_original = valor
    trabalho_valor = valor
    do_imply_fractions = False
    if a.implied_fractions and not valor.is_integer():
        trabalho_valor = math.ceil(valor)
        do_imply_fractions = True

    resultado = ""
    restante = trabalho_valor

    primeiro_simbolo = True
    contagem_maior = 0

    for s in symbols:
        valor_s = s['valor']

        rep = getPrintable(s['reps'], a.lowercase, a.unicode)

        while restante >= valor_s:
            contagem_maior += 1
            if a.max_largest != 0 and primeiro_simbolo and contagem_maior > a.max_largest:
                raise RuntimeError(f"O maior símbolo foi repetido {contagem_maior} vezes, ultrapassando o limite de {a.max_largest}.")

            if do_imply_fractions and restante - valor_s == 0:
                resultado += cli.color.CROSS + rep + cli.color.RESET
            else:
                resultado += rep
            restante -= valor_s
            restante = round(restante, 10)
        primeiro_simbolo = False

    if not resultado or resultado.strip() == "":
        if a.lowercase:
            return "nulla" if a.nulla else "n"
        else:
            return "Nulla" if a.nulla else "N"

    resultado = resultado.replace('||', '')
    resultado = resultado.replace('\033[55m\033[53m', '') 
    resultado = resultado.replace('|\033[9m|', '\033[9m') 

    # J final
    if a.final_j and resultado.endswith(('I', 'i', 'Ⅰ', 'ⅰ')):
        map_j = {'I': 'J', 'i': 'j', 'Ⅰ': 'J', 'ⅰ': 'j'}
        resultado = resultado[:-1] + map_j.get(resultado[-1], resultado[-1])

    # Sesuncia
    ind = resultado.find('Є' if not a.lowercase else 'є')
    if ind >= 1:
        resultado = resultado[:ind-1] + sesuncia(resultado[ind-1],a.lowercase) + resultado[ind+1:]

    return resultado