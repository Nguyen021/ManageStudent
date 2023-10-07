from sqlalchemy import Column, Integer, ForeignKey, Date, Float, Boolean, String, DateTime, Enum, desc, asc, \
    UniqueConstraint
from enum import Enum as UserEnum
from studentapp import db, app
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin


class UserRole(UserEnum):
    GUEST = 0
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

    def __str__(self):
        if str(self.name).__eq__('STAFF'):
            return 'NHÂN VIÊN'
        elif str(self.name).__eq__('TEACHER'):
            return 'GIÁO VIÊN'

        return self.name


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Information(Base):
    __abstract__ = True

    fullname = Column(String(50), nullable=False)
    dob = Column(Date)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(15), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    gender = Column(Boolean, nullable=False)
    address = Column(String(50), nullable=False)


class User(Information, UserMixin):
    __tablename__ = 'user'

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200),
                    default='https://res.cloudinary.com/dif0oia5b/image/upload/v1670231384/avatar/avatar_a79t6s.jpg')
    joined_date = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.GUEST)

    def __str__(self):
        return self.username


student_class = db.Table('student_class',
                         Column('student_id', ForeignKey('student.id'), nullable=False, primary_key=True),
                         Column('class_id', ForeignKey('class.id'), nullable=False, primary_key=True))


class Student(Information):
    __tablename__ = 'student'

    date_graduation = Column(Date)
    admission = Column(Date)

    marks = relationship('Mark', backref='student', lazy=True)

    def __str__(self):
        return self.fullname


class Semester(Base):
    __tablename__ = 'semester'

    semester_name = Column(String(10), nullable=False)
    school_year = Column(String(20), nullable=False)

    marks = relationship('Mark', backref='semester', lazy=True)

    def __str__(self):
        return "HK{semester} - {school_year}".format(semester=self.semester_name,
                                                     school_year=self.school_year)


class Subject(Base):
    __tablename__ = 'subject'

    subject_name = Column(String(50), nullable=True)

    marks = relationship('Mark', backref='subject', lazy=True)

    def __str__(self):
        return self.subject_name


class Mark(Base):
    __tablename__ = 'mark'

    type = Column(String(20))
    value = Column(Float)

    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    __table_args__ = (UniqueConstraint('type', 'value', 'student_id',
                                       'semester_id', 'subject_id',
                                       name='_mark_subject_uc'),
                      )

    def __str__(self):
        return "{value} - {type} - {student} - {subject} - HK{semester}".format(value=self.value, type=self.type,
                                                                                student=self.student.fullname,
                                                                                subject=self.subject.subject_name,
                                                                                semester=self.semester.semester_name)


class Grade(Base):
    __tablename__ = 'grade'

    grade_name = Column(String(10))

    classes = relationship('Class', backref='grade', lazy=True)

    def __str__(self):
        return self.grade_name


class Class(Base):
    __tablename__ = 'class'

    class_name = Column(String(10), unique=True, nullable=False)
    class_size = Column(Integer, nullable=False)

    grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)
    students = relationship(Student, secondary='student_class', lazy='subquery', backref=backref('classes', lazy=True))

    def __str__(self):
        return self.class_name


class Regulation(Base):
    __tablename__ = 'regulation'

    min_age = Column(Integer)
    max_age = Column(Integer)
    max_size_class = Column(Integer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        #
        # u1 = User(fullname='Trần Thanh Nguyên', email='ttnguyen@gmail.com', username='admin',
        #           password=str(hashlib.md5('admin'.encode('utf8')).hexdigest()),
        #           user_role=UserRole.ADMIN, phone='324123013', address='Binh Hoa', gender=True
        #           )
        # u2 = User(fullname='Nguyễn Thu Dương', email='ntduong@gmail.com', username='teacher',
        #           password=str(hashlib.md5('teacher'.encode('utf8')).hexdigest()),
        #           user_role=UserRole.TEACHER, phone='3452345155', address='Binh Nguyen', gender=False
        #           )
        # u3 = User(fullname='Lê Thị Trung', email='lttrung@gmail.com', username='staff',
        #           password=str(hashlib.md5('staff'.encode('utf8')).hexdigest()),
        #           user_role=UserRole.STAFF, phone='0456956', address='Binh Tan', gender=True
        #           )
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()
        from operator import length_hint

        # c = Class.query.filter(Class.id == 1).first()
        # print(c)
        # a = c.students
        # print('student cua clas 1',a)
        # b = len(a)
        # print(b)
        #
        # student = Student.query.filter(Student.id == 1).first()
        # print('student: ', student)
        # class_name = (student.classes[0])
        # print(class_name.id)
        # print(class_name.class_name)
        # print(class_name.class_size)

        # print(Student.query.order_by(desc(Student.id)).first())
