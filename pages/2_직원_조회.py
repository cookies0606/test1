import streamlit as st
import pandas as pd
from db.database import SessionLocal
from db.models import Employee

st.title("직원 조회")

db = SessionLocal()
employees = db.query(Employee).all()

# 데이터프레임 변환
data = [{
    "ID": emp.id,
    "이름": emp.name,
    "부서": emp.department,
    "입사일": emp.hire_date.strftime("%Y-%m-%d"),
    "연락처": emp.phone
} for emp in employees]

df = pd.DataFrame(data)

search_name = st.text_input("이름 검색")
if search_name:
    df = df[df["이름"].str.contains(search_name)]

st.dataframe(df)

db.close()
