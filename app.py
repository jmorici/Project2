import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import requests

#from flask import Flask, jsonify, render_template
#from flask_sqlalchemy import SQLAlchemy

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# The database URI
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/emoji.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/FPA_FOD_20170508.sqlite"

db = SQLAlchemy(app)


class Fires(db.Model):
    __tablename__ = 'fires'

    # OBJECTID,FOD_ID,FPA_ID,SOURCE_SYSTEM_TYPE,SOURCE_SYSTEM,NWCG_REPORTING_AGENCY,NWCG_REPORTING_UNIT_ID,NWCG_REPORTING_UNIT_NAME,SOURCE_REPORTING_UNIT,SOURCE_REPORTING_UNIT_NAME,LOCAL_FIRE_REPORT_ID,LOCAL_INCIDENT_ID,FIRE_CODE,FIRE_NAME,ICS_209_INCIDENT_NUMBER,ICS_209_NAME,MTBS_ID,MTBS_FIRE_NAME,COMPLEX_NAME,FIRE_YEAR,DISCOVERY_DATE,DISCOVERY_DOY,DISCOVERY_TIME,STAT_CAUSE_CODE,STAT_CAUSE_DESCR,CONT_DATE,CONT_DOY,CONT_TIME,FIRE_SIZE,FIRE_SIZE_CLASS,LATITUDE,LONGITUDE,OWNER_CODE,OWNER_DESCR,STATE,COUNTY,FIPS_CODE,FIPS_NAME,Shape

    id = db.Column(db.Integer, primary_key=True)
    LATITUDE = db.Column(db.Integer)
    LONGITUDE = db.Column(db.Integer)
    FIRE_YEAR = db.Column(db.Integer)
    STAT_CAUSE_CODE = db.Column(db.String)
    STATE = db.Column(db.String)
    FIRE_SIZE = db.Column(db.Integer)
    FIRE_SIZE_CLASS = db.Column(db.String)
    FIPS_CODE = db.Column(db.String)
    STAT_CAUSE_DESCR = db.Column(db.String)

    def __repr__(self):
        return '<Fires %r>' % (self.name)

# Create database tables


@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")


@app.route("/mapdata")
def mapdata():
    # results = db.session.query(Fires.LATITUDE, Fires.LONGITUDE, Fires.FIRE_YEAR, Fires.STAT_CAUSE_CODE, Fires.STATE,
    #                            Fires.FIRE_SIZE, Fires.FIRE_SIZE_CLASS, Fires.FIPS_CODE).all() #.filter(Fires.FIRE_YEAR == 2013)
    results = db.session.query(Fires.FIRE_YEAR, Fires.STATE, Fires.FIRE_SIZE, Fires.FIPS_CODE).limit(10000).all()
    firedata = []
    for result in results:
        # firedata.append({
        #     # "LAT": result[0],
        #     # "LON": result[1],
        #     "Year": result[2],
        #     # "Cause": result[3],
        #     "State": result[4],
        #     "Size": result[5],
        #     # "class": result[6],
        #     "FIPS": result[7]
        # })
        firedata.append({
            "Year": result[0],
            "State": result[1],
            "Size": result[2],
            "FIPS": result[3]
        })
    return jsonify(firedata)


@app.route('/us')
def usMap():
    r = requests.get('https://d3js.org/us-10m.v1.json')
    return r.text


@app.route('/states')
def stateNames():
    r = requests.get(
        'https://gist.githubusercontent.com/mbostock/4090846/raw/07e73f3c2d21558489604a0bc434b3a5cf41a867/us-state-names.tsv')
    return r.text


@app.route("/fire_causes")
def fire_causes_data():
    # """Return fire year and cause"""

 #   query for the fire cause data

    #    results = db.session.query(Fires.FIRE_SIZE_CLASS,func.count(Fires.STAT_CAUSE_DESCR)).\
    #      group_by(Fires.FIRE_SIZE_CLASS).all()
    results = db.session.query(Fires.STAT_CAUSE_DESCR, func.count(Fires.STAT_CAUSE_DESCR), Fires.STATE).\
        group_by(Fires.STAT_CAUSE_DESCR).all()

    cause = [result[0] for result in results]
    count = [result[1] for result in results]
    states = [result[2] for result in results]

    # Generate the plot trace
    plot_trace = {
        "x": cause,
        "y": count,
        "state": states,
        "type": "bar"
    }
    return jsonify(plot_trace)


@app.route("/firedata")
def firedata():
    results = db.session.query(Fires.LATITUDE, Fires.LONGITUDE, Fires.STATE, Fires.FIRE_YEAR,
                               Fires.STAT_CAUSE_DESCR, Fires.FIRE_SIZE_CLASS, Fires.FIRE_SIZE).limit(50000).all()

    firedata = []
    for result in results:
        firedata.append({
            "latitude": round(result[0], 4),
            "longitude": round(result[1], 4),
            "State": result[2],
            "Year": result[3],
            "Cause": result[4],
            "Class": result[5],
            "Size": result[6]
            
        })
    return jsonify(firedata)


if __name__ == '__main__':
    app.run(debug=True)
