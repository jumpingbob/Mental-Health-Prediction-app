import streamlit as st
import sympy as sp

# Streamlitアプリのタイトルを設定
st.title('漸化式アプリ')

# ガチャボタンを作成
if st.button('ガチャを引く'):
    # ガチャが押されたら漸化式を生成して表示
    n = sp.symbols('n', integer=True)
    
    # フィボナッチ数列の漸化式を定義（a_n = a_{n-1} + a_{n-2}）
    a_n_minus_1 = sp.Function('a')(n - 1)
    a_n_minus_2 = sp.Function('a')(n - 2)
    f_n = a_n_minus_1 + a_n_minus_2
    
    # 漸化式を表示
    st.write(f'生成された漸化式: $a_n = {sp.pretty(f_n)}$')

# 解答ボタンを作成
if st.button('解答を表示'):
    # 解答が押されたら漸化式の一般項を表示
    # フィボナッチ数列の一般項は直接計算できる
    a_n_formula = sp.Eq(sp.Function('a')(n), sp.fibonacci(n))
    st.write('漸化式の一般項: ', a_n_formula)

# Streamlitアプリを起動
if __name__ == '__main__':
    st.sidebar.markdown('作者: Your Name')
