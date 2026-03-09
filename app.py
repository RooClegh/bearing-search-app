import streamlit as st
import pandas as pd
import random

# 페이지 설정
st.set_page_config(page_title="베어링 형번 검색", layout="wide")

# 제목 및 안내 문구
st.title("⚙️ 베어링 형번 검색")
st.caption("베어링 자료를 추가 중입니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("Bearing Cross Reference.csv")
    return df

df = load_data()

# 검색 범위 설정 (F열~L열)
target_columns = df.iloc[:, 5:12] 

# 검색창
search_input = st.text_input("찾으시는 형번을 입력하세요:")

if search_input:
    messages = [
        "베어링 치수를 재는 중...",
        "자료를 열심히 찾는 중...",
        "카탈로그를 뒤지는 중...",
        "베어링 사양을 확인 중..."
    ]
    
    with st.spinner(random.choice(messages)):
        search_term = search_input.strip().upper()
        mask = target_columns.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        results = df[mask].copy()
    
    # --- 여기서부터 들여쓰기가 중요합니다 ---
    if not results.empty:
        results.index = range(1, len(results) + 1)
        results.index.name = '순번'
        st.success(f"✅ 총 {len(results)}건의 결과를 찾았습니다.")
        st.dataframe(results, use_container_width=True)
        st.info("💡 행을 클릭하면 상세 내용을 확인하거나 복사할 수 있습니다.")
    else:
        st.warning("🧐 검색하신 형번이 데이터베이스에 없습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            email_link = "mailto:dmbrg0035@naver.com?subject=[베어링 형번 문의] 자료 없음"
            st.link_button("📧 담당자에게 이메일 문의하기", email_link)
        with col2:
            if st.button("🔄 다시 검색하기"):
                st.rerun()
            
        st.markdown(f"""
        ---
        **검색 팁 (자료가 나오지 않을 때):**
        1. **'{search_input}'**의 오타가 없는지 확인해 보세요.
        2. 접미사(ZZ, DDU 등)를 제외하고 **기본 숫자**만으로 검색해 보세요.
        3. 신규 형번이거나 특수 베어링인 경우 이메일(**dmbrg0035@naver.com**)로 문의해 주세요.
        """)