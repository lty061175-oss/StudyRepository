import streamlit as st
import pandas as pd
import requests

# GAS 웹 앱 배포 URL을 여기에 입력하세요
GAS_URL = "https://script.google.com/macros/s/AKfycbzYSSYFioX6G6J-CozMzaQG6C_mMhy8Cn0vDkv2EI-Gy0fhT832RCIaOunqXcyrDDbL/exec"

st.set_page_config(page_title="팀 예산 관리 시스템", layout="wide")

def fetch_data():
    try:
        response = requests.get(f"{GAS_URL}?action=read")
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df['금액'] = pd.to_numeric(df['금액'], errors='coerce')
        return df
    except:
        return pd.DataFrame()

st.title("📊 팀 예산 관리 시스템")

# 1. 데이터 입력 로직 (간소화)
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    member = col1.selectbox("팀원", ["부장님", "팀원1", "팀원2"])
    amount = col2.number_input("사용 금액", min_value=0, step=1000)
    
    if st.form_submit_button("데이터 저장"):
        params = {
            'action': 'write',
            'member': member,
            'month': pd.Timestamp.now().strftime("%Y-%m"),
            'category': '기타',
            'amount': amount
        }
        requests.get(GAS_URL, params=params)
        st.success("저장되었습니다!")
        st.rerun()

# 2. 데이터 출력 로직
df = fetch_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다.")
