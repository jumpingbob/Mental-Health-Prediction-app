import streamlit as st
import numpy as np
import plotly.express as px

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features):
    user_input = []
    for feature in features:
        user_input.append(st.radio(f"{feature}を選択してください", options=[1, 2, 3, 4, 5], index=2))
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
    st.title("メンタルヘルス推定アプリ")

    # データを収集した際の質問項目
    features = [
        "anxiety_level (不安レベル)",
        "self_esteem (自尊心)",
        "mental_health_history (精神保健の歴史)",
        "depression (うつ病)",
        "headache (頭痛)",
        "blood_pressure (血圧)",
        "breathing_problem (呼吸問題)",
        "noise_level (騒音レベル)",
        "study_load (学業負担)",
        "future_career_concerns (将来のキャリアに関する懸念)",
        "social_support (社会的支援)",
        "peer_pressure (仲間からのプレッシャー)",
        "extracurricular_activities (課外活動)",
        "bullying (いじめ)"
    ]

    # 各質問項目の特徴量重要度
    feature_importances = np.array([
        0.050119,  # anxiety_level
        0.078640,  # self_esteem
        0.089115,  # mental_health_history
        0.062141,  # depression
        0.092308,  # headache
        0.088636,  # blood_pressure
        0.023618,  # breathing_problem
        0.056271,  # noise_level
        0.050188,  # study_load
        0.085528,  # future_career_concerns
        0.102331,  # social_support
        0.050649,  # peer_pressure
        0.079034,  # extracurricular_activities
        0.091422   # bullying
    ])

    st.write("以下のラジオボタンで各項目を評価し、ストレスレベルを計算します。")

    user_input = get_user_input(features)

    st.write("入力された値:", user_input)

    # 逆スコアリングを適用するインデックス
    reverse_indices = [1, 12]  # 1: self_esteem, 12: extracurricular_activities
    user_input = reverse_scoring(user_input, reverse_indices)

    st.write("逆スコアリング適用後の値:", user_input)

    scaled_values = min_max_scaling(user_input)

    st.write("Min-Max正規化された値:", scaled_values)

    stress_level = calculate_stress_level(scaled_values, feature_importances)

    st.write("ストレスレベル:", stress_level)

    highest_features = find_top_highest_features(scaled_values, features, top_n=3)
    st.write("最もストレスが高い要素:")
    for feature, value in highest_features:
        st.write(f"{feature}: {value}")

    st.write("以下は、ストレス要素をレーダーチャートで視覚化したものです。")
    fig = px.line_polar(
        r=scaled_values + scaled_values[:1],  # 周期的に閉じるために、最初の値を最後に追加
        theta=features + features[:1],  # 周期的に閉じるために、最初の項目を最後に追加
        line_close=True,
        title="ストレス要素",
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
