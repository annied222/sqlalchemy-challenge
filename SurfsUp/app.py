import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
 
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
 
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
 
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    all_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()

    precip = {date: prcp for date, prcp in all_prcp}

    return jsonify(precip) 

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()

    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(measurement.date,measurement.tobs)\
        .filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= year_ago).all()
    session.close()

    station_temp = list(np.ravel(tobs))

    return jsonify(station_temp)

if __name__ == "__main__":
    app.run(debug=True)

