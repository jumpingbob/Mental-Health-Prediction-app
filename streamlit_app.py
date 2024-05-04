import streamlit as st
import numpy as np
import plotly.express as px

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features):
    user_input = []
    for feature in features:
        user_input.append(st.radio(f"{feature}を選択してください", options=["5とても高い", "4かなり高い", "3普通", "2かなり低い", "1とても低い"], index=2))
    return user_input

# Min-Max正規化
def min_max_scaling(user_input):
    min_val = np.min(user_input)
    max_val = np.max(user_input)
    scaled_values = [(x - min_val) / (max_val - min_val) for x in user_input]
    return scaled_values

# ストレスレベルを計算
def calculate_stress_level(scaled_values, feature_importances):
    stress_level = np.dot(scaled_values, feature_importances)
    return stress_level

# Streamlitアプリの実行
def main():
    st.title("メンタルヘルス推定アプリ")

    # データを収集した際の質問項目
    features = [
        "Anxiety level (不安レベル)",
        "Self-esteem (自尊心)",
        "Mental health history (精神保健の歴史)",
        "Depression (うつ病)",
        "Headache (頭痛)",
        "Blood pressure (血圧)",
        "Sleep quality (睡眠の質)",
        "Breathing problem (呼吸問題)",
        "Future career concerns (将来のキャリアに関する懸念)",
    ]

    # 各質問項目の特徴量重要度
    feature_importances = np.array([0.18, 0.16, 0.02, 0.85, 0.19, 0.03, 0.23, 0.03, 0.10])

    st.write("以下のラジオボタンで各項目を評価し、メンタルヘルスを計算します。")

    user_input = get_user_input(features)

    st.write("入力された値:", user_input)

    scaled_values = min_max_scaling(user_input)

    st.write("Min-Max正規化された値:", scaled_values)

    stress_level = calculate_stress_level(scaled_values, feature_importances)

    st.write("ストレスレベル:", stress_level)

    st.write("以下は、ストレスレベルをレーダーチャートで視覚化したものです。")
    fig = px.line_polar(
        r=scaled_values + scaled_values[:1],  # 周期的に閉じるために、最初の値を最後に追加
        theta=features + features[:1],  # 周期的に閉じるために、最初の項目を最後に追加
        line_close=True,
        title="メンタルヘルス",
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()