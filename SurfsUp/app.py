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

#Correctly generate the engine to the correct sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
 
#Use automap_base() and reflect the database schema
Base = automap_base()
Base.prepare(autoload_with=engine)
 
#Correctly save references to the tables in the sqlite file (measurement and station)
measurement = Base.classes.measurement
station = Base.classes.station
 
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Display the available routes on the landing page
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"Start Date Route:</br>"
        f"/api/v1.0/""month-day-year</br>"
        f"Start Date and End Date Route:</br>"
        f"/api/v1.0/""month-day-year/month-day-year</br>"
    )

#A precipitation route that:
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    ##Returns json with the date as the key and the value as the precipitation
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    all_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    precip = {date: prcp for date, prcp in all_prcp}
    session.close()

    #Only returns the jsonified precipitation data for the last year in the database
    return jsonify(precip) 

#A stations route that:
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()

    all_stations = list(np.ravel(stations))

    #Returns jsonified data of all of the stations in the database
    return jsonify(all_stations)

#A tobs route that:
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #Returns jsonified data for the most active station (USC00519281)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(measurement.date,measurement.tobs)\
        .filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= year_ago).all()
    session.close()

    station_temp = list(np.ravel(tobs))

    #Only returns the jsonified data for the last year of data
    return jsonify(station_temp)

#A start route that:
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
#Accepts the start and end dates as parameters from the URL
def temp_stats(start = None, end = None):
    session = Session(engine)
    
    #Returns the min, max, and average temperatures calculated from the given start date to the given end date
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)



