import os
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class DirectoryInfo(db.Model):
    __tablename__ = 'dirtable'
    id = db.Column(db.Integer, primary_key=True)
    m_fileId = db.Column(db.Integer, unique=True)
    m_fileName = db.Column(db.String)
    m_parentFileId = db.Column(db.Integer)
    m_file_type = db.Column(db.Integer)
    m_fileSize = db.Column(db.Float)
    m_fileModifyTime = db.Column(db.String)
    m_fileUrl = db.Column(db.String)
    m_fileMD5 = db.Column(db.Text)

    def __repr__(self):
        #return '<DirectoryInfo %r>' % self.m_fileName
        data = {
            "m_fileId": self.m_fileId,
            "m_fileName": self.m_fileName,
            "m_parentFileId": self.m_parentFileId,
            "m_file_type": self.m_file_type,
            "m_fileSize": self.m_fileSize,
            "m_fileModifyTime": self.m_fileModifyTime,
            "m_fileUrl": self.m_fileUrl,
	        "m_fileMD5": self.m_fileMD5,
        }
	return '<DirectoryInfo %r>'  % data


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'),
    #                        known=session.get('known', False))
    return '<p>hello world</p>'


@app.route('/refresh', methods=['GET'])
def refresh():
    data = DirectoryInfo.query.all()
    reData = JSONEncoder().encode(data)
    return '<p>reData</p>'
if __name__ == '__main__':
    manager.run()
