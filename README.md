# Auth Registration Challenge

## Stack
Python 3.12 + Django 5.2 + PostgreSQL 16 + Docker Compose

## Setup
git clone <url>
cd auth-registration-challenge
cp app/.env.example app/.env
docker compose up -d
docker compose run --rm web python manage.py migrate
 
## Usage
http://localhost:8003/register/

## Project Structure
app/accounts/    → Django app (models, views, forms)
app/config/      → Django project settings
app/static/      → CSS
app/templates/   → Shared HTML layout
