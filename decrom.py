#!/usr/bin/python3
import os
import cli
import engine
from symbols import *
from datetime import datetime

def getPrintable(reps, lowercase, unicode):
    """Retorna a representação correta baseada nas flags de estilo."""
    if lowercase:
        return reps[3] if unicode else reps[1]
    else:
        return reps[2] if unicode else reps[0]

def DEBUG_PRINT_SYMBOLS(listasimbolos):
    """Imprime a tabela de símbolos gerada para conferência."""
    print(f"{'VALOR':<10} : {'REPRESENTAÇÃO'}")
    for s in listasimbolos:
        if type(s['valor']) == int:
            print(f'{s["valor"]:<10} : {getPrintable(s["reps"], False, False)}')
        else:
            print(f'{s["valor"]:<10.6f} : {getPrintable(s["reps"], False, False)}')

def DEBUG_PRINT_ARGUMENTS(args):
    """Imprime todas as flags ativadas no terminal."""
    for k, v in vars(args).items():
        if k in ['input', 'DEBUG']: continue

        if (k == 'export' and v is not None):
            print("--" + k + '=' + os.path.realpath(v))
        elif (k == 'max_largest' and v != 0):
            print("--" + k + '=' + str(v))
        elif v:
            print("--" + k.replace("_", "-"))

def main():

    a = cli.parse_args()


    if a.export: 
        cli.export(a.export, a)

    starttime = datetime.now()
    symbols = generateSymbols(
        a.apostrophus,
        a.apostrophus_special,
        a.vinculum,
        a.vinculum_large,
        a.additive_long,
        a.additive_four,
        a.additive_fours,
        a.additive_nine,
        a.additive_nines,
        a.subtractive_forms,
        a.subtractive_long,
        a.subtractive_fives,
        a.implied_fractions,
        a.limited_fractions,
        a.expanded_fractions
    )
    totaltime = datetime.now() - starttime

    if a.DEBUG:
        print("CONFIGURAÇÕES ATIVAS")
        DEBUG_PRINT_ARGUMENTS(a)
        print("-=-=-=-=-=-=-=-=-=-")
        print("SÍMBOLOS")
        DEBUG_PRINT_SYMBOLS(symbols)
        print(f"TOTAL DE {len(symbols)} SÍMBOLOS GERADOS EM {float(totaltime.microseconds) / 1000 :.2f}ms")
        print("-=-=-=-=-=-=-=-=-=-")

    resultado_final = engine.run_counter(a.input, symbols, a)
    
    print(resultado_final)

if __name__ == "__main__":
    main()