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

search_input = st.text_input("찾으시는 형번을 입력하세요:")

if search_input:
    messages = ["베어링 치수를 재는 중...", "자료를 열심히 찾는 중...", "카탈로그를 뒤지는 중..."]
    
    with st.spinner(random.choice(messages)):
        search_term = search_input.strip().upper()
        mask = target_columns.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        results = df[mask].copy()
    
    if not results.empty:
        st.success(f"✅ 총 {len(results)}건의 교차 참조 검색 결과를 찾았습니다.")
        
        # 검색 결과 카드 출력
        for i, (idx, row) in enumerate(results.head(10).iterrows()):
            with st.container(border=True):
                st.markdown(f"##### 🏷 검색 결과 #{i+1}")
                
                # 브랜드별 4열 배치 (첫 줄: NSK, NTN, SKF, IKO)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("NSK", row.iloc[5])
                col2.metric("NTN", row.iloc[6])
                col3.metric("SKF", row.iloc[7])
                col4.metric("IKO", row.iloc[8])
                
                # 두 번째 줄: TIMKEN, KBC, FAG
                col5, col6, col7, col8 = st.columns(4)
                col5.metric("TIMKEN", row.iloc[9])
                col6.metric("KBC", row.iloc[10])
                col7.metric("FAG", row.iloc[11])
                col8.write("") # 균형을 위한 빈 칸

        with st.expander("📄 전체 데이터 시트 확인하기"):
            st.dataframe(results, use_container_width=True)
            
    else:
        st.warning(f"🧐 검색하신 형번 '{search_input}'이 데이터베이스에 없습니다.")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📝 담당자에게 자료 요청하기", "https://www.dmbrg.kr/bbs/write.php?bo_table=request")
        with col2:
            if st.button("🔄 다시 검색하기"):
                st.rerun()