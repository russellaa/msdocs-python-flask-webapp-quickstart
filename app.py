import os
import pyodbc

from azure.identity import DefaultAzureCredential
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/sqltest')
def sqltest():
   print('Request for index page received')
   return render_template('submitdb.html')

@app.route('/sqltestoutput', methods=['POST'])
def sqltestoutput():
   name = request.form.get('name')

   if name:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://database.windows.net/.default").token       
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server={webapp-sql};"
            "Database=default;"
            "Authentication=ActiveDirectoryMsi;"
        )

        # Establish the connection
        conn = pyodbc.connect(conn_str, attrs_before={1256: bytearray(token, "UTF-8")})

        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Define your SQL query
        sql_query = "SELECT * FROM default"

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all the results
        rows = cursor.fetchall()

        # Iterate through the rows and print each row
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        conn.close()     
        print('Request for sqltest page received with name=%s' % name)
        return render_template('returndb.html', name = rows)
   else:
       print('Request for sqltest page received with no name or blank name -- redirecting')
       return redirect(url_for('sqltest'))

if __name__ == '__main__':
   app.run()
