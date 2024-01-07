
# Task Manager Flask App

This is a simple task manager web application built using Flask and Memcached for caching.

## Overview

The application allows users to add tasks, upvote or downvote tasks, change task status, and view tasks sorted by due date or votes. Memcached is used for caching tasks and key-value pairs.

## Prerequisites

- Python 3.x
- Flask
- Memcached
- A modern web browser

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/task-manager-flask.git
    ```

2. Navigate to the project directory:

    ```bash
    cd task-manager-flask
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

## Features

- **Add Task:** Users can add tasks with due dates and an initial status of "Blocked."

- **Upvote/Downvote:** Users can increase or decrease the complexity of a task by upvoting or downvoting.

- **Sort Tasks:** Tasks can be sorted by due date or votes.

- **Change Status:** Users can change the status of a task (Blocked, In Review, Done).

- **Extend Expiration:** Users can extend the expiration time of a task.

- **Delete Task:** Users can delete a task.

- **View All Keys:** Users can view all key-value pairs stored in the cache.

- **Flush Cache:** Users can flush all items from the cache.

- **Memcached Stats:** View Memcached statistics.

## File Structure

- **app.py:** Main Flask application file.
- **index.html:** HTML template for the main task manager page.
- **sorted_list.html:** HTML template for displaying sorted tasks.
- **show_all_keys.html:** HTML template for displaying all key-value pairs.
- **templates/:** Directory for HTML templates.

