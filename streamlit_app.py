import streamlit as st
import pandas as pd
import plotly.express as px

# Excelファイルを読み込む
#@st.cache  # データのキャッシュを有効にして高速化
def load_data():
    df = pd.read_excel("questionnaire.xlsx")  # Excelファイルのパスを指定
    return df

df = load_data()

# 設問を表示
st.title("ベイマックス")

# ラジオボタンのデフォルト選択肢
options1 = ["4 とてもあてはまる", "3 少しあてはまる", "2 あまりあてはまらない", "1 全くあてはまらない"]
options2 = ["4 とてもあてはまる", "3 少しあてはまる", "2 あまりあてはまらない", "1 全くあてはまらない"]

factors = df["因子名"]

factors

# ラジオボタンで回答を収集し、因子ごとの平均点を計算
factor_scores = {}
for factor in factors:

    

    st.subheader(factor)
    factor_data = df[df["因子名"] == factor]
    total_score = 0
    for idx, row in factor_data.iterrows():
        st.write(row["設問名"])
        score = st.radio("回答", options1, key=row["設問名"])
        # 反転項目の場合、数値を反転
        if row["反転"]:
            score = 5 - int(score[0])
        else:
            score = int(score[0])
        total_score += score
    avg_score = total_score / len(factor_data)
    factor_scores[factor] = avg_score
    st.write(f"{factor}の平均点: {avg_score:.2f}")

