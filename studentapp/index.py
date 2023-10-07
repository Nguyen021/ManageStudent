from flask import render_template, request, redirect, url_for
from sqlalchemy import asc, desc
from studentapp import app, admin, dao, models, login, controller
import math
from flask_login import login_user, logout_user, login_required
from studentapp.decorators import *

app.add_url_rule("/", 'index', controller.index)

app.add_url_rule("/page-denied", 'access_denied', controller.access_denied)

app.add_url_rule("/user-login", 'user_signin', controller.user_signin, methods=['get', 'post'])

app.add_url_rule("/user-logout", 'user_signout', controller.user_signout)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


app.add_url_rule("/admin-login", 'admin_login', controller.admin_login, methods=['post'])

app.add_url_rule("/about", 'about_us', controller.about_us)

# Chuc nang danh cho NHAN VIEN
app.add_url_rule("/tiep-nhan-hoc-sinh", 'tiep_nhan', controller.tiep_nhan, methods=['get', 'post'])

app.add_url_rule("/dieu-chinh-lop", 'dieu_chinh_lop', controller.dieu_chinh_lop, methods=['get', 'post'])

# Chuc nang giao vien
app.add_url_rule("/nhap-diem", 'nhap_diem', controller.nhap_diem, methods=['get', 'post'])

app.add_url_rule("/diem-trung-binh", 'diem_trung_binh', controller.diem_trung_binh, methods=['get', 'post'])

if __name__ == '__main__':
    app.run(debug=True, port=4321)
