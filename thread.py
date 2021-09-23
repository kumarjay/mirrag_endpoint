from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash
import concurrent.futures


app = Flask(__name__)

db = SQLAlchemy(app)
db.init_app(app)

class IntrusionDashboard(db.Model):
    __tablename__ = 'staircase_predictions'

    id= db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    camera_id = db.Column(db.String(35))
    model_version = db.Column(db.String(35))
    is_violation = db.Column(db.Boolean)
    img_path = db.Column(db.String(255))
    out_data = db.Column(JSON)
    description = db.Column(db.String(255))
    created_time = db.Column(db.String(120))
    prediction_time= db.Column(db.String(150))
    camera_view= db.Column(db.String(35))
    is_buzzer_start= db.Column(db.Boolean)



def data_query(text):
    intrude_data = IntrusionDashboard.query.all()
    print('itrude data is..', intrude_data)
    return intrude_data

def multi_processing():
    # texts = re.split(',+', texts)

    with concurrent.futures.ThreadPoolExecutor() as exe:
        doc_list = []

        results = exe.map(data_query, 'text')
        print('results is...', results)

        for res in results:
            print('jfahjshfjh      ', res)
            doc_list.append(res)
    return doc_list[0]