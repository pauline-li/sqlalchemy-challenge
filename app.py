import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 
from sqlalchemy import inspect
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
        f"/api/v1.0/<start><br/>"
        f" /api/v1.0/<start>/<end>"
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


if __name__ == '__main__':
    app.run(debug=True)

