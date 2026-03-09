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
    
    # 검색 로직 (랜덤 로딩 문구 적용)
    with st.spinner(random.choice(messages)):
        search_term = search_input.strip().upper()
        mask = target_columns.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        results = df[mask].copy()
    
    if not results.empty:
        # 검색 결과 출력
        results.index = range(1, len(results) + 1)
        results.index.name = '순번'
        st.success(f"✅ 총 {len(results)}건의 결과를 찾았습니다.")
        st.dataframe(results, use_container_width=True)
        st.info("💡 행을 클릭하면 상세 내용을 확인하거나 복사할 수 있습니다.")
    else:
        # 자료가 없을 경우 직원들을 위한 안내
        st.warning(f"🧐 검색하신 형번 '{search_input}'이 데이터베이스에 없습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            # 지정하신 게시판 링크로 연결되는 버튼
            request_url = "https://www.dmbrg.kr/bbs/write.php?bo_table=request"
            st.link_button("📝 담당자에게 자료 요청하기", request_url)
        with col2:
            # 검색어 초기화 및 재시도
            if st.button("🔄 다시 검색하기"):
                st.rerun()
            
        # 추가 안내 사항
        st.markdown(f"""
        ---
        **검색 결과가 나오지 않나요?**
        1. 입력하신 **'{search_input}'**에 오타가 없는지 확인해 보세요.
        2. 접미사(ZZ, DDU 등)를 제외하고 **기본 숫자**만으로 검색해 보세요.
        3. 신규 형번이거나 특수 베어링인 경우 위 버튼을 눌러 **동명베어링 자료요청 게시판**에 글을 남겨주세요.
        * 문의 이메일: dmbrg0035@naver.com
        """)