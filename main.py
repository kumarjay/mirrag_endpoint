import time

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
# from flask_ngrok import run_with_ngrok
import atexit
# from apscheduler.scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_crontab import Crontab
import threading
import concurrent.futures
import socket

print('host name is.....', socket.gethostname())


app = Flask(__name__)
# run_with_ngrok(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://RAMADHELPD3ITD/PPE_VIOLATION?driver=SQL+Server?trusted_connection=yes"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jay#2107@localhost:5432/test001'

# cron = Scheduler(daemon=True)
crontab= Crontab(app)

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

camera_id= 5
company_id= 123
model_version= '3.6'
# is_violation= True
img_path= '/jay/abc/'
out_data= {'hello': 1, "world": 2}
description= 'this is world'
created_time= datetime.now()
prediction_time= datetime.now()
camera_view= 'Straight'
is_buzzer_start= False


# db.session.add(entry)
# db.session.commit()


@app.route('/', methods= ['GET', 'POST'])
def index():
    return render_template('index.html')


def hello_job():
    print('hello world')


def cron_schedule():
    scheduler = BackgroundScheduler()
    # in your case you could change seconds to hours
    scheduler.add_job(hello_job, trigger='interval', seconds=60)
    scheduler.start()

    try:
        # To keep the main thread alive
        return app
    except:
        # shutdown if app occurs except
        scheduler.shutdown()


def data_query(text):
    # time.sleep(5)
    intrude_data = IntrusionDashboard.query.all()
    # print('itrude data is..', intrude_data)
    return intrude_data


def multi_processing():
    # texts = re.split(',+', texts)

    with concurrent.futures.ThreadPoolExecutor() as exe:
        doc_list = []
        results = exe.map(data_query, 'text')
        for res in results:
            # print('jfahjshfjh      ', res)
            doc_list.append(res)
    return doc_list[0]


@crontab.job(minute="1", hour="*", day="*", month="*", day_of_week="*")
@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    print('host name...', socket.gethostname())
    t1= time.time()
    # intrude_data= threading.Thread(target= data_query).start()
    intrude_data= ''
    # with concurrent.futures.ProcessPoolExecutor as executor:
    #     intrude_data= executor.map(data_query,'abc')
    # intrude_data = IntrusionDashboard.query.all()
    # for i in intrude_data:
    #     print(i.name)
    intrude_data= multi_processing()
    t2= time.time()
    print('intrude data is...', t2-t1)
    cron_schedule()
    return render_template('view_data.html', database_values= intrude_data)


@app.route('/data_form', methods=['GET', 'POST'])
def data_form():
    return render_template('data_form.html')


@app.route('/upload_data', methods=['POST'])
def upload_data():
    camera_view= request.form.get('camera_view')
    camera_id= request.form.get('camera_id')
    description= request.form.get('api_key')
    created_time= datetime.now()

    # print(name, ' ', company_code, ' ', api_key, ' ', created_time)
    # camera_id = 5
    company_id= 10
    # company_id = 123
    model_version = '3.6'
    is_violation = True
    img_path = '/jay/abc/'
    out_data = {'hello': 1, "world": 2}
    # description = 'this is world'
    # created_time = datetime.now()
    prediction_time = datetime.now()
    # camera_view = 'Straight'
    is_buzzer_start = False

    entry = IntrusionDashboard(camera_view=camera_view, company_id=company_id, description=description,
                               created_time=created_time, camera_id= camera_id, model_version= model_version,
                               is_violation= is_violation, img_path= img_path, out_data= out_data,
                               prediction_time= prediction_time, is_buzzer_start= is_buzzer_start)

    db.session.add(entry)
    db.session.commit()
    print('Whola ! vinsertion successful ')
    return render_template('index.html', message= 'insertion successful')

# Shutdown your cron thread if the web process is stopped
# atexit.register(lambda: cron.shutdown(wait=False))


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port= 9050, debug= True)




