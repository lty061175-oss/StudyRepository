import streamlit as st
import pandas as pd
import gspread

# 1. 페이지 설정
st.set_page_config(page_title="팀 예산 관리 시스템", layout="wide")

# 2. 구글 시트 연결 함수
@st.cache_resource
def get_sheet():
    """Secrets에서 인증 정보를 가져와 구글 시트 객체를 반환합니다."""
    secrets = st.secrets["gcp_service_account"]
    client = gspread.service_account_from_dict(dict(secrets))
    # 시트 이름이 '예산데이터시트'인지 확인하세요.
    sheet = client.open("예산데이터시트").sheet1
    return sheet

st.title("📊 팀 예산 관리 시스템")

# 3. 데이터 입력 폼 (사이드바)
with st.sidebar:
    st.header("📝 예산 내역 입력")
    with st.form("budget_form"):
        member = st.selectbox("팀원 선택", ["부장님", "팀원1", "팀원2", "팀원3", "팀원4"])
        month = st.date_input("날짜").strftime("%Y-%m")
        category = st.selectbox("예산 항목", ["수선유지비", "비품", "개량공사"])
        amount = st.number_input("사용 금액 (원)", min_value=0, step=1000)
        
        submit = st.form_submit_button("기록 저장")
        
        if submit:
            try:
                sheet = get_sheet()
                sheet.append_row([month, member, category, amount])
                st.success("데이터가 성공적으로 저장되었습니다!")
            except Exception as e:
                st.error(f"저장 중 오류 발생: {e}")

# 4. 데이터 조회 및 시각화 (메인 화면)
st.header("📂 전체 예산 대시보드")

try:
    sheet = get_sheet()
    data = sheet.get_all_records()
    
    if data:
        df = pd.DataFrame(data)
        
        # 숫자형 변환
        df["금액"] = pd.to_numeric(df["금액"])
        
        st.dataframe(df, use_container_width=True)
        
        # 간단한 대시보드
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("항목별 누적 비용")
            st.bar_chart(df.groupby("항목")["금액"].sum())
            
        with col2:
            st.subheader("팀원별 사용 현황")
            st.bar_chart(df.groupby("팀원")["금액"].sum())
    else:
        st.info("시트에 저장된 데이터가 없습니다.")
        
except Exception as e:
    st.warning("데이터를 불러올 수 없습니다. 구글 시트 권한과 설정을 확인해주세요.")
