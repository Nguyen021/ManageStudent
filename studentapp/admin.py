from studentapp import db, app, dao
from studentapp.models import Class, Student, Subject, Semester, Mark, Regulation, UserRole, Grade, User
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, url_for
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')

        return super().__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class BackHomeView(BaseView):
    @expose('/')
    def __index__(self):
        return redirect(url_for('index'))


class StudentView(AuthenticatedModelView):
    column_searchable_list = ['fullname']
    column_filters = ['fullname', 'email', 'dob']

    column_editable_list = ['fullname']
    column_export_list = ['students']
    column_labels = {
        'id': 'Mã số',
        'fullname': 'Họ và tên',
        'gender': 'Giới tính',
        'phone': 'Số điện thoại',
        'address': 'Địa chỉ',
        'dob': 'Ngày sinh',

    }
    column_sortable_list = ['id', 'fullname']

    page_size = 20
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'address': CKTextAreaField
    }


class GradeView(AuthenticatedModelView):
    column_filters = ['grade_name']
    column_labels = {
        'id': 'Mã khối',
        'grade_name': 'Tên khối',
        'classes': 'Lớp thuộc khối'
    }
    column_list = ['id', 'grade_name', 'classes']
    column_display_all_relations = True
    column_default_sort = 'grade_name'
    form_columns = ['grade_name', 'classes']


class ClassView(AuthenticatedModelView):
    column_sortable_list = ['class_name', 'class_size']

    column_labels = {
        'id': 'Mã lớp',
        'class_name': 'Tên lớp',
        'class_size': 'Sĩ số lớp',
        'grade': 'Khối',
        'students': 'hoc sinh'
    }


class SubjectView(AuthenticatedModelView):
    column_labels = {
        'id': 'Mã môn học',
        'subject_name': 'Tên môn học',
    }


class MarkView(AuthenticatedModelView):
    column_sortable_list = ['value', 'type']
    column_filters = ['type', 'student_id']
    column_labels = {
        'id': 'Mã ',
        'type': 'Điểm',
        'value': 'Điểm số',
        'student': 'Học sinh',
        'semester': 'Học kỳ',
        'subject': 'Môn học'

    }


class SemesterView(AuthenticatedModelView):
    column_sortable_list = ['semester_name', 'school_year']
    column_filters = ['school_year']
    column_labels = {
        'id': 'Mã học kỳ',
        'semester_name': 'Học kỳ',
        'school_year': 'Năm học',

    }


class RegulationView(AuthenticatedModelView):
    column_sortable_list = ['min_age', 'max_age']

    column_labels = {
        'id': 'Mã ',
        'min_age': 'Độ tuổi tối thiểu',
        'max_age': 'Độ tuổi tối đa',
        'max_size_class': 'Sĩ số tối đa ',

    }


class UserView(AuthenticatedModelView):
    column_exclude_list = ['avatar', 'joined_date', 'password']
    column_sortable_list = ['fullname', 'dob']


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        # stats = dao.stats_revenue(kw=request.args.get('kw'),
        #                           from_date=request.args.get('from_date'),
        #                           to_date=request.args.get('to_date'))
        return self.render('admin/stats.html')


admin = Admin(app=app, name='Trang Quản Trị', template_mode='bootstrap4')
admin.add_view(BackHomeView(name='Trang chính'))
admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(ClassView(Class, db.session, name='Lớp', category="QL Khối Lớp"))
admin.add_view(StudentView(Student, db.session, name='Học sinh', category="QL Điểm HS"))
admin.add_view(SubjectView(Subject, db.session, name='Môn học', category="QL Điểm HS"))
admin.add_view(SemesterView(Semester, db.session, name='Học Kỳ', category="QL Khối Lớp"))
admin.add_view(MarkView(Mark, db.session, name='Điểm', category="QL Điểm HS"))
admin.add_view(GradeView(Grade, db.session, name='Khối', category="QL Khối Lớp"))
admin.add_view(RegulationView(Regulation, db.session, name='Quy định'))
admin.add_view(StatsView(name='Thống kê - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
