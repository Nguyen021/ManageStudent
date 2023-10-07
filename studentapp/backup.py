from flask import render_template, request, redirect, url_for
from sqlalchemy import asc, desc

from studentapp import app, admin, dao, models, login
import math
from flask_login import login_user, logout_user, login_required
from studentapp.decorators import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page-denied')
def access_denied():
    return render_template('home/page-denied.html')


@app.route('/user-login', methods=['get', 'post'])
@annonynous_user
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = models.User.query.filter(models.User.username.__eq__(username.strip())).first()
        password = dao.hash_password(password)
        if user:
            if password.__eq__(user.password):
                login_user(user=user)
                return redirect(url_for('index'))
            else:
                err_msg = 'Mật khẩu không chính xác'
        else:
            err_msg = 'Username không tồn tại'
    return render_template('home/login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['post'])
@admin_requirement
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.check_login(username=username, password=password, role=models.UserRole.ADMIN)

    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/about')
def about_us():
    return render_template('home/about.html')


# Chuc nang danh cho NHAN VIEN
@app.route('/tiep-nhan-hoc-sinh', methods=['post', 'get'])
@login_required
@staff_requirement
def tiep_nhan():
    msg = ''
    msg_success = ''
    count_all_student = dao.count_student()
    page_total = math.ceil(count_all_student / app.config['STUDENT_SIZE'])

    page = request.args.get('page', 1)
    students = dao.load_student_by_page(page=int(page))

    fullname = None
    email = None
    phone = None
    address = None
    dob_day = None
    dob_month = None
    dob_year = None

    min_age = dao.get_regulation().min_age
    max_age = dao.get_regulation().max_age

    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        dob_day = request.form.get('dob_day')
        dob_month = request.form.get('dob_month')
        dob_year = request.form.get('dob_year')
        dob = "{y}-{m}-{d}".format(y=dob_year, m=dob_month, d=dob_day)

        check_email = dao.check_email_exist(email=email)
        if check_email:
            check_age = dao.validated_age(min_age=min_age, max_age=max_age, dob_year=int(dob_year))
            if check_age:
                dao.add_student(fullname=fullname, email=email, gender=bool(int(gender)),
                                phone=phone, address=address, dob=dob)

                count_all_student = dao.count_student()
                page_total = math.ceil(count_all_student / app.config['STUDENT_SIZE'])

                students = dao.load_student_by_page(page=int(page))

                msg_success = 'Tiếp nhận thành công học sinh'

            else:
                msg = "Độ tuổi của học sinh không nằm trong khoảng từ {min_age} đến {max_age}." \
                      " Vui lòng kiểm tra lại !!!" \
                    .format(min_age=min_age, max_age=max_age)
        else:
            msg = 'Email của học sinh đã tồn tại. Vui lòng kiểm tra lại'
    return render_template('home/tiep-nhan-hoc-sinh.html', students=students,
                           page_total=page_total,
                           current_page=int(page),
                           message=msg,
                           fullname=fullname,
                           email=email,
                           phone=phone,
                           address=address,
                           dob_year=dob_year,
                           dob_month=dob_month,
                           dob_day=dob_day,
                           message_success=msg_success)


@app.route('/dieu-chinh-lop', methods=['post', 'get'])
@login_required
@staff_requirement
def dieu_chinh_lop():
    msg = ''
    msg_success = ''
    count_all_student = dao.count_student()
    page_total = math.ceil(count_all_student / app.config['STUDENT_SIZE'])

    page = request.args.get('page', 1)
    students = dao.load_student_by_page(page=int(page))

    classes = dao.get_all_class()
    if request.method.__eq__('POST'):
        student_id = request.form.get('student_id')
        class_name = request.form.get('class_name')

        class_get = dao.get_class_by_name(class_name=class_name)
        student_get = dao.get_student_by_id(student_id=student_id)

        if student_get:
            if class_get:
                result_check = dao.check_total_student_regulation(class_id=class_get.id)
                if result_check:

                    result = dao.change_class_for_student(student_id=int(student_id),
                                                          class_id=class_get.id)
                    print('result', result)
                    if result:
                        msg_success = 'Học sinh {name} đã được cập nhập thành lớp {class_name} thành công' \
                            .format(name=student_get.fullname, class_name=class_get.class_name)
                    else:
                        msg = 'Lớp học sinh đã tồn tại'
                else:
                    msg = "Lớp {name} đã đạt sĩ số tối đa cho phép".format(name=class_name)
            else:
                msg = "Không tồn tại lớp {name}".format(name=class_name)
        else:
            msg = "Không tồn tại học sinh với {id} trên ".format(id=student_id)

    return render_template('home/dieu-chinh-lop.html',
                           page_total=page_total,
                           current_page=int(page),
                           students=students,
                           message=msg,
                           message_success=msg_success,
                           classes=classes)


# Chuc nang giao vien
@app.route('/nhap-diem', methods=['post', 'get'])
def nhap_diem():
    count_all_student = dao.count_student()
    page_total = math.ceil(count_all_student / app.config['STUDENT_SIZE'])

    page = request.args.get('page', 1)
    students = dao.load_student_by_page(page=int(page))

    # student = dao.get_student_by_id(student_id=student_id)
    msg = ''
    msg_success = ''
    semesters = dao.get_all_semester()
    subjects = dao.get_all_subject()
    type_mark = dao.get_all_type_mark()
    print('type_mark', type_mark, 'typew', type(type_mark))
    if request.method.__eq__('POST'):
        student_id = request.form.get('student_id')
        # print('student_id',student_id)
        student_name = request.form.get('student_name')
        # print('student_name', student_name)
        subject_id = request.form.get('subject_id')
        # print('subject_id', subject_id)
        semester_id = request.form.get('semester_id')
        # print('semester_id', semester_id)
        mark_type = request.form.get('mark_type')
        # print('mark_type', mark_type)
        value = request.form.get('value')
        # print('value', value)
        student = dao.get_student_by_id_name(student_id=student_id,
                                             student_name=student_name)
        subject = dao.get_subject_by_id(subject_id=int(subject_id))
        semester = dao.get_semester_by_id(semester_id=int(semester_id))
        if student:
            try:
                dao.add_mark(type_mark=mark_type,
                             value=float(value),
                             student_id=int(student_id),
                             semester_id=int(semester_id),
                             subject_id=int(subject_id))
            except Exception as ex:
                msg = 'Đã có lỗi trong quá trình thêm đểm cho học sinh: ' + str(ex)
            else:
                msg_success = 'Thêm điểm cho học sinh {student_name} với mã học sinh {student_id}.' \
                              ' Điểm {type_mark} cho môn {subject} học kỳ {semester}' \
                    .format(student_name=student_name,
                            student_id=student_id,
                            type_mark=mark_type,
                            subject=subject,
                            semester=semester)
        else:
            msg = 'Mã học sinh và tên học sinh không khớp vui lòng kiểm tra lại  '
    return render_template('home/nhap-diem.html',
                           message=msg,
                           message_success=msg_success,
                           all_semester=semesters,
                           subjects=subjects,
                           type_mark=type_mark)


@app.route('/diem-trung-binh', methods=['post', 'get'])
def diem_trung_binh():
    classes = dao.get_all_class()
    semesters = dao.get_all_semester()
    subjects = dao.get_all_subject()
    students_in_class = None
    class_name = None
    marks = None
    subjects_object = None
    semester_object = None
    mark_type=None
    msg = ''
    msg_success = ''
    # students_in_class = dao.get_student_by_class_id(class_id=int(1))  # test
    # marks = dao.get_mark_by_subject_and_class(semester_id=1,
    #                                            subject_id=1,
    #                                            class_id=1)
    # dao.get_mark_by_subject_and_class(class_id=1, subject_id=1, semester_id=1)
    if request.method.__eq__('POST'):
        class_id = request.form.get('class_id')
        semester_id = request.form.get('semester_id')
        subject_id = request.form.get('subject_id')
        class_name = dao.get_class_by_id(class_id=int(class_id))
        students_in_class = None

        if class_id:
            # class_object = dao.get_class_by_name(class_name)
            semester_object = dao.get_semester_by_id(semester_id=int(semester_id))

            if semester_object:
                subjects_object = dao.get_subject_by_id(subject_id=int(subject_id))
                students_in_class = dao.get_student_by_class_id(class_id=int(class_id))

                marks = dao.get_mark_by_subject_and_class(semester_id=semester_id,
                                                          subject_id=subject_id,
                                                          class_id=class_id)
                mark_type = dao.get_mark_type_by_subject_and_class(semester_id=semester_id,
                                                                   subject_id=subject_id,
                                                                   class_id=class_id)
                print('mark', marks)
            else:
                msg = 'Học kỳ không tồn tại'
        else:
            msg = 'Mã lớp không tồn tại'
    return render_template('home/diem-trung-binh.html', classes=classes,
                           semesters=semesters,
                           semesters_obj=semester_object,
                           subjects=subjects,
                           students=students_in_class,
                           message=msg,
                           marks=marks,
                           class_name=class_name,
                           subject_obj=subjects_object,
                           mark_type=mark_type
                           )

#
# if __name__ == '__main__':
#     app.run(debug=True, port=4321)
