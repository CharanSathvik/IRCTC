# IRCTC
Railway Management System API

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL Database
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- PyJWT

### Step-by-Step Setup

1. *Clone the Repository*
    bash
    git clone https://your-repo-link.git
    cd railway-management-system
    

2. *Create a Virtual Environment*
    bash
    python3 -m venv venv
    source venv/bin/activate  # For Mac/Linux
    venv\Scripts\activate  # For Windows
    

3. *Install Dependencies*
    bash
    pip install -r requirements.txt
    

4. *Setup Environment Variables*
    Create a .env file and add the following:
    plaintext
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=mysql+pymysql://username:password@localhost/railway
    ADMIN_API_KEY=your_admin_api_key
    

5. *Run Migrations*
    bash
    flask db upgrade
    

6. *Start the Application*
    bash
    flask run
    

## API Endpoints

### 1. *Register User*  
- *POST* /register
- *Body*: { "username": "user1", "password": "password123" }

### 2. *Login User*  
- *POST* /login
- *Body*: { "username": "user1", "password": "password123" }
- *Returns*: { "token": "<JWT_TOKEN>" }

### 3. *Add a New Train (Admin Only)*  
- *POST* /trains
- *Headers*: x-api-key: <ADMIN_API_KEY>
- *Body*: { "name": "Express 101", "source": "Station A", "destination": "Station B", "total_seats": 100 }

### 4. *Get Train Availability*  
- *GET* /trains?source=Station A&destination=Station B

### 5. *Book a Seat*  
- *POST* /book
- *Headers*: Authorization: Bearer <JWT_TOKEN>
- *Body*: { "train_id": 1, "seats": 2 }

## Running Tests (Optional)

To run tests, use the following command:
bash
pytest
yaml
Copy code

---
