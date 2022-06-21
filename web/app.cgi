#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask, render_template, redirect, url_for, request

## PostgreSQL database adapter
import psycopg2
import psycopg2.extras

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist198966"
DB_DATABASE=DB_USER
DB_PASSWORD="ijxh6100"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/insert_nserie_ivm/", methods=["POST", "GET"])
def insert_nserie_ivm():
    if request.method == "POST":
        nserie = request.form["input"]
        return redirect(url_for("list_replenishment_events_from_ivm", nserie=nserie))
    else:
        return render_template("insert_nserie_ivm.html")

@app.route("/list_replenishment_events_from_ivm/<nserie>")
def list_replenishment_events_from_ivm(nserie):
    dbConn=None
    cursor=None

    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "SELECT * FROM evento_reposicao e WHERE e.num_serie = {n_serie};".format(n_serie = nserie)
        cursor.execute(query)
        rowcount=cursor.rowcount
        html = '''
        <!DOCTYPE html>
        <style>
        body {
            font-family: Montserrat;
            margin: 0;
        }
        /* Header/Logo Title */
        .header {
          padding: 15px;
          text-align: left;
          background: #55BCC9;
          color: white;
          font-size: 15px;
        }

        /* Page Content */
        .content {padding:20px;}

        .button {
          border: none;
          color: white;
          padding: 15px 50px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          border-radius: 5px;
        }

        .logo {float:right}

        .button1 {background-color: #4CAF50;} /* Green */
        .button2 {background-color: #55BCC9;} /* Blue */
        </style>
        <html>
            <head>
                <meta charset="utf-8">
                <title>List of categories - Python </title>
            </head>
            <div class="header">
                <h1>Databases Project - Delivery 3</h1>
            </div>
            <div class="content">
                <h1>Lista de Sub-Categorias de uma Super-Categoria</h1>
                <body style="padding:20px" >
                    <table border="5" cellspacing="5" style="background-color:#FFFFFF;">
                        <th style="background-color: #55BCC9; width: 500px; text-align: center;" colspan="7"><strong><span style="color: #ffffff;">Lista de Eventos de Reposição da IVM</span></strong></th>
                        <tbody>
                          <tr>
                            <th>EAN</th>
                            <th>nro</th>
                            <th>n_serie</th>
                            <th>fabricante</th>
                            <th>instante</th>
                            <th>unidades</th>
                            <th>TIN</th>
                          </tr>
        '''

        for record in cursor:
            html += f'''
                    <tr>
                        <td>{record[0]}</td>
                        <td>{record[1]}</td>
                        <td>{record[2]}</td>
                        <td>{record[3]}</td>
                        <td>{record[4]}</td>
                        <td>{record[5]}</td>
                        <td>{record[6]}</td>
                    </tr>
            '''
        html += '''
                        </tbody>
                    </table>
                </body>
            </div>
            <div>
                <br />
                <button class="button button2" onclick="document.location='../../app.cgi/'">Voltar</button>
            </div>
        </html>
        '''

        return html ## Renders the html string
    except Exception as e:
        return str(e) ## Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

    return html

@app.route("/insert_supercat/", methods=["POST", "GET"])
def insert_supercat():
    if request.method == "POST":
        super_cat = request.form["input"]
        return redirect(url_for("list_subcat_from_supercat", super_cat=super_cat))
    else:
        return render_template("insert_supercat.html")

@app.route("/list_subcat_from_supercat/<super_cat>")
def list_subcat_from_supercat(super_cat):

    dbConn=None
    cursor=None

    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "SELECT categoria FROM tem_outra WHERE super_categoria LIKE '{cat}';".format(cat = super_cat)
        cursor.execute(query)
        rowcount=cursor.rowcount
        html = '''
        <!DOCTYPE html>
        <style>
        body {
            font-family: Montserrat;
            margin: 0;
        }
        /* Header/Logo Title */
        .header {
          padding: 15px;
          text-align: left;
          background: #55BCC9;
          color: white;
          font-size: 15px;
        }

        /* Page Content */
        .content {padding:20px;}

        .button {
          border: none;
          color: white;
          padding: 15px 50px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          border-radius: 5px;
        }

        .logo {float:right}

        .button1 {background-color: #4CAF50;} /* Green */
        .button2 {background-color: #55BCC9;} /* Blue */
        </style>
        <html>
            <head>
                <meta charset="utf-8">
                <title>List of categories - Python </title>
            </head>
            <div class="header">
                <h1>Databases Project - Delivery 3</h1>
            </div>
            <div class="content">
                <h1>Lista de Sub-Categorias de uma Super-Categoria</h1>
                <body style="padding:20px" >
                    <table border="5" cellspacing="5" style="background-color:#FFFFFF;">
                        <th style="background-color: #55BCC9; width: 500px; text-align: center;" colspan="5"><strong><span style="color: #ffffff;">List of Categories</span></strong></th>
                        <tbody>
        '''

        for record in cursor:
            html += f'''
                    <tr>
                        <td>{record[0]}</td>
                    </tr>
            '''
        html += '''
                        </tbody>
                    </table>
                </body>
            </div>
            <div>
                <br />
                <button class="button button2" onclick="document.location='../../app.cgi/'">Voltar</button>
            </div>
        </html>
        '''

        return html ## Renders the html string
    except Exception as e:
        return str(e) ## Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

    return html


CGIHandler().run(app)
