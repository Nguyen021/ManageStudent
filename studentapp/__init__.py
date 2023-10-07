from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)

app.secret_key = "wa12ff25gr#..;'09u3q5fwx3ef98.,l;"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/manage_student?charset=utf8mb4" % quote("123456789")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


app.config['STUDENT_SIZE']=2
db = SQLAlchemy(app=app)
babel = Babel(app=app)

cloudinary.config(
    cloud_name="dif0oia5b",
    api_key="386971183136555",
    api_secret="inkWOO7C2gLlFFr8AqGu18ut4xE"
)

login = LoginManager(app=app)


@babel.localeselector
def get_locale():
    return 'vi'
