import streamlit as st
import pandas as pd
import plotly.express as px

# Excelファイルを読み込む
@st.cache  # データのキャッシュを有効にして高速化
def load_data():
    df = pd.read_excel("questionnaire.xlsx")  # Excelファイルのパスを指定
    return df

df = load_data()

# 設問を表示
st.title("ベイマックス")

# ラジオボタンのデフォルト選択肢
options = ["4 とてもあてはまる", "3 少しあてはまる", "2 あまりあてはまらない", "1 全くあてはまらない"]

factors = df["因子名"]

df