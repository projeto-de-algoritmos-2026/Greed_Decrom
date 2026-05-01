from argparse import ArgumentParser, RawTextHelpFormatter, Action
import os

not_stored = ['export', 'input', 'DEBUG', 'additive']

class color:
    BOLD = '\033[1m'
    BOLD_END = '\033[22m'
    OVERLINE = '\033[53m'
    OVERLINE_END = '\033[55m'
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


def parse_args():
    parser = ArgumentParser(
        description=
f"""Conversor de números decimais em algarismos romanos\n
notas:
    - por padrão, se a entrada for inteira serão utilizados os símbolos da numeração romana padrão moderna
      - se a entrada for fracionária, a maior precisão possível será utilizada (veja {color.BOLD}-r{color.BOLD_END} e {color.BOLD}-i{color.BOLD_END})
    - o programa não limita o tamanho da entrada, isso pode resultar em longas repetições do maior símbolo (e.g. MMMMMMMMMMM = 11_000). veja {color.BOLD}--max-largest{color.BOLD_END}
    - duas maneiras de representar números grandes estão disponíveis: vinculum({color.BOLD}-v{color.BOLD_END}, {color.BOLD}-V{color.BOLD_END}) e apostrophus ({color.BOLD}-b{color.BOLD_END})""", 
        epilog='Criado por: Laisczt, Sunamit\nMaio de 2026', 
        formatter_class=RawTextHelpFormatter, 
        fromfile_prefix_chars="@")

    # Número de entrada
    parser.add_argument('input', help='number to be converted, in decimal notation')

    # Argumentos
    parser.add_argument('--export', help='exportar configurações de estilo pro arquivo')
    parser.add_argument('--max-largest', default= 0, help='quantidade máxima de vezes que o maior símbolo pode ser repetido. Ao passar disso levanta runtime error\n *valor de 0 -> ilimitado\n *default: ilimitado')

    # Flags
    parser.add_argument('--DEBUG', action='store_true', help='DEBUG PRINTS')
    parser.add_argument('-a', '--additive', action='store_true', help=f'utiliza a forma aditiva (e.g XXXX ao invés de XL)\n *compõe {color.BOLD}-N{color.BOLD_END} e {color.BOLD}-F{color.BOLD_END}')
    parser.add_argument('-A', '--additive-long', action='store_true', help=f'exclui V,L,D,etc. (símbolos com valores decimais começando com 5), optando por usar a forma aditiva (e.g iiiiiii ao invés de 7)\n *implica {color.BOLD}-a{color.BOLD_END}\n *incompatível com {color.BOLD}-s{color.BOLD_END}, {color.BOLD}-S{color.BOLD_END}, {color.BOLD}-d{color.BOLD_END}')
    parser.add_argument('-f', '--additive-four', action='store_true', help='utiliza forma aditiva para representar o valor 4 (IIII)')
    parser.add_argument('-F', '--additive-fours', action='store_true', help=f'utiliza forma aditiva para representar os valores 4, 40, e 400\n *implica {color.BOLD}-f{color.BOLD_END}')
    parser.add_argument('-J', '--please-jupiter', action='store_true', help='utiliza a forma aditiva para representar o valor 4 (IIII), somente se a entrada for exatamente 4')
    parser.add_argument('-n', '--additive-nine', action='store_true', help=f'utiliza forma aditiva para representar o valor 9 (VIIII)\n *incompatível com {color.BOLD}-S{color.BOLD_END}')
    parser.add_argument('-N', '--additive-nines', action='store_true', help=f'utiliza forma aditiva para representar os valores 9, 90, e 900\n *implica {color.BOLD}-n{color.BOLD_END}')
    parser.add_argument('-s', '--subtractive-forms', action='store_true', help=f'permite representações subtrativas não padrão (e.g IC, XM, XD)\n *incompatível com {color.BOLD}-A{color.BOLD_END}')
    parser.add_argument('-S', '--subtractive-long', action='store_true', help=f'permite representações subtrativas com até 3 caractéres em sequência\n *incompatível com {color.BOLD}-A{color.BOLD_END} e {color.BOLD}-n{color.BOLD_END}')
    parser.add_argument('-d', '--subtractive-fives', action='store_true', help=f'permite que não-potências-de-cinco (V,L,D) sejam utilizados subtrativamente, com até 1 caractér em sequência\n *incompatível com {color.BOLD}-A{color.BOLD_END}\n *implica {color.BOLD}-s{color.BOLD_END}')
    parser.add_argument('-c', '--clock', action='store_true', help=f'caso a entrada seja de 1-12, utiliza caractéres utf8 dedicados\n *pode causar inconsistência com {color.BOLD}-j{color.BOLD_END}')
    parser.add_argument('-u', '--unicode', action='store_true', help=f'utiliza caractéres utf8 para símbolos latinos (quando possível). Exclui caracteres dedicados da notação apostrophus\n *veja {color.BOLD}-B{color.BOLD_END}')
    parser.add_argument('-l', '--lowercase', action='store_true', help='utiliza versões minúsculas dos símbolos (onde possível)')
    parser.add_argument('-o', '--nulla', action='store_true', help='caso a entrada for 0, imprime a palavra Nulla (o comportamento padrão é imprimir N)')
    parser.add_argument('-j', '--final-j', action='store_true', help=f'se o último símbolo inteiro for I, substitui por J\n *pode causar inconsistência com {color.BOLD}-c{color.BOLD_END}')
    parser.add_argument('-i', '--implied-fractions', action='store_true', help=f'não imprime parte fracional, mas risca o último dígito para indicar existência da mesma (e.g {color.CROSS}I{color.RESET},{color.CROSS}M{color.RESET})\n *incompatível com {color.BOLD}-r{color.BOLD_END} e {color.BOLD}-R{color.BOLD_END}')
    parser.add_argument('-r', '--limited-fractions', action='store_true', help='arredonda valores fracionais a frações de 12 (Uncias)')
    parser.add_argument('-R', '--expanded-fractions', action='store_true', help='não utiliza caractéres compactos para uncias')
    parser.add_argument('-v', '--vinculum', action='store_true', help=f'utiliza notação vinculum (aka titulum) para números grandes. Inclui multiplicação por 1000\n *veja também {color.BOLD}-V{color.BOLD_END}')
    parser.add_argument('-V', '--vinculum-large', action='store_true', help=f'utiliza notação vinculum (aka titulum) para números grandes. Inclui multiplicação por 1000 e 100_000\n *implica {color.BOLD}-v{color.BOLD_END}\n *incompatível com {color.BOLD}-b{color.BOLD_END}')
    parser.add_argument('-b', '--apostrophus', action='store_true', help=f'utiliza notação apostrophus para números grandes\n *veja também {color.BOLD}-B{color.BOLD_END}\n *incompatível com {color.BOLD}-v{color.BOLD_END}')
    parser.add_argument('-B', '--apostrophus-special', action='store_true', help=f'utiliza símbolos utf8 dedicados para notação apostrophus\n *implica {color.BOLD}-b{color.BOLD_END}')

    implicacoes = { # a opção à esquerda implica todas à direita (USE _ AO INVES DE -)
        "additive" : ("additive_fours", "additive_nines"),
        "additive_long" : tuple(["additive"]),
        "additive_fours" : tuple(["additive_four"]),
        "additive_nines" : tuple(["additive_nine"]),
        "apostrophus_special": tuple(["apostrophus"]),
        "vinculum_large": tuple(["vinculum"]),
        "subtractive_fives": tuple(["subtractive_forms"])
    }

    incompat = { # cada opção à esquerda é incompatível com cada uma à direita
        tuple(['additive_long']): ('subtractive_forms', 'subtractive_fives', 'subtractive_long'),
        tuple(['additive_nine']): tuple(['subtractive_long']),
        tuple(['implied_fractions']): ('expanded_fractions', 'limited_fractions'),
        tuple(['vinculum']): tuple(['apostrophus'])
    }

    a = parser.parse_args() # argumentos podem ser acessados com a.nomeArg

    try:    # Verifica se a entrada é numérica
        float(a.input)
    except:
        raise ValueError(f"Entrada deve ser numérica: {color.RED}{a.input}{color.PURPLE}")
    
    maxlisint = True
    if(type(a.max_largest) != int):
        maxlisint = a.max_largest.isdigit()
    if not maxlisint:
        raise ValueError(f"{color.BOLD}--max-largest{color.BOLD_END} deve ser número inteiro: {color.RED}{a.max_largest}{color.PURPLE}")


    cascade(a, implicacoes) # propaga implicações
    
    hasIncompat = checkIncompat(a, incompat)# checa se existem incompatibilidades entre flags

    if(hasIncompat): 
        raise ValueError(f"Opções incompatíveis: {color.BOLD + color.RED}{"--"+hasIncompat[0]}{color.BOLD_END + color.PURPLE}, {color.BOLD + color.RED}{"--"+hasIncompat[1]}{color.BOLD_END + color.PURPLE}")

    return a

def export(export): # exporta configurações de estilo à arquivo
    path = a.export
    if(os.path.isdir(path)):
        raise ValueError(f"Caminho provido para export é um diretório: {color.RED}{a.export}{color.PURPLE}")
    
    with open(path, 'w') as f:
        for arg, val in vars(a).items():
            if arg in not_stored : continue
            if arg == 'max_largest' and val != 0:
                f.write("--" + arg.replace("_", '-') + "=" + val + "\n")
                continue
            if not val: continue
            f.write("--" + arg.replace("_", "-") + "\n")