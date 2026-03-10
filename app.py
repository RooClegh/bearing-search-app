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

df = load_data()

# 검색 범위 설정 (F열~L열: NSK, NTN, SKF, IKO, TIMKEN, KBC, FAG)
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
        search_term = search_input.strip().upper()
        # 대소문자 구분 없이 F~L열에서 검색
        mask = target_columns.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        results = df[mask].copy()
    
    if not results.empty:
        st.success(f"✅ 총 {len(results)}건의 교차 참조 결과를 찾았습니다.")
        
        # 상단 결과를 카드 형태로 출력
        for i, (idx, row) in enumerate(results.head(10).iterrows()):
            with st.container(border=True):
                st.markdown(f"##### 🏷 검색 결과 #{i+1}")
                
                # 브랜드 리스트 정의
                brands = ["NSK", "NTN", "SKF", "IKO", "TIMKEN", "KBC", "FAG"]
                
                # 4열 배치로 균등하게 시각화
                cols = st.columns(4)
                for j, brand in enumerate(brands):
                    col_idx = j % 4
                    # 브랜드명은 작고 굵게, 형번은 아래에 표시
                    cols[col_idx].markdown(f"**{brand}** \n{row.iloc[5 + j]}")

        # 상세 데이터 시트 (필요할 때만 확인)
        with st.expander("📄 전체 데이터 시트 확인하기 (전체 열 포함)"):
            st.dataframe(results, use_container_width=True)
            
    else:
        # 자료가 없을 경우 안내 및 문의 링크
        st.warning(f"🧐 검색하신 형번 '{search_input}'이 데이터베이스에 없습니다.")
        col1, col2 = st.columns(2)
        with col1:
            # 공식 자료요청 게시판 링크
            st.link_button("📝 담당자에게 자료 요청하기", "https://www.dmbrg.kr/bbs/write.php?bo_table=request")
        with col2:
            if st.button("🔄 다시 검색하기"):
                st.rerun()

        st.markdown(f"""
        ---
        **검색 팁:**
        1. **'{search_input}'**의 오타를 확인해 보세요.
        2. 접미사를 제외한 **기본 숫자**만으로 검색해 보세요. (예: 6204ZZ ➔ 6204)
        """)