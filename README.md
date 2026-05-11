# Web Nutrition Tracker

A self-hosted Flask web application for tracking daily nutrition intake, custom meals and historical progress.

## Overview

Web Nutrition Tracker is an open-source nutrition logging app designed for users who want a simple, customizable and privacy-friendly alternative to commercial nutrition trackers.

Users can create an account, add custom foods, record daily consumption, track calories/protein/fats/carbohydrates and view historical nutrition data through charts.

## Why I Built It

I wanted a nutrition tracker that was easy to customize and could be self-hosted without sending personal nutrition data to a third-party service.

The project was tested by several users. Their feedback was used to improve the food database workflow, chart behavior, suggestion list size and interface usability.

## features

- User registration and login
- Password hashing with Werkzeug
- User-specific meal database
- Add and delete custom foods
- Daily nutrition calculation
- Calories, carbohydrates, proteins and fats tracking
- Daily nutrition goals
- Historical nutrition charts
- Responsive Bootstrap interface
- Self-hosted SQLite database

Backend:

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Werkzeug

Frontend:

- HTML
- CSS
- JavaScript
- Bootstrap
- Chart.js
- Jinja2

Database:

- SQLite
- SQLAlchemy ORM

## Architecture

The application is structured around four main areas:

- Authentication
- Meal management
- Nutrition calculation
- Nutrition history and charts

Database models:

- `User`
- `UserMeal`
- `UserConsumption`
- `DailyGoalHistory`

A longer design summary is available in [`docs/PROJECT_BRIEF.md`](docs/PROJECT_BRIEF.md).

## Project Structure

```text
web_nutrition_tracker_v2/
  instance/
    default_database.json
  website/
    auth/
    nutrition/
    user/
    static/
      css/
      js/
    templates/
    __init__.py
    config.py
    models.py
  main.py
  requirements.txt
  .env.example
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment

Create a `.env` file or export environment variables manually. Example values are in `.env.example`:

```env
SECRET_KEY=change-me
DATABASE_URL=sqlite:///database.db
FLASK_DEBUG=1
```

## Run

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Testing

```bash
pytest
```

## Screenshots

Add screenshots to `docs/screenshots/` and include them here, for example:

```markdown
![Calculate page](docs/screenshots/calculate.png)
![History chart](docs/screenshots/history.png)
```

