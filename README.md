# Quiz Master
# QuizMaster

## 📌 Overview
QuizMaster is a web-based quiz management system built using Flask. It allows administrators to create subjects, chapters, and quizzes, and manage quiz-related data efficiently.

## 🚀 Features
- Add, edit, and delete subjects.
- Create chapters under subjects.
- Manage quizzes with assigned chapters and subjects.
- Display all existing quizzes in a user-friendly interface.

## 🛠️ Tech Stack
- Backend: Flask, SQLAlchemy
- Database: SQLite
- Frontend: HTML, CSS, Bootstrap, Jinja2 Templates

## 🔧 Installation & Setup
1. Clone the Repository
   ```sh
   git clone https://github.com/yourusername/QuizMaster.git
   cd QuizMaster
   ```
2. Create a Virtual Environment (Optional but Recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install Dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Set Up the Database
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. Run the Application
   ```sh
   flask run
   ```
   The application will be available at **http://127.0.0.1:5000/**

## 📂 Project Structure
```
QuizMaster/
│-- migrations/         # Database migrations
│-- templates/          # HTML Templates
│-- static/             # CSS, JS, Images
│-- app.py              # Main Flask app
│-- models.py           # Database models
│-- forms.py            # Flask Forms
│-- requirements.txt    # Required dependencies
│-- README.md           # Project documentation
```

## 🎯 Usage
- Navigate to **`/admin`** to manage subjects, chapters, and quizzes.
- Use the quiz form to add quizzes.
- Quizzes will be listed on the dashboard with edit and delete options.

## 🤝 Contributing
Feel free to open an issue or submit a pull request to enhance the project.

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).

