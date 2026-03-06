import streamlit as st
import pandas as pd
import random
import time

# 페이지 설정
st.set_page_config(page_title="베어링 형번 검색", layout="wide")

# 제목 및 안내 문구
st.title("⚙️ 베어링 형번 검색")
st.caption("베어링 자료를 추가 중입니다.")

@st.cache_data
def load_data():
    # 데이터 파일 불러오기
    df = pd.read_csv("Bearing Cross Reference.csv")
    return df

# 데이터 로드
df = load_data()

# 검색 범위 설정 (F열~L열)
target_columns = df.iloc[:, 5:12] 

# 검색창
search_input = st.text_input("찾으시는 형번을 입력하세요:")

if search_input:
    # 랜덤 로딩 문구 리스트
    messages = [
        "베어링 치수를 재는 중...",
        "자료를 열심히 찾는 중...",
        "카탈로그를 뒤지는 중...",
        "베어링 사양을 확인 중..."
    ]

    with st.spinner(random.choice(messages)):
        time.sleep(1) # [테스트용] 1초간 강제로 멈추게 하여 문구를 확인해 보세요
        
        search_term = search_input.strip().upper()
        # ... (이하 동일)
    
    # 검색 로직 (랜덤 로딩 문구 적용)
    with st.spinner(random.choice(messages)):
        search_term = search_input.strip().upper()
        mask = target_columns.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        results = df[mask].copy()
    
    if not results.empty:
        # 검색 결과 출력
        results.index = range(1, len(results) + 1)
        results.index.name = '순번'
        st.success(f"총 {len(results)}건의 결과를 찾았습니다.")
        st.dataframe(results, use_container_width=True)
    else:
        st.error("일치하는 형번이 없습니다.")