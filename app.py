from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd

#Creates connections
rds_connection_string = "postgres:postgres@localhost:5432/corona_db"
engine = create_engine(f'postgresql://{rds_connection_string}')

#Creates a dataframe from sql query
df=pd.read_sql_query('select * from corona_virus',con=engine)

#Creates App
app = Flask(__name__)

#First Decorator, home page
@app.route("/")
def welcome():

    #Returns text on page for all routes
    return (
        f"Welcome to the Corona Virus API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/all_data<br/>"
        f"/api/v1.0/<Province><br/>"
    )

#Gives out all data and turns it into a table
@app.route("/api/v1.0/all_data")
def all_data():

    results = df.to_html()

    return (results)

#Uses user input to filter Province/State specific information
@app.route("/api/v1.0/<Province>")
def province(Province):
    
    #Query specific state
    df_state = pd.read_sql_query(f'''select * from corona_virus where corona_virus."Province/State" = '{Province}' ''',con=engine)
    
    results = df_state.to_html()

    return (results)

#Need it
if __name__ == "__main__":
    app.run(debug=True)
