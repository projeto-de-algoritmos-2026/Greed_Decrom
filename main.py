import os
from symbols import *
import cli

def getPrintable(reps, lowercase, unicode):
    if lowercase:
        if unicode:
            return reps[3]
        else:
            return reps[1]
    else:
        if unicode:
            return reps[2]
        else:
            return reps[0]


def DEBUG_PRINT_SYMBOLS(listasimbolos):
    for s in listasimbolos:
        if type(s['valor']) == int:
            print(f'{s["valor"]:<8} : {getPrintable(s["reps"],False, False)}')
        else:
            print(f'{s["valor"]:.6f} : {getPrintable(s["reps"],False, False)}')

def DEBUG_PRINT_ARGUMENTS(args):
    for k, v in vars(args).items():
        if k in ['input', 'DEBUG']: continue

        if (k == 'export' and v != None):
            print("--" + k + '=' + os.path.realpath(v))
        elif (k == 'max_largest' and v != 0):
            print("--" + k + '=' + v)
        elif v:
            print("--" + k.replace("_", "-"))



def main():
    
    a = cli.parse_args()

    if(a.export): cli.export(a.export)

    #   para SUNAMITA
    #   
    #   use `py main.py -h` para ver os argumentos e flags
    #   talvez você precise dar pip install argparse ou algo do tipo
    #   py main.py -[flags] num
    #
    #   argumentos podem ser acessados por a.nome_arg
    #   o valor a ser convertido está em `a.input` (precisa converter para float)
    #   além desses, você só deve precisar usar `a.lowercase`, `a.unicode`, `a.please_jupiter`, `a.nulla`, `a.clock`, `a.implied_fractions` e 'a.final_j' (TODOS SÃO BOOLEANOS)
    #   de uma olhada no -h para saber o que cada uma faz, qualquer dúvida pode perguntar
    #   para o `a.implied_fractions`, arredonde o número para cima e risque o último símbolo. faça assim: cli.color.CROSS + simbolo + cli.color.RESET
    #
    #   lista de símbolos está na variável symbols(em ordem decrescente do valor)
    #   para saber o valor de um símbolo use `symbol[ind]['valor']`
    #   para imprimir um símbolo, use a função `getPrintable(symbol[ind]['reps'], a.lowercase, a.unicode)`
    #
    #   é possível que um número fracional seja impossível de converter perfeitamente, cuidado para não criar um loop infinito
    #
    #   tem 2 funções para debug:
    #   `DEBUG_PRINT_SYMBOLS(symbols)` para imprimir os símbolos
    #   `DEBUG_PRINT_ARGUMENTS(a)` para imprimir os argumentos

    symbols = generateSymbols(   # Símbolos a serem usados com o algorítmo do contador
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

    clock = getClockFace() # Lista de números de 1-12, use caso o usuário utilize a opção -c/--clock e se o valor de entrada seja de 1-12
    jupiter = getPleaseJupiter() # Lista contendo somente IIII, use caso o usuário utiliza a opção -j/--please-jupiter, e se o valor de entrada seja exatamente 4

    if a.DEBUG:
        print("ARGUMENTOS")
        DEBUG_PRINT_ARGUMENTS(a)
        print("-=-=-=-=-=-=-=-=-=-=-=-")
        DEBUG_PRINT_SYMBOLS(symbols)
        print(F"GERADOS {len(symbols)} SIMBOLOS")
     

if __name__ == "__main__":
    main()