import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("📊 CSV 기반 데이터 분석 및 시각화 도우미")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV 파일 업로드 완료!")

    # 데이터 기본 정보 출력
    st.subheader("🔍 기본 정보")
    st.write(df.head())

    # 수치형 컬럼 자동 감지
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # 📊 시각화
    st.subheader("📈 시각화: 히스토그램/상자 그림")
    selected_column = st.selectbox("분석할 수치형 컬럼을 선택하세요", numeric_columns)

    # 히스토그램
    fig, ax = plt.subplots()
    sns.histplot(df[selected_column], kde=True, ax=ax)
    st.pyplot(fig)

    # 박스플롯
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df[selected_column], ax=ax2)
    st.pyplot(fig2)

    # 🔍 조건별 필터링
    st.subheader("🧮 조건별 데이터 필터링")
    condition_column = st.selectbox("조건을 적용할 컬럼 선택", numeric_columns)
    threshold = st.slider(f"{condition_column} 최소값 필터", int(df[condition_column].min()), int(df[condition_column].max()))
    filtered_df = df[df[condition_column] >= threshold]
    st.write(f"🔎 {condition_column}이 {threshold} 이상인 데이터:")
    st.write(filtered_df)

    # 🤖 GPT 요약 분석
    st.subheader("🤖 GPT로 분석하기")
    if st.button("GPT에게 필터링된 데이터 요약 요청"):
        data_sample = filtered_df.head(10).to_csv(index=False)

        prompt = f"""
        아래는 학생 데이터의 일부입니다. 각 컬럼은 이름, 수학, 영어, 과학 점수, 결석일수를 나타냅니다.
        이 데이터를 기반으로 성적 경향이나 이상치가 있는 학생을 찾아 요약해 주세요.

        데이터:
        {data_sample}
        """

        with st.spinner("GPT가 분석 중입니다..."):
            response = client.chat.completions.create(
                model="gpt-4",  # 또는 "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "당신은 교육 데이터를 분석하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown("### 📘 GPT 분석 결과")
            st.write(reply)
