import streamlit as st
import numpy as np
import plotly.express as px

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features):
    user_input = []
    for feature in features:
        user_input.append(st.radio(f"{feature}を選択してください", options=[5, 4, 3, 2, 1], index=2, key=feature))
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

# ストレスレベルを計算
def calculate_stress_level(scaled_values, feature_importances):
    stress_level = np.dot(scaled_values, feature_importances)
    st.write(f"stress_level: {stress_level}")  # デバッグ出力
    return stress_level

# 最も高い項目を特定する
def find_top_highest_features(scaled_values, features, top_n=3):
    sorted_indices = np.argsort(scaled_values)[-top_n:][::-1]
    highest_features = [(features[i], scaled_values[i]) for i in sorted_indices]
    return highest_features

# Streamlitアプリの実行
def main():
    st.title("メンタルヘルスセルフチェックアプリ")

    # セッション状態を初期化
    if 'user_inputs' not in st.session_state:
        st.session_state.user_inputs = []

    # 精神疾患の有無に関する質問
    #mental_health_history = st.radio("精神疾患が以前あったことがありますか？", options=["はい", "いいえ"], index=1, key='mental_health_history')

    st.write("以下のラジオボタンで各項目を評価し、ストレスレベルおよびストレス要因を推定します。")
    st.write("直感的にあてはまるものを選択してください。")

    # データを収集した際の質問項目
    features = [
        "anxiety level (不安レベル)",
        "self-esteem (自尊心)",
        "depression (うつ病)",
        "headache (頭痛)",
        "sleep quality (睡眠の質)",
        "breathing problem (呼吸問題)",
        "noise level (騒音レベル)",
        "living conditions (生活環境)",
        "safety (安全)",
        "basic needs (基本的ニーズ)",
        "academic performance (学業成績)",
        "study load (学業負担)",
        "teacher-student relationship (教師と生徒の関係)",
        "future career concerns (将来のキャリアに関する懸念)",
        "peer pressure (仲間からのプレッシャー)",
        "extracurricular activities (課外活動)",
        "bullying (いじめ)"
    ]

    # 各質問項目の特徴量重要度
    feature_importances = np.array([
        0.063881,  # anxiety level
        0.074731,  # self-esteem
        0.043206,  # depression
        0.066067,  # headache
        0.083017,  # sleep quality
        0.015290,  # breathing problem
        0.038964,  # noise level
        0.020777,  # living conditions
        0.061408,  # safety
        0.047875,  # basic needs
        0.068805,  # academic performance
        0.025424,  # study load
        0.057318,  # teacher-student relationship
        0.065572,  # future career concerns
        0.050163,  # peer pressure
        0.058846,  # extracurricular activities
        0.074321   # bullying
    ])

    user_input = get_user_input(features)

    st.session_state.user_inputs = user_input  # 入力データをセッション状態に保存

    st.write("入力された値:", st.session_state.user_inputs)

    # 逆スコアリングを適用するインデックス
    reverse_indices = [1, 4, 7, 8, 9, 10, 12]  # 1: self-esteem, 4: sleep quality, 7: living conditions, 8: safety, 9: basic needs, 10: academic performance, 12: teacher-student relationship
    user_input = reverse_scoring(st.session_state.user_inputs, reverse_indices)

    st.write("Values after applying reverse scoring:", user_input)

    scaled_values = min_max_scaling(user_input)

    st.write("Min-Max normalized values:", scaled_values)

    stress_level = calculate_stress_level(scaled_values, feature_importances)

    stress_level_rounded = round(stress_level, 2)  # 小数第二位まで四捨五入

    st.write("ストレスレベル:", stress_level_rounded)

    highest_features = find_top_highest_features(scaled_values, features, top_n=3)
    st.write("ストレス要因上位3項目:")
    for feature, value in highest_features:
        st.write(f"{feature}: {value}")

    st.write("以下は、ユーザーのストレス要因をレーダーチャートで視覚化したものです。")
    fig = px.line_polar(
        r=scaled_values + scaled_values[:1],  # 周期的に閉じるために、最初の値を最後に追加
        theta=features + features[:1],  # 周期的に閉じるために、最初の項目を最後に追加
        line_close=True,
        title="ストレス要因",
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
