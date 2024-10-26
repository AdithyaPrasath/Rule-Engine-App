# Project Title

## Installation Instructions

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup Steps

1. **Clone the repository:**

   git clone https://github.com/your_username/your_repository.git
   cd your_repository
2. Create a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install dependencies: Create a requirements.txt file with the following content:

Flask
Flask-Mail
Werkzeug
itsdangerous
sqlite3
Then run:

pip install -r requirements.txt
4. Set up the database: Run the database setup script to create necessary tables:

python database_setup.py
5. Run the application: Start the Flask server:


python app.py
6. Access the application: Open your web browser and go to http://127.0.0.1:5000
