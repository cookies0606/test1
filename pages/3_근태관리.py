import streamlit as st
from datetime import datetime, date
from db.database import SessionLocal
from db.models import Employee, Attendance
from sqlalchemy import and_

db = SessionLocal()
st.title("📆 근태 관리")

# 예시: 로그인한 사용자 ID (실제 구현시 로그인 연동 필요)
employee_id = st.session_state.get("user_id", 1)

# 오늘 날짜 확인
today = date.today()

# 오늘 출퇴근 기록 존재 여부 확인
record = db.query(Attendance).filter(
    and_(
        Attendance.employee_id == employee_id,
        Attendance.date == today
    )
).first()

# 출근
if not record:
    if st.button("출근하기"):
        check_in_time = datetime.now().time()
        new_record = Attendance(
            employee_id=employee_id,
            date=today,
            check_in=check_in_time
        )
        db.add(new_record)
        db.commit()
        st.success(f"출근 시간 기록됨: {check_in_time.strftime('%H:%M:%S')}")
else:
    st.info(f"출근 시간: {record.check_in.strftime('%H:%M:%S')}")

# 퇴근
if record and not record.check_out:
    if st.button("퇴근하기"):
        record.check_out = datetime.now().time()
        db.commit()
        st.success(f"퇴근 시간 기록됨: {record.check_out.strftime('%H:%M:%S')}")
elif record and record.check_out:
    st.info(f"퇴근 시간: {record.check_out.strftime('%H:%M:%S')}")

# 근무 시간 계산
if record and record.check_in and record.check_out:
    t1 = datetime.combine(today, record.check_in)
    t2 = datetime.combine(today, record.check_out)
    work_duration = t2 - t1
    st.write(f"총 근무 시간: {work_duration}")
