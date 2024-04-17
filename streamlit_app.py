import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# データの読み込み
data = pd.read_csv("stress_data.csv")

# 特徴量とターゲットを分割
X = data.drop(columns=["stress_level"])
y = data["stress_level"]

# モデルの作成
model = RandomForestClassifier()
model.fit(X, y)

# 特徴量の重要度を取得
feature_importances = model.feature_importances_

# Streamlitアプリケーションの作成
st.title("Stress Level Predictor")

# 特徴量の重要度を表示
st.write("Feature Importances:")
st.bar_chart(feature_importances)

# 特徴量の入力欄を作成
feature_inputs = {}
for feature in X.columns:
    feature_inputs[feature] = st.slider(f"Enter {feature}", min_value=data[feature].min(), max_value=data[feature].max())

# 予測の実行
prediction = model.predict(pd.DataFrame([feature_inputs]))

# 予測結果の表示
st.write("Predicted Stress Level:", prediction[0])
