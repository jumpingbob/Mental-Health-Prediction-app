import streamlit as st
import pandas as pd

def calculate_score(feature_importance, multiplier):
    # 特徴量の重要度と倍率を乗算してスコアを計算する関数
    score = sum(feature_importance * multiplier)
    return score

def main():
    st.title('Feature Importance Score Calculator')

    st.sidebar.header('Settings')
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xls", "xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write(df)

        # 特徴量の重要度と倍率を取得
        feature_importance = df.iloc[:, 0].values
        multiplier = df.iloc[:, 1].values

        if st.sidebar.button('Calculate Score'):
            # スコアを計算
            score = calculate_score(feature_importance, multiplier)
            st.write(f"Calculated Score: {score}")

if __name__ == "__main__":
    main()
