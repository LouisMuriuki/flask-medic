# Medication Tracker Documentation

## Overview

This is a full-stack medication tracker application built with Python (Flask) for the backend and Tailwind CSS for the frontend. The inspiration behind this application is to address the issue of individuals forgetting to complete their prescribed medication dosages.

The Medication Tracker provides users with real-time visibility into their prescription progress and allows them to track details about the prescribing doctor.

## How to Run

### 1. Clone the Repository

Clone the repository to your local machine:
### 2. Install and configure tailwind

## run the following commands to set up Tailwind CSS:
~run "npm init -y" to create a package.json file
~run "npm i tailwindcss" to install tailwind
~run "npx tailwindcss init" to initialize tailwind
~Change the content section of the file such that the final tailwind.config.js looks something like this:
 content: ["./app/templates/*.html", "./app/static/src/*.js"],
Create "input.css" file inside css folder under static folder and add the following:
@tailwind base;
@tailwind components;
@tailwind utilities;
~Create an alias in the package.json inorder to listen to new tailwind changes i.e
"buildcss": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"

### 3.install flask packages
Run "pip install -r requirements.txt"

### 4.setup the Environmental variables
### 5.run "env\scripts\activate" to activate your environmental variables
### 6.run "python app/app.py" to start the project.