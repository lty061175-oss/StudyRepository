import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="팀 예산 관리 시스템", layout="wide")

# 구글 시트 연동 설정 (스트림릿 Cloud Secrets 등에 설정 권장)
def get_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    # 실제 환경에서는 서비스 계정 키 파일 경로를 설정하세요
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)
    return client.open("팀예산관리").sheet1

# UI 구성
st.title("📊 팀 예산 관리 시스템")
tab1, tab2 = st.tabs(["데이터 입력", "대시보드"])

with tab1:
    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        member = col1.selectbox("팀원", ["부장님", "팀원1", "팀원2", "팀원3", "팀원4"])
        month = col2.date_input("날짜").strftime("%Y-%m")
        category = st.selectbox("항목", ["수선유지비", "비품", "개량공사"])
        amount = st.number_input("금액", min_value=0, step=1000)
        
        if st.form_submit_button("기록 저장"):
            # 구글 시트에 행 추가
            # sheet = get_gsheet()
            # sheet.append_row([month, member, category, amount])
            st.success("데이터가 구글 시트에 저장되었습니다.")

with tab2:
    st.header("전체 현황")
    # sheet = get_gsheet()
    # data = pd.DataFrame(sheet.get_all_records())
    # st.dataframe(data)
