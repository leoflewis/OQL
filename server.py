from flask import Flask, jsonify, request
import cx_Oracle, os
from flask_cors import CORS, cross_origin
from OQL.Query import *

cx_Oracle.init_oracle_client(lib_dir="C:\Program Files\instantclient_21_12")
 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

primarykeys = {"skaterstats": "playerid", "team": "teamid", "game": "gameid", "player": "player_id"}

def getConnection():
    try:
        username = os.environ.get("zOracleDb_user")
        password = os.environ.get("zOracleDb_Pass")
        connect_string = "tcps://adb.us-phoenix-1.oraclecloud.com:1522/fssjrzpe2zgsiup_seis630fall2023_high.adb.oraclecloud.com?" \
        "wallet_location=C:/Users/fleon/OneDrive/Desktop/UST/SEIS 630/Wallet&retry_delay=3"
        connection = cx_Oracle.connect(username, password, connect_string)
        print("Successfully connected to Oracle Database")
        return connection
    except Exception as e:
        print(str(e))
        return None

def respond(col_names, rows):
    json_data = [col_names]
    for row in rows:
        json_data.append(dict(zip(col_names,row)))
    return jsonify(json_data)

def getQueryFromArgs(args: dict):
    q = Query(args['table'])
    vals = []
    q.Select(primarykeys[args['table'].lower()], args['table'], "id")
    q.Select("*", args['table'])
    if 'order' in args.keys():
        for orders in args['order'].split('|'):
            order = orders.split(',')
            if order[1].lower() == "desc":
                q.OrderBy(order[0], Orders.Descending)
            else:
                q.OrderBy(order[0], Orders.Ascending)


    if 'select' in args.keys():
        for column in args['select'].split(','):
            q.Select(column)
    
    if 'group' in args.keys():
        q.GroupBy(args['group'])

    if 'join' in args.keys():
        join = args['join'].split(",")
        q.Join(join[0], JoinOperators.INNER, join[2], join[3])

    print(q.getQuery())
    return q.getQuery(), vals
    
@cross_origin()
@app.route('/')
def selectPlayer():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        sql, vals = getQueryFromArgs(request.args.to_dict())
        cursor.execute(sql, vals)
        rows = cursor.fetchall()
        col_names = [col[0] for col in cursor.description]
        cursor.close()

        if len(col_names) == len(rows[0]):
            return respond(col_names, rows)
    except KeyError as error:
        return str(KeyError)
    except Exception as error:
        print('Error occurred')
        return str(error)


if __name__ == '__main__':
    app.run()
