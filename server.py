from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import joblib

app = Flask(__name__, static_url_path='/static')
CORS(app)

user_credentials = {
    'SwayamPendgaonkar': 'Swayam123',
    'TanushJadhav': 'Tanush123'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in user_credentials and user_credentials[username] == password:
            # Authentication successful, redirect to a success page
            return redirect(url_for('home'))
        else:
            # Authentication failed, stay on the login page
            return render_template('login.html', message='Invalid credentials')

    # Render the login page template
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if data:

        age = int(data.get('age'))

        prof = data.get('profession')
        if prof == 'artist':
            prof=1
        elif prof=='entertainment':
            prof=2
        elif prof=='lawyer':
            prof=3
        elif prof=='engineer':
            prof=4
        elif prof=='executive':
            prof=5
        elif prof=='marketing':
            prof=6
        elif prof=='homemaker':
            prof=7
        else:
            prof=8

        mar_status = data.get('maritalStatus')
        if mar_status == 'married':
            mar_status=1
        elif mar_status=='single':
            mar_status=2
        elif mar_status=='widowed':
            mar_status=3
        else:
            mar_status=4

        income = float(data.get('income'))

        exp = float(data.get('expenditure'))

        print(age, prof, mar_status, income, exp)
        # Perform prediction
        model = joblib.load('retired_model.pkl') 
        prediction = model.predict([[age, prof, mar_status, income, exp]])

        if prediction==0:
            prediction='Low'
        elif prediction==1:
            prediction='Average'
        else:
            prediction='High'

        return jsonify({'prediction': prediction})    
    
    return jsonify({'error': 'No data received'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)


