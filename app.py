import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)
# Flask Routes
@app.route("/")
def home_page():
    return(
        f"(George SQLAlchemy Challenge - Step 2 Climate App). <br><br>"
        f"Available Routes: <br>"

        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from the last year in data set. <br><br>"

        f"/api/v1.0/stations<br/>"
        f"Returns a list of stations. <br><br>"

        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations for last year in data set. <br><br>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given date range."
   ) 

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(func.max(Measurement.date)).first()
    last_date2=str(last_date)
    year = int(last_date2[2]+last_date2[3]+last_date2[4]+last_date2[5])
    month = int(last_date2[7]+last_date2[8])
    day = int(last_date2[10]+last_date2[11])
    query_date = dt.date(year, month, day) - dt.timedelta(days=365)
    maxdate = dt.date(year, month, day)
    prcp_list = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > query_date).filter(Measurement.date <= maxdate).\
    all()
    session.close()
    return jsonify(prcp_list)

 
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stationhits = session.query(Measurement.station, Station.name, func.count(Measurement.station)).\
    filter(Measurement.station == Station.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
    return jsonify(stationhits)   
    
if __name__ == "__main__":
    app.run(debug=True)