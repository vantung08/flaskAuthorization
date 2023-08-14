from flask import Flask, request
from markupsafe import escape
from flask_cors import CORS
import psycopg2


app = Flask(__name__)
CORS(app)


def create_connection():
    host = 'localhost'
    port = '5432'
    database = 'nextjsblog'
    user = 'postgres'
    password = '1989'
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return connection


# @app.route('/')
# def test_db_connection():
#     try:
#         connection = create_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT version()')
#         db_version = cursor.fetchone()[0]
#         cursor.close()
#         connection.close()
#         return f'Successfully connected to PostgreSQL. Database version: {db_version}'
#     except (Exception, psycopg2.Error) as error:
#         return f'Error connecting to PostgreSQL: {error}'


@app.route('/users', methods=['GET', 'POST'])
def registration():
    user = request.get_json()
    first_name = user['firstName']
    last_name = user['lastName']
    email = user['email']
    password = user['password']

    connection = create_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (first_name, last_name, email, password))
    connection.commit()

    cursor.close()
    connection.close()

    return {'First Name: ': first_name,
            'Last Name: ': last_name,
            'Email: ': email,
            'Password: ':password
            }


    # if request.method == 'POST':
    #     # logic to push data to DB
    #     return {'First Name: ': user['firstName'],
    #             'Last Name: ': user['lastName'],
    #             'Email: ': user['email'],
    #             'Password: ':user['password']
    #             }
    # else:
    #     return ['Wrong http method']


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.get_json()
    email = user['email']
    password = user['password']

    connection = create_connection()
    cursor = connection.cursor()

    insert_query = 'SELECT email FROM users WHERE email = %s AND password = %s'
    cursor.execute(insert_query, (email, password))
    result = cursor.fetchone()

    if result:
        return {'Login status: ': 'Login successful'}
    else:
        return {'Login status: ': 'Login failed'}

    cursor.close()
    connection.close()


# if __name__ == '__main__':
#     app.run()

