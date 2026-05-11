import sys, subprocess
import streamlit as st
from symbols import generateSymbols
from cli import export

st.set_page_config(
    page_title="Conversor Romano G37",
    page_icon="🏛️",
    layout="wide"
)

def ansi_to_html(text):
    """
    Traduz os códigos ANSI do terminal para tags HTML/CSS.
    Essencial para renderizar Vinculum (overline) e Implied Fractions (strike) na Web.
    """
   
    text = text.replace('\033[53m', '<span style="text-decoration: overline;">')
    text = text.replace('\033[55m', '</span>')
    
 
    text = text.replace('\033[9m', '<span style="text-decoration: line-through; color: #FF4B4B;">')
    text = text.replace('\033[0m', '</span>')
    
    return text

class AppFlags:
    """Simula o objeto retornado pelo argparse para compatibilidade com o engine.py"""
    def __init__(self, **entries):
        self.__dict__.update(entries)

st.title("Conversor Romano Ambicioso")
st.markdown("---")

st.sidebar.header("Configurações (Flags)")

# Organizando as flags em subseções na Sidebar
with st.sidebar.expander("Estilo e Tipografia", expanded=True):
    u_unicode = st.checkbox("Símbolos Unicode (-u)", help="Usa caracteres latinos dedicados (Ⅰ, Ⅴ, Ⅹ...)")
    u_lower = st.checkbox("Minúsculas (-l)", help="Retorna o resultado em caixa baixa.")
    u_nulla = st.checkbox("Usar 'Nulla' (-o)", help="Imprime 'Nulla' em vez de 'N' para o valor zero.")
    u_finalj = st.checkbox("Substituir final por 'J' (-j)", help="Prática antiga de trocar o último 'i' por 'j'.")
    u_clock = st.checkbox("Símbolos de Relógio (-c)", help="Usa glifos únicos de 1 a 12 (Ⅰ-Ⅻ).")

with st.sidebar.expander("Lógica Aditiva", expanded=False):
    la_long = st.checkbox("Forma Aditiva Longa (-A)", help="Só utiliza símbolos potências de 10 (ex: IIIIII em vez de VI)")
    la_gen = st.checkbox("Forma Aditiva Geral (-a)", help="Combina -F e -N")
    la_four = st.checkbox("4 Aditivo (IIII) (-f)")
    la_fours = st.checkbox("4, 40, 400 Aditivos (-F)")
    la_nine = st.checkbox("9 Aditivo (VIIII) (-n)")
    la_nines = st.checkbox("9, 90, 900 Aditivos (-N)")
    la_jupiter = st.checkbox("Please Jupiter (-J)", help="Usa IIII apenas se a entrada for exatamente 4.")
with st.sidebar.expander("Lógica Subtrativa", expanded=False):
    la_subs_forms = st.checkbox("Subtrações não padrão (-s)", help="Permite IC, XM, etc.")
    la_subs_fives = st.checkbox("Subtrações com cincos (-d)", help="Permite VC, LM, etc.")
    la_subs_long = st.checkbox("Subtrações longas (-S)", help="Permite IIC, XXXM, etc.")

with st.sidebar.expander("Frações e Números Grandes"):
    f_implied = st.checkbox("Frações Implicadas (-i)", help="Arredonda para cima e risca o último dígito.")
    f_limited = st.checkbox("Frações Limitadas (Uncias) (-r)", help="Arredonda para frações de 12.")
    f_expanded = st.checkbox("Frações expandidas (-R)", help="Não utiliza caracteres compactos para Uncias")
    n_vinc = st.checkbox("Vinculum (-v)", help="Barra superior para multiplicar por 1.000.")
    n_vinc_l = st.checkbox("Vinculum Large (-V)", help="Multiplica por 100.000.")
    n_apos = st.checkbox("Apostrophus (-b)", help="Notação clássica CIƆ.")
    n_apos_spec = st.checkbox("Apostrophus com símbolos especiais (-B)", help="Notação ↀ")
    n_max = st.slider("Limite maior símbolo", 0, 10, 0, help="0 significa ilimitado.")

input_num = st.number_input("Digite o número decimal para conversão:", value=12.3, format="%.6f")

# Construção do objeto de flags com todas as chaves esperadas pelo engine e symbols
flags = AppFlags(
    unicode=u_unicode,
    lowercase=u_lower,
    nulla=u_nulla,
    final_j=u_finalj,
    clock=u_clock,
    please_jupiter=la_jupiter,
    max_largest=n_max,
    additive=la_gen,
    additive_long=la_long, 
    additive_four=la_four,
    additive_fours=la_fours,
    additive_nine=la_nine,
    additive_nines=la_nines,
    subtractive_forms=la_subs_forms,
    subtractive_long=la_subs_long,
    subtractive_fives=la_subs_fives,
    apostrophus=n_apos,
    apostrophus_special=n_apos_spec,
    vinculum=n_vinc,
    vinculum_large=n_vinc_l,
    implied_fractions=f_implied,
    limited_fractions=f_limited,
    expanded_fractions=f_expanded,
)

if st.button("Executar Conversão"):
    try:
        export('./app_estilo.txt', flags)
        resultado_raw = subprocess.run([sys.executable, './main.py', '@app_estilo.txt', str(input_num)], capture_output=True, text=True).stdout.strip()

        resultado_html = ansi_to_html(resultado_raw)


        st.markdown(f"""
            <div style="
                background-color: #262730; 
                padding: 30px; 
                border-radius: 15px; 
                border-left: 8px solid #FF4B4B;
                margin-top: 20px;
                text-align: center;">
                <p style="color: #808495; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px;">Resultado Final</p>
                <p style="font-family: 'serif'; font-size: 4em; color: white; margin: 0; line-height: 1.2;">
                    {resultado_html}
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

st.markdown("---")
st.caption("Trabalho de Algoritmos Ambiciosos - Maio 2026")