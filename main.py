import sys
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from symbols import getSymbols, clockFace, pleaseJupiter

class color:
    BOLD = '\033[1m'
    RESET = '\033[0m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CROSS = '\033[9m'

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
        print(f'{s["valor"]:<6} : {getPrintable(s["reps"],False, False)}')
def DEBUG_PRINT_ARGUMENTS(args):
    for k, v in vars(args).items():
        if k not in ['input', 'export'] and v:
            print(k)

def cascade(argumentos, implicacoes): # propaga implicações
    a = vars(argumentos)

    change = True

    while(change):
        change = False
        for opcao in list(a.keys()):
            if opcao in implicacoes.keys() and a[opcao]:
                for implicada in implicacoes[opcao]:
                    if(not a[implicada]):
                        a[implicada] = True
                        change = True

def checkIncompat(argumentos, incompatibilidades):
    a = vars(argumentos)
    for k, v in incompatibilidades.items():
        for opcao in k:
            if a[opcao]:
                for incompat in v:
                    if a[incompat]:
                        return (opcao, incompat)
    return tuple()


def main():
    parser = ArgumentParser(description="Conversor de números decimais em algarismos romanos", epilog='Criado por: Laisczt, Sunamit\nMaio de 2026', formatter_class=RawTextHelpFormatter, fromfile_prefix_chars="@")

    # Número de entrada
    parser.add_argument('input', help='number to be converted, in decimal notation')

    # Argumentos posicionais
    parser.add_argument('--export', help='exportar configurações de estilo pro arquivo')

    # Flags
    parser.add_argument('-a', '--additive', action='store_true', help=f'utiliza a forma aditiva (e.g XXXX ao invés de XL)\n *implica {color.BOLD}-N{color.RESET} e {color.BOLD}-F{color.RESET}')
    parser.add_argument('-A', '--additive-long', action='store_true', help=f'exclui V,L,D,etc. (símbolos com valores decimais começando com 5), optando por usar a forma aditiva (e.g iiiiiii ao invés de 7)\n *implica {color.BOLD}-a{color.RESET}\n *incompatível com {color.BOLD}-s{color.RESET}, {color.BOLD}-S{color.RESET}, {color.BOLD}-d{color.RESET}')
    parser.add_argument('-f', '--additive-four', action='store_true', help='utiliza forma aditiva para representar o valor 4 (IIII)')
    parser.add_argument('-F', '--additive-fours', action='store_true', help=f'utiliza forma aditiva para representar os valores 4, 40, e 400\n *implica {color.BOLD}-f{color.RESET}')
    parser.add_argument('-J', '--please-jupiter', action='store_true', help='utiliza a forma aditiva para representar o valor 4 (IIII), somente se a entrada for exatamente 4')
    parser.add_argument('-n', '--additive-nine', action='store_true', help='utiliza forma aditiva para representar o valor 9 (VIIII)')
    parser.add_argument('-N', '--additive-nines', action='store_true', help=f'utiliza forma aditiva para representar os valores 9, 90, e 900\n *implica {color.BOLD}-n{color.RESET}')
    parser.add_argument('-s', '--subtractive-forms', action='store_true', help=f'permite representações subtrativas não padrão (e.g IC, XM, XD)\n *incompatível com {color.BOLD}-A{color.RESET}')
    parser.add_argument('-S', '--subtractive-long', action='store_true', help=f'permite representações subtrativas com até 3 caractéres em sequência\n *incompatível com {color.BOLD}-A{color.RESET}')
    parser.add_argument('-d', '--subtractive-fives', action='store_true', help=f'permite que não-potências-de-cinco (V,L,D) sejam utilizados subtrativamente, com até 1 caractér em sequência\n *incompatível com {color.BOLD}-A{color.RESET}')
    parser.add_argument('-c', '--clock', action='store_true', help='caso a entrada seja de 1-12, utiliza caractéres utf8 dedicados')
    parser.add_argument('-u', '--unicode', action='store_true', help=f'utiliza caractéres utf8. Exclui caracteres dedicados da notação apostrophus\n *veja {color.BOLD}-B{color.RESET}({color.BOLD}--apostrophus-special{color.RESET})')
    parser.add_argument('-l', '--lowercase', action='store_true', help='utiliza versões minúsculas dos símbolos (onde possível)')
    parser.add_argument('-0', '--nulla', action='store_true', help='caso a entrada for 0, imprime a palavra Nulla (o comportamento padrão é imprimir N)')
    parser.add_argument('-i', '--implied-fractions', action='store_true', help=f'não imprime parte fracional, mas risca o último dígito para indicar existência de fração (e.g {color.CROSS}I{color.RESET},{color.CROSS}M{color.RESET})')
    parser.add_argument('-r', '--limited-fractions', action='store_true', help='arredonda valores fracionais a frações de 12 (Uncias)')
    parser.add_argument('-R', '--expand-fractions', action='store_true', help='não utiliza caractéres compactos para uncias')
    parser.add_argument('-b', '--apostrophus', action='store_true', help='utiliza notação apostrophus para números grandes')
    parser.add_argument('-B', '--apostrophus-special', action='store_true', help=f'utiliza símbolos utf8 dedicados para notação apostrophus\n *implica {color.BOLD}-b{color.RESET}')

    implicacoes = { # a opção à esquerda implica todas à direita (USE _ AO INVES DE -)
        "additive" : ("additive_fours", "additive_nines"),
        "additive_long" : tuple(["additive"]),
        "additive_fours" : tuple(["additive_four"]),
        "additive_nines" : tuple(["additive_nine"]),
        "apostrophus_special": tuple(["apostrophus"])
    }

    incompat = { # cada opção à esquerda é incompatível com cada uma à direita
        tuple(['additive_long']): ('subtractive_forms', 'subtractive_fives', 'subtractive_long'),
        tuple(['additive_nine']): tuple(['subtractive_long'])
    }

    a = parser.parse_args() # argumentos podem ser acessados com a.nomeArg

    cascade(a, implicacoes) # propaga implicações
    
    hasIncompat = checkIncompat(a, incompat)# checa se existem incompatibilidades entre flags

    if(hasIncompat): 
        raise ValueError(f"Opções incompatíveis: {color.BOLD + color.RED}{"--"+hasIncompat[0]}{color.RESET + color.PURPLE}, {color.BOLD + color.RED}{"--"+hasIncompat[1]}{color.RESET + color.PURPLE}")

    try:    # Verifica se a entrada é numérica
        float(a.input)
    except:
        raise ValueError(f"Entrada deve ser numérica: {color.RED}{a.input}{color.RESET + color.PURPLE}")


    if(a.export): # exporta configurações de estilo à arquivo
        path = a.export
        if(os.path.isdir(path)):
            raise ValueError(f"Caminho provido para export é um diretório: {color.RED}{a.export}{color.RESET + color.PURPLE}")
        
        with open(path, 'w') as f:
            for arg, val in vars(a).items():
                if arg in ['input', 'export']: continue
                if not val: continue
                f.write("--" + arg.replace("_", "-") + "\n")


    symbols = getSymbols(   # Símbolos a serem usados com o algorítmo do contador
        a.apostrophus,
        a.apostrophus_special,
        a.additive_long,
        a.additive_four,
        a.additive_fours,
        a.additive_nine,
        a.additive_nines,
        a.subtractive_forms,
        a.subtractive_long,
        a.subtractive_fives,
    )

    clock = clockFace() # Lista de números de 1-12, use caso o usuário utilize a opção -c/--clock e se o valor de entrada seja de 1-12
    jupiter = pleaseJupiter() # Lista contendo somente IIII, use caso o usuário utiliza a opção -j/--please-jupiter, e se o valor de entrada seja exatamente 4

    #   para SUNAMITA
    #   
    #   use `py main.py -h` para ver os argumentos e flags
    #   talvez você precise dar pip install argparse ou algo do tipo
    #   py main.py -[flags] num
    #
    #   argumentos podem ser acessados por a.nome_arg
    #   o valor a ser convertido está em `a.input` (precisa converter para float)
    #   além você só deve precisar usar `a.lowercase`, `a.unicode`, `a.please_jupiter`, `a.nulla`, `a.clock` e `a.implied_fractions` (TODOS SÃO BOOLEANOS)
    #   de uma olhada no -h para saber o que cada uma faz, qualquer dúvida pode perguntar
    #   para o `a.implied_fractions`, arredonde o número para cima e risque o último símbolo. faça assim: color.CROSS + simbolo + color.RESET
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

    #DEBUG_PRINT_SYMBOLS(symbols)
    #DEBUG_PRINT_ARGUMENTS(a)

if __name__ == "__main__":
    main()


