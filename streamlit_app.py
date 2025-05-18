import streamlit as st
import random

# 페이지 제목
st.title("🎲 주사위 시뮬레이션 (여러 개)")

# 설명 텍스트
st.write("주사위의 개수를 선택한 후, 버튼을 누르면 해당 개수만큼 주사위를 던지고 평균을 계산합니다.")

# 주사위 개수 선택 슬라이더
num_dice = st.slider("주사위 개수 선택", min_value=1, max_value=1000, value=10)

# 버튼
if st.button("주사위 굴리기"):
    results = [random.randint(1, 6) for _ in range(num_dice)]
    average = sum(results) / num_dice

    st.write(f"총 {num_dice}개의 주사위를 굴렸습니다.")
    st.write(f"주사위 값들의 평균: **{average:.2f}**")

    # 선택적으로 결과 값 일부 보여주기
    if num_dice <= 20:
        st.write("굴린 주사위 값:", results)
else:
    st.write("🎯 먼저 주사위 개수를 정하고, 버튼을 눌러 주세요!")
