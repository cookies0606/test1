from sqlalchemy import Column, Integer, String, Date, Time, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 기존 직원 테이블
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    phone = Column(String)
    is_admin = Column(Boolean, default=False)  # 🔐 권한관리

# 근태 기록
class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(Date)
    check_in = Column(Time)
    check_out = Column(Time)

# 연차 신청
class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(Date)
    reason = Column(String)
    status = Column(String, default="대기")  # 대기, 승인, 반려

# 봉급 정보
class Salary(Base):
    __tablename__ = 'salaries'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    year = Column(Integer)
    month = Column(Integer)
    amount = Column(Float)
