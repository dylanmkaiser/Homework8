import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
# engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
# Home page - List all available api routes.
    return """
        Available Routes:</a><br/>
        <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>
        <a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>
        <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
        <a href="/api/v1.0/2013-10-31">/api/v1.0/<start></a><br/>
        "Input start date as yyyy-mm-dd"<br/>
        <a href="/api/v1.0/2013-10-31/2014-01-01">/api/v1.0/<start>/<end></a><br/>
        "Input start and end dates as yyyy1-mm1-dd1/yyyy2-mm2-dd2"<br/>
    """

# Return a dictionary of last 12 months of precipitation data
@app.route("/api/v1.0/precipitation")

def precipitation_data():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_12_mo = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > previous_year).\
        order_by(Measurement.date).all()

    precipitation = []

    for value in precip_12_mo:
        precip_dict = {}
        precip_dict["date"] = value.date
        precip_dict["prcp"] = value.prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

# Return a list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations_data():
    stations = session.query(Station.station,Station.name)
    
    all_stations = []
    for station in stations:
        all_stations.append(station)

    return jsonify(all_stations)

# Query for the dates and temperature observations from a year from the last data point.
@app.route("/api/v1.0/tobs")
def tobs_data():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_12_mo = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > previous_year).\
        order_by(Measurement.date).all()

    temperature = []
    for value in temp_12_mo:
        temp_dict = {}
        temp_dict["date"] = value.date
        temp_dict["tobs"] = value.tobs
        temperature.append(temp_dict)

    return jsonify(temperature)

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    temp_start = session.query(*sel).\
        filter(Measurement.date > start).all()
    
    return jsonify(temp_start, f"Your start date: {start}")

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    sel2 = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    temp_start_end = session.query(*sel2).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end).all()
    
    return jsonify(temp_start_end, f"Your start and end dates: {start}/{end}")

if __name__ == '__main__':
    app.run(debug=True)