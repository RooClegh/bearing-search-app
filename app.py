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
        st.success(f"✅ 총 {len(results)}건의 결과를 찾았습니다.")
        
        # 브랜드 리스트와 인덱스 매핑
        brands = ["NSK", "NTN", "SKF", "IKO", "TIMKEN", "KBC", "FAG"]
        
        for i, (idx, row) in enumerate(results.head(10).iterrows()):
            with st.container(border=True):
                st.markdown(f"##### 🏷 검색 결과 #{i+1}")
                
                # 1. 카드 레이아웃: 데이터가 있는 브랜드만 추출
                available_info = []
                for j, brand in enumerate(brands):
                    val = row.iloc[5 + j]
                    # 값이 존재하고 (NaN이 아님), 빈 문자열이 아니며, '-' 가 아닌 경우만 추가
                    if pd.notna(val) and str(val).strip() not in ["", "-"]:
                        available_info.append((brand, val))
                
                # 데이터가 있는 것들만 가로로 배치
                if available_info:
                    cols = st.columns(len(available_info) if len(available_info) < 5 else 4)
                    for idx, (b_name, b_val) in enumerate(available_info):
                        col_target = cols[idx % len(cols)]
                        col_target.markdown(f"**{b_name}** \n{b_val}")
                else:
                    st.write("상세 형번 정보가 없습니다.")

        # 2. 표 레이아웃: 모든 브랜드를 한꺼번에 확인 (빈칸 포함)
        with st.expander("📄 전체 데이터 시트 확인하기 (모든 브랜드 포함)"):
            st.dataframe(results, use_container_width=True)
            
    else:
        st.warning(f"🧐 검색하신 형번 '{search_input}'이 데이터베이스에 없습니다.")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📝 담당자에게 자료 요청하기", "https://www.dmbrg.kr/bbs/write.php?bo_table=request")
        with col2:
            if st.button("🔄 다시 검색하기"):
                st.rerun()