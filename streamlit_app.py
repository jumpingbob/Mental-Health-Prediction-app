import streamlit as st
import pandas as pd
import plotly.express as px



# Excelファイルを読み込む
@st.cache  # データのキャッシュを有効にして高速化
def load_data():
    df = pd.read_excel("./questionaire.xlsx")  # Excelファイルのパスを指定
    return df

df = load_data()

# 設問を表示
st.title("ベイマックス")

# ラジオボタンのデフォルト選択肢
options = ["4 とてもあてはまる", "3 少しあてはまる", "2 あまりあてはまらない", "1 全くあてはまらない"]

# 因子名の一覧を取得
factors = df["因子名"].unique()

# ラジオボタンで回答を収集し、因子ごとの平均点を計算
factor_scores = {}
for factor in factors:
    st.subheader(factor)
    factor_data = df[df["因子名"] == factor]
    total_score = 0
    for idx, row in factor_data.iterrows():
        st.write(row["設問名"])
        score = st.radio("回答", options)
        # 反転項目の場合、数値を反転
        if row["反転項目"]:
            score = 5 - int(score[0])
        else:
            score = int(score[0])
        total_score += score
    avg_score = total_score / len(factor_data)
    factor_scores[factor] = avg_score
    st.write(f"{factor}の平均点: {avg_score:.2f}")

# レーダーチャートを描画
if factor_scores:
    st.subheader("因子ごとの評価")
    fig = px.line_polar(
        r=list(factor_scores.values()),
        theta=list(factor_scores.keys()),
        line_close=True
    )
    st.plotly_chart(fig)
