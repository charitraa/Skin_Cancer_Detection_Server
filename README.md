# 🧪 Skin Cancer Detection Server (Django + CNN)

This repository contains a Django REST API server for detecting skin cancer using a trained CNN model. The server provides authentication APIs and an endpoint to upload a skin image and get a prediction (Malignant or Benign).

## 🚀 Features

- User authentication (login, update user, user list).
- Prediction API (`api/predict/`) for skin cancer detection.
- Uses SQLite3 database (default Django DB).
- Loads a trained CNN model (`skin_cancer_cnn.h5`) for prediction.

## 📂 Folder Structure

```
Skin_Cancer_Detection_Server/
│── core/                     # Main app for APIs
│   ├── migrations/           
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── predictions.py        # Prediction logic using CNN model
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py               # API routes
│   └── views.py              # API views
│
│── models/                   # Trained ML/DL models
│   └── skin_cancer_cnn.h5    # CNN model (add manually)
│
│── Skin_Detection/           # Django project folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── env/                      # Virtual environment (not included in repo)
│── db.sqlite3                # SQLite database
│── manage.py                 # Django management script
│── requirements.txt          # Python dependencies
│── test2.png                 # Sample image for testing
│── test3.png                 # Sample image for testing
└── .gitignore
```

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/charitraa/Skin_Cancer_Detection_Server.git
   cd Skin_Cancer_Detection_Server
   ```

2. **Create virtual environment & install dependencies**  
   ```bash
   python -m venv env
   source env/bin/activate   # Linux/Mac
   env\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Database setup**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Add trained model**  
   Create a `models/` folder and place your trained model inside:  
   ```
   models/skin_cancer_cnn.h5
   ```

## ▶️ Running the Server

```bash
python manage.py runserver
```

Server will run at:  
👉 `http://127.0.0.1:8000/`

## 🔑 Authentication APIs

- **POST** `/api/login/` → Login user
- **POST** `/api/auth/` → Signup user
- **GET** `/api/user/all/` → List users
- **PUT** `/api/user/update/` → Update user
- **GET** `/api/user/me/` → user Details

## 🩺 Prediction API

**Endpoint:**  
**POST** `/api/predict/`

**Request (multipart/form-data):**  
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -F "file=@test2.png"
```

**Response:**  
```json
{
  "class_label": "Malignant"
  "confidence_score":"0.00"
}
```

**Logic:**  
```python
class_label = "Malignant" if prediction > 0.5 else "Benign"
```

## 🖼️ Example Folder Structure with Images

```
Skin_Cancer_Detection_Server/
│── test2.png   # Example input image
│── test3.png   # Example input image
```

## ✅ Requirements

- Python 3.9+
- Django 4+
- TensorFlow / Keras
- Django REST Framework
