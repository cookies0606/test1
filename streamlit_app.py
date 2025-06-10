import streamlit as st
from db.database import init_db

# 앱 최초 실행 시 DB 테이블 생성
init_db()

st.set_page_config(page_title="인사 관리 시스템", layout="wide")

st.title("👥 인사 관리 시스템")
st.markdown("왼쪽 사이드바에서 관리할 항목을 선택하세요.")
