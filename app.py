from flask import Flask,render_template,request
import pickle
import numpy as np

app=Flask(__name__)

with open('models/knn.pkl','rb') as f:
    model=pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        gender = int(request.form['gender'])           # 0 for Female, 1 for Male
        device_type = int(request.form['device_type']) # 0=mobile,1=desktop,2=tablet
        ad_position = int(request.form['ad_position']) # numerical position id
        browsing_history = float(request.form['browsing_history']) # number of past visits
        time_of_day = int(request.form['time_of_day']) #  hour in 0-23 format

        features = np.array([[age, gender, device_type, ad_position, browsing_history, time_of_day]])

        prediction_prob = model.predict_proba(features)[0][1]
        prediction = model.predict(features)[0]

        result = "Ad Clicked" if prediction == 1 else "Not Clicked"
        confidence = round(prediction_prob * 100, 2)

        return render_template('index.html', prediction_text=f"{result} (Confidence: {confidence}%)")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)