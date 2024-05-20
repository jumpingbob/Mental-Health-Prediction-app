import streamlit as st
import numpy as np
import plotly.express as px

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features):
    user_input = []
    for feature in features:
        user_input.append(st.radio(f"{feature}を選択してください", options=[5, 4, 3, 2, 1], index=2))
    return user_input

# 逆スコアリングを適用する
def reverse_scoring(user_input, reverse_indices):
    for i in reverse_indices:
        user_input[i] = 6 - user_input[i]  # 1から5の範囲なので、6 - current_valueで逆にする
    return user_input

# Min-Max正規化
def min_max_scaling(user_input):
    min_val = np.min(user_input)
    max_val = np.max(user_input)
    st.write(f"min_val: {min_val}, max_val: {max_val}")  # デバッグ出力
    if min_val == max_val:
        # すべての値が同じ場合、すべてのスケーリング値を0.5に設定
        scaled_values = [0.5 for _ in user_input]
    else:
        scaled_values = [(x - min_val) / (max_val - min_val) for x in user_input]
    st.write(f"scaled_values: {scaled_values}")  # デバッグ出力
    return scaled_values

# 因子スコアを計算
def calculate_factor_scores(scaled_values, factor_loadings):
    factor_scores = np.dot(scaled_values, factor_loadings)
    st.write(f"factor_scores: {factor_scores}")  # デバッグ出力
    return factor_scores

# Streamlitアプリの実行
def main():
    st.title("ストレスレベル計測アプリ")

    # データを収集した際の質問項目
    features = [
        "extracurricular activities (課外活動)",
        "peer pressure (仲間からのプレッシャー)",
        "study load (学業負担)",
        "future career concerns (将来のキャリアに関する懸念)",
        "depression (うつ病)",
        "noise level (騒音レベル)",
        "bullying (いじめ)",
        "self-esteem (自尊心)",
        "headache (頭痛)",
        "mental health history (精神保健の歴史)",
        "breathing problems (呼吸問題)",
        "teacher-student relationships (教師と学生の関係)",
        "academic performance (学業成績)",
        "safety (安全性)",
        "basic needs (基本的ニーズ)",
        "sleep quality (睡眠の質)",
        "living conditions (生活環境)"
    ]

    # 各質問項目の因子負荷量
    factor_loadings = np.array([
        [0.760, -0.035],
        [0.730, -0.071],
        [0.641, -0.071],
        [0.571, -0.309],
        [0.561, -0.298],
        [0.537, -0.189],
        [0.493, -0.370],
        [-0.458, 0.389],
        [0.427, -0.383],
        [0.427, -0.347],
        [0.352, -0.319],
        [-0.078, 0.760],
        [-0.092, 0.728],
        [-0.086, 0.727],
        [-0.107, 0.696],
        [-0.377, 0.483],
        [-0.272, 0.420]
    ])

    st.write("以下のラジオボタンで各項目を評価し、ストレスレベルを計算します。")

    user_input = get_user_input(features)

    st.write("入力された値:", user_input)

    # 逆スコアリングを適用するインデックス
    reverse_indices = [7, 15]  # 7: Self-esteem, 15: Sleep quality
    user_input = reverse_scoring(user_input, reverse_indices)

    st.write("逆スコアリング適用後の値:", user_input)

    scaled_values = min_max_scaling(user_input)

    st.write("Min-Max正規化された値:", scaled_values)

    factor_scores = calculate_factor_scores(scaled_values, factor_loadings)

    st.write("因子スコア (Factor 1, Factor 2):", factor_scores)

    st.write("以下は、ストレスレベルをレーダーチャートで視覚化したものです。")
    fig = px.line_polar(
        r=scaled_values + scaled_values[:1],  # 周期的に閉じるために、最初の値を最後に追加
        theta=features + features[:1],  # 周期的に閉じるために、最初の項目を最後に追加
        line_close=True,
        title="ストレスレベル",
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
