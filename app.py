import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 
from sqlalchemy import distinct
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# #################################################
# # Flask Routes
# #################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (Start Date ~ Enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> (Start/End Date ~ Enter as YYYY-MM-DD)"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return last 12 months of data"""
    # Query to retrieve max date 
    Max_Date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date  
    # Query to go back a year from max date   
    Twelve_Months = dt.datetime.strptime(Max_Date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query last 12 months date and precipitaion data, order by descending 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= Twelve_Months)\
                  .order_by(Measurement.date.desc()).all()
    session.close()

    #Create a dictionary from the row data and append to a list of all_prcs
    all_prcp = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp        
        all_prcp.append(precipitation_dict)
    return jsonify(all_prcp)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    #results = session.query(func.count(distinct(Measurement.station))).all()
    session.close()
    
    # Return jason list
    unique_stations = list(np.ravel(results))
    return jsonify(unique_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return last 12 months data of most active station"""
    # Query for last 12 months date
    Max_Date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date  
    Twelve_Months = dt.datetime.strptime(Max_Date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query 12 months data on most active station 'USC00519281' 
    stationCount = session.query( Measurement.station, Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= Twelve_Months).\
                    filter(Measurement.station == 'USC00519281').\
                    order_by(Measurement.date.desc()).all()
 
    session.close()
    
    #Create a dictionary for the query result and append to a list of all_tobs
    all_tobs = []
    for station, date, tobs in stationCount:
        tobs_dict = {}
        tobs_dict["station"] = station 
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)
@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return Min, Max, and Avg of  temperature"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.round(func.avg(Measurement.tobs),2)).\
                   filter(Measurement.date >= start).all()
           
    #results = session.query(func.count(distinct(Measurement.station))).all()
    session.close()
    
    

    start_date = list(np.ravel(results))
    return jsonify(start_date)

if __name__ == '__main__':
    app.run(debug=True)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
