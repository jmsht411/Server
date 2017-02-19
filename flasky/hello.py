import os
from flask import Flask, request
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
# from werkzeug import secure_filename

import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        'm_fileId': self.m_fileId,
        'm_fileName': self.m_fileName,
        'm_parentFileId': self.m_parentFileId,
        'm_file_type': self.m_file_type,
        'm_fileSize': self.m_fileSize,
        'm_fileModifyTime': self.m_fileModifyTime,
        'm_fileUrl': self.m_fileUrl,
        'm_fileMD5': self.m_fileMD5
    }

	return json.dumps(data)



@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/refresh', methods=['GET'])
def refresh():
    data = DirectoryInfo.query.all()
    print data[0]
    temp = str(data)
    return temp

@app.route('/newdocument', methods=['POST'])
def newdocument():
    documentInfo = request.get_data()
    print documentInfo
    j = json.loads(documentInfo)
    print j['m_fileName']
    m_temp = DirectoryInfo(m_fileId=j['m_fileId'],
                           m_fileName=j['m_fileName'],
                           m_parentFileId=j['m_parentFileId'],
                           m_file_type=j['m_file_type'],
                           m_fileSize=j['m_fileSize'],
                           m_fileModifyTime=j['m_fileModifyTime'],
                           m_fileUrl=j['m_fileUrl'],
                           m_fileMD5=j['m_fileMD5'])
    db.session.add(m_temp)
    db.session.commit()
    return 'OK'
    
# @app.route('/upload', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['the_file']
#         f.save('/var/www/uploads/' + secure_filename(f.filename))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
