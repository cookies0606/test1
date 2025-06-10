import streamlit as st
from datetime import date
from db.database import SessionLocal
from db.models import Employee, LeaveRequest

db = SessionLocal()
st.title("🌴 연차 신청")

# 예시: 로그인 사용자 정보
employee_id = st.session_state.get("user_id", 1)
is_admin = st.session_state.get("is_admin", False)

# 연차 신청 폼
with st.form("leave_form"):
    leave_date = st.date_input("연차 날짜", value=date.today())
    reason = st.text_area("사유")
    submit = st.form_submit_button("신청하기")
    if submit:
        new_leave = LeaveRequest(
            employee_id=employee_id,
            date=leave_date,
            reason=reason
        )
        db.add(new_leave)
        db.commit()
        st.success(f"{leave_date} 연차 신청 완료")

# 신청 이력 표시
st.subheader("📋 연차 신청 내역")
if is_admin:
    # 관리자: 전체 신청 보기
    requests = db.query(LeaveRequest).all()
else:
    # 일반 직원: 본인 신청만
    requests = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee_id
    ).all()

for req in requests:
    emp_name = db.query(Employee).get(req.employee_id).name
    with st.expander(f"{req.date} | {emp_name} | 상태: {req.status}"):
        st.write(f"사유: {req.reason}")
        if is_admin and req.status == "대기":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ 승인", key=f"approve_{req.id}"):
                    req.status = "승인"
                    db.commit()
            with col2:
                if st.button("❌ 반려", key=f"reject_{req.id}"):
                    req.status = "반려"
                    db.commit()
