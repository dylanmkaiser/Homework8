import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
# List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation_data():
# Return a list of last 12 months of precipitation data
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

@app.route("/api/v1.0/stations")
def stations_data():
# Return a list stations from the dataset

    stations = session.query(Station.station,Station.name)
    
    all_stations = []
    for station in stations:
        all_stations.append(station)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs_data():

# Query for the dates and temperature observations from a year from the last data point.

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_12_mo = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > previous_year).\
        order_by(Measurements.date).all()

# Return a JSON list of Temperature Observations (tobs) for the previous year.

    temperature = []

    for value in temp_12_mo:
        temp_dict = {}
        temp_dict["date"] = temperature.date
        temp_dict["tobs"] = temperature.tobs
        temperature.append(temp_dict)

    return jsonify(temperature)


if __name__ == '__main__':
    app.run(debug=True)