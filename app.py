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
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    Max_Date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date  
       
    Twelve_Months = dt.datetime.strptime(Max_Date, '%Y-%m-%d') - dt.timedelta(days=365)
    #Begin_Date  = Twelve_Months.strftime('%Y-%m-%d')

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= Twelve_Months)\
                  .order_by(Measurement.date.desc()).all()
    session.close()
    #Create a dictionary from the row data and append to a list of all_passengers
  
    all_prcp = []
    for date, prcp in results:
        precipitaion_dict = {}
        precipitaion_dict["date"] = date
        precipitaion_dict["precipitation"] = prcp        
        all_prcp.append(precipitaion_dict)
    return jsonify(all_prcp)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    #results = session.query(func.count(distinct(Measurement.station))).all()
    session.close()
 
    unique_stations = list(np.ravel(results))
    return jsonify(unique_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    Max_Date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date  
    Twelve_Months = dt.datetime.strptime(Max_Date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    
    # results = session.query(Measurement.station).filter(Measurement.date >= Twelve_Months)\
    #               .order_by(Measurement.date.desc()).first()
    stationCount = session.query( Measurement.station, Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= Twelve_Months).\
                    filter(Measurement.station == 'USC00519281').\
                    order_by(Measurement.date.desc()).all()


    #results = session.query(func.count(distinct(Measurement.station))).all()
    session.close()
    
    all_tobs = []
    for station, date, tobs in stationCount:
        tobs_dict = {}
        tobs_dict["station"] = station 
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)
if __name__ == '__main__':
    app.run(debug=True)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.