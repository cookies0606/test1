import streamlit as st
from datetime import date
from db.models import Employee

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

engine = create_engine("sqlite:///employees.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# DB 초기화
init_db()

st.title("직원 등록")

with st.form("employee_form"):
    name = st.text_input("이름")
    department = st.selectbox("부서", ["개발", "인사", "영업", "기획"])
    hire_date = st.date_input("입사일", value=date.today())
    phone = st.text_input("연락처")
    submitted = st.form_submit_button("등록하기")

    if submitted:
        db = SessionLocal()
        new_employee = Employee(
            name=name,
            department=department,
            hire_date=hire_date,
            phone=phone
        )
        db.add(new_employee)
        db.commit()
        db.close()
        st.success(f"{name} 님이 등록되었습니다.")
