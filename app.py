from flask import Flask, request
import mysql.connector
from omegaconf import OmegaConf

with open("team.sql", 'r') as file:
    sql = file.read()
    file.close()

app = Flask(__name__)
creds = OmegaConf.load('credentials.yaml')
cnx = mysql.connector.connect(user = creds['user']
                            , password = creds['password']
                            , host = creds['host']
                            , auth_plugin = creds['auth']
                            , database = creds['database'])

cursor = cnx.cursor(dictionary=True)

@app.get("/team")
def get_teams():
    cursor.execute("show tables")
    result = cursor.fetchall()
    
    if len(result) == 0:
        return {"teams": "No Teams Yet"}
    else: 
        return {"teams": [team['Tables_in_nba_teams'] for team in result]}
     
@app.post("/team")
def create_team():
    request_data = request.get_json()
    table_name = request_data["name"]
    cursor.execute(sql.format(**locals()))
    return get_teams(), 201

@app.get("/team/<string:team>")
def get_players(team):
    cursor.execute(f"SELECT player_name FROM {team}")
    result = cursor.fetchall()
    return {"players": [player['player_name'] for player in result]}

@app.post("/team/<string:team>/player")
def create_player(team):
    request_data = request.get_json()
    column_names = []
    values = []
    for col, val in request_data.items():
        print(col,val)
        column_names.append(col)
        if type(val) == str: val = f'"{val}"'
        else: val = str(val)
        values.append(val)
    column_names = ", ".join(column_names)
    values = ", ".join(values)

    sql = f"""
        INSERT INTO {team} ({column_names})
        VALUES ({values})
    """
    print(sql)
    cursor.execute(sql)
    cnx.commit()
    return get_players(team), 201
    




