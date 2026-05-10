import streamlit as st
import engine
from symbols import generateSymbols

# Configuração da página
st.set_page_config(page_title="Conversor Romano", page_icon="🏛️")

st.title("🏛️ Conversor de Algarismos Romanos")

# Criamos uma classe para simular o objeto que o engine.py espera
class AppFlags:
    def __init__(self, **entries):
        self.__dict__.update(entries)

# --- SIDEBAR: Configurações (Flags) ---
st.sidebar.header("🔧 Configurações (Flags)")

# Flags de Estilo e Comportamento
additive_gen = st.sidebar.checkbox("Forma Aditiva Geral (-a)", value=False)
unicode_val = st.sidebar.checkbox("Usar Símbolos Unicode (-u)", value=False)
lowercase_val = st.sidebar.checkbox("Minúsculas (-l)", value=False)
nulla_val = st.sidebar.checkbox("Usar 'Nulla' para Zero (-o)", value=False)
final_j_val = st.sidebar.checkbox("Substituir último I por J (-j)", value=False)
clock_val = st.sidebar.checkbox("Usar Símbolos de Relógio (-c)", value=False)
jupiter_val = st.sidebar.checkbox("Please Jupiter (4 = IIII) (-J)", value=False)

# Flags de Representação Não Padrão
st.sidebar.markdown("---")
st.sidebar.subheader("Representações Especiais")
add_four = st.sidebar.checkbox("4 como IIII (-f)", value=False)
add_fours = st.sidebar.checkbox("4, 40, 400 aditivos (-F)", value=False)
add_nine = st.sidebar.checkbox("9 como VIIII (-n)", value=False)
add_nines = st.sidebar.checkbox("9, 90, 900 aditivos (-N)", value=False)
sub_forms = st.sidebar.checkbox("Subtrações não padrão (IC, XM) (-s)", value=False)

# Limite de repetição
max_val = st.sidebar.slider("Limite do maior símbolo (--max-largest)", 0, 10, 0)

# --- CORPO PRINCIPAL ---
input_num = st.number_input("Digite o número decimal:", value=2026.0)

# Criamos o objeto de flags com TODAS as chaves necessárias para evitar o erro de 'attribute'
flags = AppFlags(
    additive=additive_gen,
    unicode=unicode_val,
    lowercase=lowercase_val,
    nulla=nulla_val,
    final_j=final_j_val,
    clock=clock_val,
    please_jupiter=jupiter_val,
    max_largest=max_val,
    # Flags exigidas pelo symbols.py
    apostrophus=False,
    apostrophus_special=False,
    vinculum=False,
    vinculum_large=False,
    additive_long=False,
    additive_four=add_four,
    additive_fours=add_fours,
    additive_nine=add_nine,
    additive_nines=add_nines,
    subtractive_forms=sub_forms,
    subtractive_long=False,
    subtractive_fives=False,
    implied_fractions=False,
    limited_fractions=False,
    expanded_fractions=False
)

if st.button("Converter"):
    # 1. Gerar os símbolos usando as flags da UI
    symbols = generateSymbols(
        flags.apostrophus, flags.apostrophus_special, flags.vinculum, flags.vinculum_large,
        flags.additive_long, flags.additive_four, flags.additive_fours, flags.additive_nine,
        flags.additive_nines, flags.subtractive_forms, flags.subtractive_long,
        flags.subtractive_fives, flags.implied_fractions, flags.limited_fractions,
        flags.expanded_fractions
    )
    
    # 2. Executar o Algoritmo do Contador
    try:
        resultado = engine.run_counter(input_num, symbols, flags)
        st.subheader("Resultado:")
        st.code(resultado, language="")
    except Exception as e:
        st.error(f"Erro no processamento: {e}")