from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE-URI']='sqlite:///'+os.path.join(basedir)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Init db
db=SQLAlchemy(app)

#Init ma
ma=Marshmallow(app)

#Patient Class
class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    right_hip_angle=db.Column(db.Float)
    right_knee_angle=db.Column(db.Float)
    right_ankle_angle=db.Column(db.Float)
    left_hip_angle=db.Column(db.Float)
    left_knee_angle=db.Column(db.Float)
    left_ankle_angle=db.Column(db.Float)

    def __init__(self,name,right_hip_angle,right_knee_angle,right_ankle_angle,left_hip_angle,left_knee_angle,left_ankle_angle):
        self.name=name
        self.right_hip_angle=right_hip_angle
        self.right_knee_angle=right_knee_angle
        self.right_ankle_angle=right_ankle_angle
        self.left_hip_angle=left_hip_angle
        self.left_knee_angle=left_knee_angle
        self.left_ankle_angle=left_ankle_angle

db.create_all()

class PatientSchema(ma.Schema):
    class Meta:
        fields=('id','name','right_hip_angle','right_knee_angle','right_ankle_angle','left_hip_angle','left_knee_angle','left_ankle_angle')

#Init schema
patient_schema=PatientSchema()
patients_schema=PatientSchema(many=True)

@app.route('/patient',methods=['POST'])
def add_patient():
    name=request.json['name']
    right_hip_angle=request.json['right_hip_angle']
    right_knee_angle=request.json['right_knee_angle']
    right_ankle_angle=request.json['right_ankle_angle']
    left_hip_angle=request.json['left_hip_angle']
    left_knee_angle=request.json['left_knee_angle']
    left_ankle_angle=request.json['left_ankle_angle']

    new_patient=Patient(name,right_hip_angle,right_knee_angle,right_ankle_angle,left_hip_angle,left_knee_angle,left_ankle_angle)    

    db.session.add(new_patient)
    db.session.commit()

    return patient_schema.jsonify(new_patient)

#Get All Patients
@app.route('/patient/',methods=['GET'])
def get_patients():
    all_products=Patient.query.all()
    result=patients_schema.dump(all_products)
    return jsonify(result)

#Get Single Patient
#By id
@app.route('/patient/<id>',methods=['GET'])
def get_patient_byId(id):
    patient=Patient.query.get(id)
    return patient_schema.jsonify(patient)

#Update patient
@app.route('/patient/<id>',methods=['PUT'])
def update_patient(id):
    patient=Patient.query.get(id)

    name=request.json['name']
    right_hip_angle=request.json['right_hip_angle']
    right_knee_angle=request.json['right_knee_angle']
    right_ankle_angle=request.json['right_ankle_angle']     
    left_hip_angle=request.json['left_hip_angle']
    left_knee_angle=request.json['left_knee_angle']
    left_ankle_angle=request.json['left_ankle_angle']

    patient.name=name
    patient.right_hip_angle=right_hip_angle
    patient.right_knee_angle=right_knee_angle
    patient.right_ankle_angle=right_ankle_angle
    patient.left_hip_angle=left_hip_angle
    patient.left_knee_angle=left_knee_angle
    patient.left_ankle_angle=left_ankle_angle
   
    db.session.commit()
    return patient_schema.jsonify(patient)

#Delete patient
@app.route('/patient/<id>',methods=['DELETE'])
def delete_patient(id):
    patient=Patient.query.get(id)
    
    db.session.delete(patient)
    db.session.commit()

    return patient_schema.jsonify(patient)
    




if __name__== "__main__":
    app.run(debug=True)
