import streamlit as st
import pandas as pd
import requests

# 1. Apps Script에서 배포 후 생성된 웹 앱 URL을 여기에 입력하세요
GAS_URL = "https://script.google.com/macros/s/AKfycbzYSSYFioX6G6J-CozMzaQG6C_mMhy8Cn0vDkv2EI-Gy0fhT832RCIaOunqXcyrDDbL/exec"

st.set_page_config(page_title="팀 예산 관리", layout="centered")
st.title("📊 팀 예산 관리 시스템")

# 데이터 로드 함수 (code.gs의 'read' 액션 호출)
@st.cache_data(ttl=60)
def fetch_data():
    try:
        response = requests.get(f"{GAS_URL}?action=read")
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        # 첫 번째 행을 헤더로 설정
        df = pd.DataFrame(data[1:], columns=data[0])
        # 금액 데이터 처리
        if '금액' in df.columns:
            df['금액'] = pd.to_numeric(df['금액'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 데이터 입력 폼 (code.gs의 'write' 액션 호출)
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    member = col1.selectbox("팀원", ["부장님", "팀원1", "팀원2", "팀원3", "팀원4"])
    category = col2.selectbox("항목", ["수선유지비", "비품", "개량공사"])
    amount = st.number_input("사용 금액 (원)", min_value=0, step=1000)
    
    if st.form_submit_button("기록 저장"):
        params = {
            'action': 'write',
            'member': member,
            'month': pd.Timestamp.now().strftime("%Y-%m"),
            'category': category,
            'amount': amount
        }
        try:
            response = requests.get(GAS_URL, params=params)
            if response.status_code == 200:
                st.success("데이터가 성공적으로 저장되었습니다!")
                st.rerun() 
            else:
                st.error("저장에 실패했습니다. URL을 확인하세요.")
        except Exception as e:
            st.error(f"통신 오류: {e}")

# 데이터 표시
st.divider()
st.subheader("📋 최근 입력 내역")
df = fetch_data()

if not df.empty:
    # 최신 데이터 상단 정렬
    st.dataframe(df.sort_values(by=df.columns[0], ascending=False), use_container_width=True)
else:
    st.info("데이터가 없습니다.")
