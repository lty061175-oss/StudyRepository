import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(page_title="팀 예산 관리 시스템", layout="wide")

def get_gsheet():
    try:
        creds_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client.open("팀예산관리").sheet1
    except Exception as e:
        st.error(f"구글 시트 연결 실패: {e}")
        return None

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
            sheet = get_gsheet()
            if sheet:
                try:
                    sheet.append_row([month, member, category, amount])
                    st.success("데이터가 구글 시트에 저장되었습니다.")
                except Exception as e:
                    st.error(f"데이터 저장 실패: {e}")

with tab2:
    st.header("전체 현황")
    sheet = get_gsheet()
    if sheet:
        try:
            data = pd.DataFrame(sheet.get_all_records())
            st.dataframe(data)
        except Exception as e:
            st.error(f"데이터 로드 실패: {e}")
