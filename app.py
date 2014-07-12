# ---------------
# Imports
# ---------------

from flask import Flask, make_response, request, jsonify, render_template, url_for
import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import types, desc

# ---------------
# Init
# ---------------

app = Flask(__name__)

if os.getenv('DEBUG') == 'false':
  app.debug = False
else:
  app.debug = True

app.secret_key = "ukl\xab\xb7\xc9\x10\xf7\xf1\x03\x087\x0by\x88X'v\xc9\x8c\xc4\xc8\xfe+"

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
db = SQLAlchemy(app)

# ---------------
# Settings
# ---------------

def add_cors_header(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
  response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

# -------------------
# Types
# -------------------

class JsonType(Mutable, types.TypeDecorator):
    ''' JSON wrapper type for TEXT database storage.

        References:
        http://stackoverflow.com/questions/4038314/sqlalchemy-json-as-blob-text
        http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/mutable.html
    '''
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        return unicode(json.dumps(value))

    def process_result_value(self, value, engine):
        if value:
            return json.loads(value)
        else:
            # default can also be a list
            return {}

# -------------------
# Models
# -------------------

class Doc(db.Model):
  '''
    A single documentation in a particular language
  '''
  # Columns
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.Unicode())
  version = db.Column(db.Unicode())
  description = db.Column(db.Unicode())
  sections = db.Column(JsonType())
  language = db.Column(db.Unicode())
  __table_args__ = ( db.UniqueConstraint('title', 'version', 'language'), { } )

  def __init__(self, title, version, description=None, sections=None, language='English'):
    self.title = title
    self.version = version
    self.description = description
    self.sections = sections
    self.language = language

  def __repr__(self):
    return "%s. v. %s" % (self.title, self.version)

  def asdict(self):
    '''
      Returns the documentation as a dictionary
    '''
    doc_dict = db.Model.asdict(self)
    return doc_dict

# -------------------
# Routes
# -------------------

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/<language>/')
def list(language):
  docs = Doc.query.filter(Doc.language == language).all()
  return render_template('list.html', docs=docs)

@app.route('/<language>/<title>/<version>')
def doc(language, title, version):
  filter = Doc.language == language and Doc.title == title and Doc.version == version
  doc = Doc.query.filter(filter).first()
  return render_template('list.html', docs=doc)


if __name__ == "__main__":
  app.run()