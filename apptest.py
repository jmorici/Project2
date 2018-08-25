import pandas as pd

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

    id = db.Column(db.Integer, primary_key=True)
    LATITUDE = db.Column(db.Integer)
    LONGITUDE = db.Column(db.Integer)
    FIRE_YEAR = db.Column(db.Integer)
    STAT_CAUSE_DESCR = db.Column(db.String)
    STATE = db.Column(db.String)
    FIRE_SIZE = db.Column(db.Integer)
    FIRE_SIZE_CLASS = db.Column(db.String)

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



@app.route("/firedata")
def firedata():
    results = db.session.query(Fires.LATITUDE, Fires.LONGITUDE, Fires.STATE, Fires.FIRE_YEAR, Fires.STAT_CAUSE_DESCR, Fires.FIRE_SIZE_CLASS, Fires.FIRE_SIZE).limit(100000).all()

    firedata = []
    for result in results:
        firedata.append({
            "latitude": round(result[0], 4),
            "longitude": round(result[1], 4),
            "State": result[2],
            "Year": result[3],
            "Cause": result[4],
            "Class": result[5],
            "Size": result[6],
            # "coordinates": [result[0], result[1]]
        })
    return jsonify(firedata)



if __name__ == '__main__':
    app.run(debug=True)
