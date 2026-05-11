import math
import re
import cli
from symbols import sesuncia, getPrintable

def run_counter(valor, symbols, a):
    if valor == 0:
        return "Nulla" if a.nulla else "N"

    valor_original = valor
    trabalho_valor = valor
    if a.implied_fractions and (valor % 1 != 0):
        trabalho_valor = math.ceil(valor)

    resultado = ""
    restante = trabalho_valor


    for s in symbols:
        valor_s = s['valor']
        
        if valor_s == 1/24:
            while restante >= valor_s:
                # Chamamos sua função que move a uncia: (∴ + Є -> :Є·)
                resultado = sesuncia(resultado, a.lowercase)
                restante -= valor_s
                restante = round(restante, 10)
            continue

        rep = getPrintable(s['reps'], a.lowercase, a.unicode)
        while restante >= valor_s:
            resultado += rep
            restante -= valor_s
            restante = round(restante, 10)

    if not resultado or resultado.strip() == "":
        return "Nulla" if a.nulla else "N"

    resultado = resultado.replace('\033[55m\033[53m', '')
    resultado = resultado.replace('||', '') 
    # Regex para garantir que blocos como |X| |I| fiquem |XI|
    resultado = re.sub(r'\|(.*?)\|\|(.*?)\|', r'|\1\2|', resultado)

    if a.final_j and resultado.endswith(('I', 'i', 'Ⅰ', 'ⅰ')):
        map_j = {'I': 'J', 'i': 'j', 'Ⅰ': 'J', 'ⅰ': 'j'}
        resultado = resultado[:-1] + map_j.get(resultado[-1], resultado[-1])

    if a.implied_fractions and (valor_original % 1 != 0):
        ultimo = resultado[-1]
        resultado = resultado[:-1] + cli.color.CROSS + ultimo + cli.color.RESET

    return resultado