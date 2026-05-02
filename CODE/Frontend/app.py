from flask import Flask, url_for, redirect, render_template, request, session,flash,send_from_directory
import pymysql
import os
import pandas as pd
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image



class EnsembleModel(nn.Module):
    def __init__(self, num_classes):
        super(EnsembleModel, self).__init__()
        self.resnet50 = models.resnet50(pretrained=True)
        self.resnet50.fc = nn.Identity()  # Output: 2048 features
        
        self.mobilenetv2 = models.mobilenet_v2(pretrained=True)
        self.mobilenetv2.classifier[1] = nn.Identity()  # Output: 1280 features
        
        self.alexnet = models.alexnet(pretrained=True)
        self.alexnet.classifier[6] = nn.Identity()  # Output: 4096 features
        
        # Freeze the pre-trained model parameters
        for param in self.resnet50.parameters():
            param.requires_grad = False
        for param in self.mobilenetv2.parameters():
            param.requires_grad = False
        for param in self.alexnet.parameters():
            param.requires_grad = False
        
        # Adjust the classifier to match the combined feature size: 7424
        self.classifier = nn.Linear(7424, num_classes)

    def forward(self, x):
        resnet_features = self.resnet50(x)
        mobilenet_features = self.mobilenetv2(x)
        alexnet_features = self.alexnet(x)
        
        # Concatenate features
        combined_features = torch.cat((resnet_features, mobilenet_features, alexnet_features), dim=1)
        
        # Pass concatenated features through the custom classifier
        output = self.classifier(combined_features)
        return output

# Initialize the model and load the saved weights
num_classes = 5  # This should match the number of classes used during training
ensemble_model = EnsembleModel(num_classes=num_classes)
ensemble_model.load_state_dict(torch.load('ensemble_model.pth'))
ensemble_model.eval()  # Set the model to evaluation mode
data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

app = Flask(__name__)
app.secret_key = 'admin'

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="ROHITHKUMAR@123",
    port=3306,
    database='mediplus'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT UPPER(email) FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO users (email, password) VALUES (%s, %s)"
                values = (email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return render_template('home.html')
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
            myfile=request.files['file']
            fn=myfile.filename
            mypath=os.path.join('images/', fn)
            myfile.save(mypath)
            accepted_formated=['jpg','png','jpeg','jfif','JPG']

            if fn.split('.')[-1] not in accepted_formated:
                flash("Image formats only Accepted","Danger")
                return render_template("upload.html")
            
            image = Image.open(mypath).convert('RGB')
            image = data_transforms(image)
            image = image.unsqueeze(0)  # Add a batch dimension
            # Assuming the classes are 'Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe'
            class_names = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']

            with torch.no_grad():
                outputs = ensemble_model(image)
                _, predicted = torch.max(outputs, 1)
                prediction = class_names[predicted.item()]
                print(f'Predicted class: {prediction}')

            
            return render_template('upload.html', result=prediction,image_name=fn)

    return render_template('upload.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == '__main__':
    app.run(debug = True)