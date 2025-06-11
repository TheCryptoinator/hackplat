# Hackathon Management Platform

A Flask-based web application for managing hackathons, teams, and submissions.

## Features

- User authentication (login/register)
- Create and manage hackathons
- Team formation and management
- Project submissions
- Dashboard for users to track their activities

## Tech Stack

- Python 3.8+
- Flask (Web Framework)
- SQLite (Database)
- Flask-Login (Authentication)
- Bootstrap 5 (UI)
- Jinja2 (Templating)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database:
```bash
python hackathon_app.py
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
hackathon-platform/
├── hackathon_app.py      # Main application file
├── requirements.txt      # Project dependencies
├── README.md            # Project documentation
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── login.html       # Login page
    ├── register.html    # Registration page
    └── dashboard.html   # User dashboard
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 