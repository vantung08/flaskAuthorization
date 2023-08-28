from flask import Flask, request, session, jsonify
from markupsafe import escape
from flask_cors import CORS
import psycopg2
from itsdangerous import TimedSerializer, BadSignature, SignatureExpired


app = Flask(__name__)
CORS(app)
app.secret_key = 'abc123'

#Set the token expiration time (in seconds)
TOKEN_EXPIRATION_TIME = 3600 #1 hour


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.get_json()
    email = user['email']
    password = user['password']

    if verify_credentials(email, password):
        # token = generate_token(email)
        # session['token'] = token
        return jsonify({'success': True, 'message': 'Login successful.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'})

def generate_token(email):
    serializer = TimedSerializer(app.secret_key, expires_in=TOKEN_EXPIRATION_TIME)
    data = {'email': email}
    token = serializer.dumps(data).decode('utf-8')
    return token

def verify_credentials(email, password):
    connection = create_connection()
    cursor = connection.cursor()
    insert_query = 'SELECT email FROM users WHERE email = %s AND password = %s'
    cursor.execute(insert_query, (email, password))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

    cursor.close()
    connection.close()


@app.route('/protected')
def protected():
    token = session.get('token')
    if token:
        data = verify_and_decode_token(token)
        if data:
            email = data['email']
            return f'Projected content for user: {email}' #recheck
    return 'Unauthorized' #recheck

def verify_and_decode_token(token):
    serializer = TimedSerializer(app.secret_key)
    try:
        data = serializer.loads(token)
        return data
    except SignatureExpired:
        return None
    except BadSignature:
        return None

# if __name__ == '__main__':
#     app.run()

