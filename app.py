# ---------------
# Imports
# ---------------

from flask import Flask, make_response, request, jsonify, render_template, url_for, redirect
import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import types, desc
from dictalchemy import make_class_dictable
from urllib import quote_plus
import requests

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
make_class_dictable(db.Model)

yandex_key = os.getenv('YANDEX_API_KEY')

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

  def __init__(self, title, version, description=None, sections=[], language='English'):
    self.title = title
    self.version = version
    self.description = description
    self.sections = sections
    self.language = language

  def api_url(self):
      ''' 
        API link to itself
      '''
      return '%s://%s/api/%s/%s/%s' % (request.scheme, request.host, self.language, self.title, self.version)

  def asdict(self):
    '''
      Returns the documentation as a dictionary
    '''
    doc_dict = db.Model.asdict(self)
    doc_dict['api_url'] = self.api_url()
    return doc_dict

  def __repr__(self):
    return "%s. v. %s. lang: %s" % (self.title, self.version, self.language)

# -------------------
# Helpers
# -------------------

def translate_text(phrase, from_lang='en', dest_lang='es'):
  url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=%s-%s&text=%s" % (yandex_key, from_lang, dest_lang, quote_plus(phrase))
  translation = requests.get(url)
  return json.loads(translation.content)['text'][0]

# -------------------
# Routes
# -------------------

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/save/', methods=['POST', 'GET'])
def save():
  if request.method != 'POST':
    return 'POST here to save'
  if request.method == 'POST':
    doc_data = request.get_json(force=True)

    filter = Doc.language == doc_data['language'], Doc.title == doc_data['title'], Doc.version == doc_data['version']
    existing_doc = db.session.query(Doc).filter(*filter).first()
    
    if not existing_doc:
      new_doc = Doc(**doc_data)
      db.session.add(new_doc)
      db.session.commit()
      return redirect(new_doc.asdict()['api_url'])

    for (field, value) in doc_data.items():
      setattr(existing_doc, field, value)

    db.session.commit()
    return redirect(existing_doc.asdict()['api_url'])

@app.route('/languages/')
def languages():
  languages = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs?key=%s&ui=en' % yandex_key)
  return jsonify(json.loads(languages.content)['langs'])

@app.route('/api/<language>')
def list(language):
  docs = db.session.query(Doc).filter(Doc.language == language).all()
  return jsonify({ 'docs': [doc.asdict() for doc in docs] })

@app.route('/api/<language>/<title>/<version>')
def doc(language, title, version):
  filter = Doc.language == language, Doc.title == title, Doc.version == version
  doc = db.session.query(Doc).filter(*filter).first()
  if doc:
    return jsonify(doc.asdict())
  else:
    filter = Doc.language == 'en', Doc.title == title, Doc.version == version
    doc = db.session.query(Doc).filter(*filter).first()
    new_doc = Doc(title=doc.title, version=doc.version, language=language, 
                  description=translate_text(doc.description))
    db.session.add(new_doc)
    db.session.commit()
    payload = new_doc.asdict()
    payload['new'] = True
    return jsonify(payload)

if __name__ == "__main__":
  app.run()