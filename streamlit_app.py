import streamlit as st
import numpy as np
import plotly.express as px

# 翻訳辞書を定義
translations = {
    "日本語": {
        "title": "メンタルヘルス推定アプリ",
        "intro": "以下のラジオボタンで各項目を評価し、ストレスレベルを計算します。",
        "select_language": "使用言語を選択してください",
        "input_values": "入力された値:",
        "reversed_values": "逆スコアリング適用後の値:",
        "scaled_values": "Min-Max正規化された値:",
        "stress_level": "ストレスレベル:",
        "highest_features": "最もストレスが高い要素:",
        "chart_title": "ストレス要素"
    },
    "English": {
        "title": "Mental Health Estimation App",
        "intro": "Evaluate each item using the radio buttons below and calculate the stress level.",
        "select_language": "Select language",
        "input_values": "Input values:",
        "reversed_values": "Values after reverse scoring:",
        "scaled_values": "Min-Max scaled values:",
        "stress_level": "Stress level:",
        "highest_features": "Top stress factors:",
        "chart_title": "Stress Factors"
    }
}

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features, lang):
    user_input = []
    for feature in features:
        user_input.append(st.radio(f"{feature}を選択してください" if lang == "日本語" else f"Select {feature}", options=[1, 2, 3, 4, 5], index=2))
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
    # 使用言語を選択する
    lang = st.selectbox("使用言語を選択してください", ["日本語", "English"])

    # 言語に応じた翻訳を取得
    t = translations[lang]

    st.title(t["title"])

    # データを収集した際の質問項目
    features = [
        "anxiety_level (不安レベル)" if lang == "日本語" else "Anxiety Level",
        "self_esteem (自尊心)" if lang == "日本語" else "Self Esteem",
        "mental_health_history (精神保健の歴史)" if lang == "日本語" else "Mental Health History",
        "depression (うつ病)" if lang == "日本語" else "Depression",
        "headache (頭痛)" if lang == "日本語" else "Headache",
        "sleep_quality (睡眠の質)" if lang == "日本語" else "Sleep Quality",
        "breathing_problem (呼吸問題)" if lang == "日本語" else "Breathing Problem",
        "noise_level (騒音レベル)" if lang == "日本語" else "Noise Level",
        "living_conditions (生活環境)" if lang == "日本語" else "Living Conditions",
        "safety (安全)" if lang == "日本語" else "Safety",
        "basic_needs (基本的ニーズ)" if lang == "日本語" else "Basic Needs",
        "academic_performance (学業成績)" if lang == "日本語" else "Academic Performance",
        "study_load (学業負担)" if lang == "日本語" else "Study Load",
        "teacher_student_relationship (教師と生徒の関係)" if lang == "日本語" else "Teacher-Student Relationship",
        "future_career_concerns (将来のキャリアに関する懸念)" if lang == "日本語" else "Future Career Concerns",
        "peer_pressure (仲間からのプレッシャー)" if lang == "日本語" else "Peer Pressure",
        "extracurricular_activities (課外活動)" if lang == "日本語" else "Extracurricular Activities",
        "bullying (いじめ)" if lang == "日本語" else "Bullying"
    ]

    # 各質問項目の特徴量重要度
    feature_importances = np.array([
        0.063881,  # anxiety_level
        0.074731,  # self_esteem
        0.084334,  # mental_health_history
        0.043206,  # depression
        0.066067,  # headache
        0.083017,  # sleep_quality
        0.015290,  # breathing_problem
        0.038964,  # noise_level
        0.020777,  # living_conditions
        0.061408,  # safety
        0.047875,  # basic_needs
        0.068805,  # academic_performance
        0.025424,  # study_load
        0.057318,  # teacher_student_relationship
        0.065572,  # future_career_concerns
        0.050163,  # peer_pressure
        0.058846,  # extracurricular_activities
        0.074321   # bullying
    ])

    st.write(t["intro"])

    user_input = get_user_input(features, lang)

    st.write(t["input_values"], user_input)

    # 逆スコアリングを適用するインデックス
    reverse_indices = [1, 16]  # 1: self_esteem, 16: extracurricular_activities
    user_input = reverse_scoring(user_input, reverse_indices)

    st.write(t["reversed_values"], user_input)

    scaled_values = min_max_scaling(user_input)

    st.write(t["scaled_values"], scaled_values)

    stress_level = calculate_stress_level(scaled_values, feature_importances)

    st.write(t["stress_level"], stress_level)

    highest_features = find_top_highest_features(scaled_values, features, top_n=3)
    st.write(t["highest_features"])
    for feature, value in highest_features:
        st.write(f"{feature}: {value}")

    st.write(t["chart_title"])
    fig = px.line_polar(
        r=scaled_values + scaled_values[:1],  # 周期的に閉じるために、最初の値を最後に追加
        theta=features + features[:1],  # 周期的に閉じるために、最初の項目を最後に追加
        line_close=True,
        title=t["chart_title"],
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
