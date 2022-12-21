#import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request

#Database setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base() 
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Homepage 
@app.route("/")
def welcome():
   """List all available api routes.""" 
   return (
    f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
   )

@app.route("/api/v1.0/precipitation")
def precipitation ():
    """JSON of Rain from LY"""

    # Calculate the date one year from the last date in data set.
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores 
    LY_rain = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > last_year_date ).\
    all()

    #Creating dictionary
    prcp = []
    prcp_date = []


    for rain, date in LY_rain:
        prcp.append(rain)
        prcp_date.append(date)
    
    prcp_dict = dict(zip(prcp, prcp_date))

   
    
    #close session
    session.close()

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations ():
    """JSON of stations"""
    #query to obtain the data
    all_stations = session.query(station.name).distinct().all()
    
    #Creating Dictionary
    station_list = list(np.ravel(all_stations))

    session.close()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs ():
    """JSON of tobs for LY"""
    #Query to obtain data
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    LY_tobs= session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > last_year_date).\
    all()
    #Creating dictionary

    tobs_dates = []
    tobs_temp = []

    for date, temp in LY_tobs:
        tobs_dates.append(date)
        tobs_temp.append(temp)

    tobs_dict = dict(zip(tobs_dates, tobs_temp))

    session.close()

    return jsonify(tobs_dict)

if __name__ == '__main__':
    app.run(debug=True)



