import streamlit as st
import engine
from symbols import generateSymbols

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

with st.sidebar.expander("Lógica do Algoritmo", expanded=True):
    la_gen = st.checkbox("Forma Aditiva Geral (-a)", help="Evita formas subtrativas (ex: IIII em vez de IV).")
    la_four = st.checkbox("4 Aditivo (IIII) (-f)")
    la_fours = st.checkbox("4, 40, 400 Aditivos (-F)")
    la_nine = st.checkbox("9 Aditivo (VIIII) (-n)")
    la_nines = st.checkbox("9, 90, 900 Aditivos (-N)")
    la_jupiter = st.checkbox("Please Jupiter (-J)", help="Usa IIII apenas se a entrada for exatamente 4.")
    la_subs_forms = st.checkbox("Subtrações não padrão (-s)", help="Permite IC, XM, etc.")

with st.sidebar.expander("Frações e Números Grandes"):
    f_implied = st.checkbox("Frações Implicadas (-i)", help="Arredonda para cima e risca o último dígito.")
    f_limited = st.checkbox("Frações Limitadas (Uncias) (-r)", help="Arredonda para frações de 12.")
    n_vinc = st.checkbox("Vinculum (-v)", help="Barra superior para multiplicar por 1.000.")
    n_vinc_l = st.checkbox("Vinculum Large (-V)", help="Multiplica por 100.000.")
    n_apos = st.checkbox("Apostrophus (-b)", help="Notação clássica C|Ɔ.")
    n_max = st.slider("Limite maior símbolo", 0, 10, 0, help="0 significa ilimitado.")

input_num = st.number_input("Digite o número decimal para conversão:", value=12.3, format="%.6f")

# Construção do objeto de flags com todas as chaves esperadas pelo engine e symbols
flags = AppFlags(
    input=input_num,
    unicode=u_unicode,
    lowercase=u_lower,
    nulla=u_nulla,
    final_j=u_finalj,
    clock=u_clock,
    please_jupiter=la_jupiter,
    max_largest=n_max,
    additive=la_gen,
    additive_long=False, 
    additive_four=la_four,
    additive_fours=la_fours,
    additive_nine=la_nine,
    additive_nines=la_nines,
    subtractive_forms=la_subs_forms,
    subtractive_long=False,
    subtractive_fives=False,
    apostrophus=n_apos,
    apostrophus_special=False,
    vinculum=n_vinc,
    vinculum_large=n_vinc_l,
    implied_fractions=f_implied,
    limited_fractions=f_limited,
    expanded_fractions=False,
    DEBUG=False
)

if st.button("Executar Conversão"):
    try:
        symbols_list = generateSymbols(
            flags.apostrophus,
            flags.apostrophus_special,
            flags.vinculum,
            flags.vinculum_large,
            flags.additive_long,
            flags.additive_four,
            flags.additive_fours,
            flags.additive_nine,
            flags.additive_nines,
            flags.subtractive_forms,
            flags.subtractive_long,
            flags.subtractive_fives,
            flags.implied_fractions,
            flags.limited_fractions,
            flags.expanded_fractions
        )

        resultado_raw = engine.run_counter(input_num, symbols_list, flags)

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
                <h1 style="font-family: 'serif'; font-size: 4em; color: white; margin: 0; line-height: 1.2;">
                    {resultado_html}
                </h1>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

st.markdown("---")
st.caption("Trabalho de Algoritmos Ambiciosos - Maio 2026")