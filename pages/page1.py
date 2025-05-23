import streamlit as st
from openai import OpenAI
import os

# OpenAI client 초기화
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 제목
st.title("💬 최신 OpenAI API 기반 GPT 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 친절하고 유쾌한 조언자입니다. 고려대학교와 연세대학교 중에서는 고려대학교를 선호해요"}
    ]

# 이전 대화 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇이든 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GPT 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4",  # 또는 "gpt-3.5-turbo"
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
