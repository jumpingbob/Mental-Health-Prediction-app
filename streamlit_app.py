pip install streamlit
import streamlit as st

# 曜日ごとの時間割を定義（例として平日の時間割を作成）
timetable = {
    "月曜日": ["数学", "国語", "英語"],
    "火曜日": ["体育", "理科", "音楽"],
    "水曜日": ["国語", "社会", "数学"],
    "木曜日": ["美術", "技術", "保健体育"],
    "金曜日": ["英語", "数学", "家庭科"]
}

# Streamlitアプリの設定
st.title("時間割アプリ")

# 曜日の選択
selected_day = st.selectbox("曜日を選択してください", list(timetable.keys()))

# 選択された曜日の時間割を表示
st.write(f"【{selected_day}の時間割】")
for subject in timetable[selected_day]:
    st.write(f"- {subject}")

streamlit run timetable_app.py
