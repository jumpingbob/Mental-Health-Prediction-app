import streamlit as st
import numpy as np
import plotly.express as px

# ユーザーからの入力を受け取り、それぞれの項目の値をリストに格納する
def get_user_input(features):
    user_input = []
    options = ["5.とても高い", "4.やや高い", "3.ふつう", "2.やや低い", "1.とても低い"]
    for feature in features:
        user_input.append(int(st.radio(f"**{feature}**の高さを選択してください", options=options, index=2, key=feature)[0]))  # 文字列の最初の文字を数値に変換
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
    
    if min_val == max_val:
        # すべての値が同じ場合、すべてのスケーリング値を0.5に設定
        scaled_values = [0.5 for _ in user_input]
    else:
        scaled_values = [(x - min_val) / (max_val - min_val) for x in user_input]
   
    return scaled_values

# ストレスレベルを計算
def calculate_stress_level(scaled_values, feature_importances):
    stress_level = np.dot(scaled_values, feature_importances)
   
    return stress_level

# 最も高い項目を特定する
def find_top_highest_features(scaled_values, features, top_n=3):
    sorted_indices = np.argsort(scaled_values)[-top_n:][::-1]
    highest_features = [(features[i], scaled_values[i]) for i in sorted_indices]
    return highest_features

# Streamlitアプリの実行
def main():
    st.title("メンタルヘルスセルフチェッカー")

    st.write("以下のラジオボタンで各項目を評価し、ストレスレベルおよびストレス要因を推定します。")
    st.markdown("直感的にあてはまる各項目の強さ(大きさ）を選択してください。")

    # データを収集した際の質問項目
    features = [
        "anxiety level (不安レベル)",
        "self-esteem (自尊心の高さ)",
        "depression (うつ傾向)",
        "headache (頭痛の強度)",
        "sleep quality (睡眠の質)",
        "breathing problem (呼吸の苦しさ・息苦しさ)",
        "noise level (騒音レベル)",
        "living conditions (生活環境・状態)",
        "safety (安全性)",
        "basic needs (基本的欲求)",
        "academic performance (学業成績)",
        "study load (学業負担)",
        "teacher-student relationship (教師と生徒の関係)",
        "future career concerns (将来のキャリア・進路に関する懸念)",
        "peer pressure (仲間からのプレッシャー)",
        "extracurricular activities (課外活動における負担)",
        "bullying (外部からの圧力的な被害)"
    ]

    # 各質問項目の特徴量重要度
    feature_importances = np.array([
        0.057802,  # anxiety level
        0.057088,  # self-esteem
        0.039464,  # depression
        0.081881,  # headache
        0.088141,  # sleep quality
        0.023011,  # breathing problem
        0.042920,  # noise level
        0.026199,  # living conditions
        0.056138,  # safety
        0.072368,  # basic needs
        0.075147,  # academic performance
        0.035174,  # study load
        0.051709,  # teacher-student relationship
        0.067962,  # future career concerns
        0.048509,  # peer pressure
        0.074542,  # extracurricular activities
        0.101947   # bullying
    ])

    user_input = get_user_input(features)

    # 逆スコアリングを適用するインデックス
    reverse_indices = [1, 4, 7, 8, 9, 10, 12]  # 1: self-esteem, 4: sleep quality, 7: living conditions, 8: safety, 9: basic needs, 10: academic performance, 12: teacher-student relationship
    user_input = reverse_scoring(user_input, reverse_indices)

    scaled_values = min_max_scaling(user_input)

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
