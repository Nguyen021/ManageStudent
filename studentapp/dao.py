from studentapp.models import Student, User, Subject, UserRole, Regulation, Class, Mark, Semester
from studentapp import db, app
from sqlalchemy import func, asc, and_, or_
import hashlib
from datetime import datetime


def get_user_by_id(user_id):
    user = User.query.filter(User.id.__eq__(user_id)).first()

    if user:
        return user


def check_email_exist(email):
    student = Student.query.filter(Student.email.__eq__(email)).count()

    if student == 0:
        return True
    else:
        return False


def validated_age(min_age, max_age, dob_year):
    current_year = datetime.now().year
    age = current_year - dob_year

    if min_age <= int(age) <= max_age:
        return True
    else:
        return False


def hash_password(passw):
    password = str(hashlib.md5(passw.strip().encode('utf8')).hexdigest())
    return password


def check_login(username, password, role):
    if username and password:
        password = hash_password(password)

        return User.query.filter((User.username.__eq__(username.strip())),
                                 User.password.__eq__(password.strip()),
                                 User.user_role.__eq__(role)).first()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id1(user_id):
    return User.query.get(User.id.__eq__(user_id)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_student_by_id(student_id):
    student_id = str(student_id).lower().strip()
    student = Student.query.filter(Student.id.__eq__(student_id)).first()

    if student:
        return student


def add_student(fullname, gender, email, phone, address, dob):
    try:
        student = Student(fullname=fullname,
                          gender=gender,
                          email=email,
                          phone=phone,
                          address=address,
                          dob=dob)
        db.session.add(student)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()


def get_all_student():
    students = Student.query.filter().all()
    return students


def load_student_by_page(page=1):
    student_size = app.config['STUDENT_SIZE']
    start = (page - 1) * student_size
    end = student_size * page

    if page:
        students = get_all_student()
        # print(students[0], (students[0].classes[0]))
        return students[start:end]


def count_student():
    return Student.query.filter().count()


def count_subject():
    return Subject.query.filter().count()


def count_staff():
    return User.query.filter(User.user_role == UserRole.STAFF).count()


def count_teacher():
    return User.query.filter(User.user_role == UserRole.TEACHER).count()


def get_regulation():
    regulation = Regulation.query.order_by(Regulation.id.asc()).first()

    if regulation:
        return regulation


def get_all_classes():
    return Class.query.order_by(asc(Class.class_name)).all()


def count_student_by_class(class_id):
    # total_student = Student.query.filter(Student.classes.id == class_id).count()
    class_current = Class.query.filter(Class.id.__eq__(class_id)).first()
    total_student = len(class_current.students)

    if total_student:
        return total_student


def check_total_student_regulation(class_id):
    regulation = get_regulation()
    class_input = Class.query.filter(Class.id.__eq__(class_id)).first()

    if class_input.class_size < regulation.max_size_class:
        return True
    else:
        return False


def get_class_by_name(class_name):
    return Class.query.filter(Class.class_name.__eq__(class_name)).first()


def get_class_by_id(class_id):
    class_obj = Class.query.get(class_id)
    return class_obj.class_name


def get_class_id_by_name(class_name):
    classes = Class.query.filter(Class.class_name.__eq__(class_name)).first()
    return classes.id


def get_student_by_class_id(class_id):
    class_obj = Class.query.get(class_id)
    # print(class_obj)
    # print(class_obj.students)
    students = class_obj.students
    return students


def get_mark_by_subject_and_class(semester_id, subject_id, class_id):
    mark_list = []
    students = get_student_by_class_id(class_id=class_id)
    print(students)
    if students:
        for s in students:
            mark_result = Mark.query.filter(and_(Mark.semester_id.__eq__(semester_id),
                                                 Mark.student_id.__eq__(s.id),
                                                 Mark.subject_id.__eq__(subject_id))).all()

            if mark_result:
                for i in mark_result:
                    mark_list.append(i)
            else:

                mark_list.append(None)

    return mark_list


def get_mark_type_by_subject_and_class(semester_id, subject_id, class_id):
    mark_type = []
    students = get_student_by_class_id(class_id=class_id)

    if students:
        for s in students:
            mark_result = Mark.query.filter(and_(Mark.semester_id.__eq__(semester_id),
                                                 Mark.student_id.__eq__(s.id),
                                                 Mark.subject_id.__eq__(subject_id))).all()

            if mark_result:
                for i in (set(mark_result)):
                    mark_type.append(i.type)
            # else:

                # mark_type.append(None)
                # return False
        print('set mark_type', (mark_type))
    return sorted(set(mark_type))


def get_all_class():
    return Class.query.all()


def get_all_subject():
    return Subject.query.order_by(Subject.id.asc()).all()


def get_subject_by_id(subject_id):
    subject = Subject.query.get(subject_id)
    return subject


def get_all_semester():
    return Semester.query.order_by(Semester.id.asc()).all()


def get_semester_by_id(semester_id):
    semester = Semester.query.get(semester_id)
    return semester


def get_all_type_mark():
    mark = Mark.query.order_by(Mark.id.desc()).all()
    type_mark = []
    for m in mark:
        type_mark.append(m.type)
    print("mark type ", type(mark), 'mark value', mark)
    print('type[[]]',type_mark)
    print('set type[[]]',set(type_mark))

    return set(type_mark)


def get_student_by_id_name(student_id, student_name):
    student = Student.query.filter(and_(Student.id.__eq__(student_id), Student.fullname.__eq__(student_name))).first()
    if student:
        return student


# def get_student_class(student_id):
#     return student_class.query.filter(student_class.)

def change_class_for_student(student_id, class_id):
    class_before = Student.query.filter(Student.id.__eq__(student_id)).first().classes[-1]

    class_id_before = class_before.id

    new_class = Class.query.filter(Class.id.__eq__(class_id)).order_by(Class.id.asc()).first()
    new_class = Class.query.filter(Class.id.__eq__(class_id)).order_by(Class.id.asc()).first()
    print('new class', new_class)
    if class_id_before != new_class.id:

        size_class_before = str(count_student_by_class(class_id=class_id_before))

        class_before.class_size = int(size_class_before) - 1
        db.session.commit()
        size_class_new = str(count_student_by_class(class_id=class_id))

        new_class.class_size = int(size_class_new) + 1

        student = Student.query.filter(Student.id.__eq__(student_id)).first()
        print('student', student)
        print('student classes', student.classes)
        # student.classes[0].id = class_id
        class_new = Class.query.get(class_id)
        print('class', class_new)
        student.classes.append(Class.query.get(class_id))
        db.session.commit()
        return True
    else:
        return False


# Nhap Diem
def add_mark(type_mark, value, student_id, semester_id, subject_id):
    try:
        mark = Mark(subject_id=subject_id, student_id=student_id, semester_id=semester_id,
                    type=type_mark, value=value)

        db.session.add(mark)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
