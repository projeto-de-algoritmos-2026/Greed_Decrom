"""
Módulo de Interface Gráfica para o Conversor de Algarismos Romanos.
Este arquivo integra o motor de conversão (engine.py) com uma interface
moderna utilizando Streamlit, focada em UX e documentação técnica.
"""

import streamlit as st
import engine
from symbols import generateSymbols

st.set_page_config(
    page_title="Roman Converter Pro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .result-card {
        padding: 2rem;
        border-radius: 10px;
        background-color: #262730;
        border-left: 5px solid #FF4B4B;
        margin-top: 1rem;
    }
    .flag-desc {
        font-size: 0.85rem;
        color: #808495;
    }
    </style>
    """, unsafe_allow_html=True)


class ArgumentsMock:
    """Simula o objeto Namespace do argparse para compatibilidade com o engine."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def main():
    st.title("Conversor Romano Avançado")
    st.markdown("---")


    col_input, col_settings = st.columns([1, 2])

    with col_input:
        st.subheader("Entrada de Dados")
        decimal_val = st.number_input(
            "Valor Decimal", 
            min_value=0.0, 
            value=2026.0, 
            help="Insira o valor decimal (suporta frações unciais)."
        )
        
        st.info("O algoritmo utiliza uma abordagem Gulosa (Greedy) para decompor o valor.")

    with col_settings:
        st.subheader("Configurações de Algoritmo")
        

        tab_style, tab_logic, tab_large = st.tabs(["Estilo", "Lógica Aditiva", "Notações Antigas"])

        with tab_style:
            c1, c2 = st.columns(2)
            u_unicode = c1.checkbox("Símbolos Unicode (-u)", help="Usa caracteres latinos dedicados.")
            u_lower = c1.checkbox("Minúsculas (-l)", help="Retorna i, v, x em vez de I, V, X.")
            u_nulla = c2.checkbox("Palavra 'Nulla' (-o)", help="Substitui N por Nulla para o valor zero.")
            u_finalj = c2.checkbox("J-Final (-j)", help="Substitui o último I por J (comum em manuscritos).")
            u_clock = st.checkbox("Símbolos de Relógio (-c)", help="Usa Ⅰ-Ⅻ para valores entre 1 e 12.")

        with tab_logic:
            st.write("Controle de formas aditivas (IIII vs IV)")
            la_gen = st.checkbox("Aditivo Geral (-a)")
            la_four = st.checkbox("Somente 4 Aditivo (-f)")
            la_nines = st.checkbox("9, 90, 900 Aditivos (-N)")
            la_subs = st.checkbox("Subtrações Longas (IC, XM) (-s)")

        with tab_large:
            u_vinc = st.checkbox("Vinculum (-v)", help="Usa barras sobrepostas para multiplicar por 1.000.")
            u_apos = st.checkbox("Apostrophus (-b)", help="Usa a notação clássica de C, I e Ɔ.")
            u_max = st.number_input("Limite de Repetição (M)", 0, 10, 0)

    st.markdown("---")
    if st.button("Executar Conversão"):
        # Mapeamento para o objeto de flags
        args = ArgumentsMock(
            input=decimal_val,
            unicode=u_unicode,
            lowercase=u_lower,
            nulla=u_nulla,
            final_j=u_finalj,
            clock=u_clock,
            please_jupiter=False, # Pode ser integrado se desejar
            max_largest=u_max,
            additive=la_gen,
            additive_four=la_four,
            additive_fours=False,
            additive_nine=False,
            additive_nines=la_nines,
            subtractive_forms=la_subs,
            subtractive_long=False,
            subtractive_fives=False,
            apostrophus=u_apos,
            apostrophus_special=False,
            vinculum=u_vinc,
            vinculum_large=False,
            implied_fractions=False,
            limited_fractions=False,
            expanded_fractions=False
        )

        try:
         
            symbols = generateSymbols(
                args.apostrophus, args.apostrophus_special, args.vinculum, 
                args.vinculum_large, False, args.additive_four, False, 
                False, args.additive_nines, args.subtractive_forms, 
                False, False, False, False, False
            )
            
            
            res = engine.run_counter(decimal_val, symbols, args)
            
         
            st.markdown(f"""
                <div class="result-card">
                    <p style="margin:0; color:#808495; font-size:0.9rem;">RESULTADO DA CONVERSÃO</p>
                    <h1 style="margin:0; color:white; font-family:serif;">{res}</h1>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erro no processamento algorítmico: {e}")

if __name__ == "__main__":
    main()