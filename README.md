# 🦴 Knee Osteoarthritis Detection using CNN (AlexNet Enhanced)

## 📌 Project Overview
This project is a deep learning-based medical image classification system designed to detect Knee Osteoarthritis (OA) from X-ray images. It uses a Convolutional Neural Network (CNN) model enhanced with AlexNet architecture to improve feature extraction and classification accuracy. The system helps in early detection of osteoarthritis, enabling timely medical intervention and reducing manual diagnostic effort.

---

## 🧠 Problem Statement
Knee Osteoarthritis is a common degenerative joint disease that affects mobility and quality of life. Manual diagnosis using X-rays can be time-consuming and subjective. This project automates the detection process using AI to provide fast and accurate classification of disease severity.

---

## ⚙️ How It Works
The system processes knee X-ray images through the following pipeline:
1. Image upload via web interface
2. Preprocessing (resizing, normalization, noise reduction)
3. Feature extraction using CNN (AlexNet-based architecture)
4. Model prediction and classification
5. Display of results on UI

The model classifies images into:
- Normal
- Mild Osteoarthritis
- Moderate Osteoarthritis
- Severe Osteoarthritis

---

## 🚀 Features
- Automated detection of Knee Osteoarthritis from X-ray images
- CNN model enhanced with AlexNet architecture
- High-accuracy image classification system
- Streamlit-based interactive web interface
- Fast prediction with real-time results
- Easy-to-use medical AI tool

---

## 🧠 Tech Stack
- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Pandas
- Streamlit
- CNN (Convolutional Neural Network)
- AlexNet Architecture

---

## 📂 Project Structure
- Backend: Model training, preprocessing, and inference logic
- Frontend: Streamlit web application interface
- Dataset: Knee X-ray image dataset
- Model Files: Trained weights (.pth files, stored locally due to size limits)

⚠️ Note: Large model files are not uploaded to GitHub due to size restrictions (100MB limit). They can be stored locally or shared via Google Drive or cloud storage.

---

## 🖥️ Workflow
Upload X-ray Image → Preprocessing → CNN Model Prediction → Output Classification → Display Result on Web UI

---

## 📊 Output Classes
- 🟢 Normal
- 🟡 Mild Osteoarthritis
- 🟠 Moderate Osteoarthritis
- 🔴 Severe Osteoarthritis

---

## 📈 Future Improvements
- Improve accuracy using advanced architectures (ResNet, EfficientNet)
- Deploy model on cloud platforms (AWS / Streamlit Cloud / Render)
- Integrate AI-based medical report generation
- Optimize model for real-time clinical applications
- Expand dataset for better generalization

---

## 🛠️ Installation & Setup
```bash
git clone https://github.com/bommepallipadmalatha/knee-osteoarthritis-detection-1-.git
cd knee-osteoarthritis-detection-1-
pip install -r requirements.txt
streamlit run app.py
