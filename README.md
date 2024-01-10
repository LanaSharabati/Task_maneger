
# Task Manager Flask App

This is a simple task manager web application built using Flask and Memcached for caching.

## Overview

The application allows users to add tasks, upvote or downvote tasks, change task status, and view tasks sorted by due date or votes. Memcached is used for caching tasks and key-value pairs.

## About Memcached

1 . Memcached is an open-source.
2 . high-performance.
3 . distributed memory caching system that is commonly used to speed up dynamic web applications by caching data and objects in memory.
4 . It stores data in a key-value format and is designed to be simple, lightweight, and scalable.

### Why Use Memcached in Task Manager App?

In the Task Manager app, Memcached is employed for several reasons:

1. **Caching Task Data:**
   - Memcached is used to cache task data, including details such as task name, due date, status, and complixty.
   - Caching helps reduce the load on the database and speeds up the retrieval of frequently accessed task information.

2. **Efficient complixty Counting:**
   - The app uses Memcached to store the number of complixty for each task.
   - This ensures efficient vote counting without the need to query the database each time a user upvotes or downvotes a task.

3. **Sorting and Filtering:**
   - Memcached is utilized to cache sorted task lists based on due date or votes.
   - This allows for quick retrieval of sorted task lists without the need to perform complex sorting operations on the entire dataset.

4. **Expiration Time Handling:**
   - Tasks in the app have expiration times, and Memcached is used to manage these expiration times efficiently.
   - The app extends or updates the expiration time of tasks without the need for frequent database updates.

5. **Improved Performance:**
   - By storing frequently accessed data in memory, Memcached significantly improves the overall performance of the task manager app.
   - It reduces the response time for user interactions, providing a more responsive and seamless user experience.

6. **Scalability:**
   - Memcached's distributed nature allows the task manager app to scale easily as the number of users and tasks increases.
   - It provides a scalable solution to handle a growing amount of data and user interactions.

## Prerequisites

- Python 3.x
- Flask
- Memcached
- A modern web browser

### Installing Memcached on Windows

1. Download the Memcached installer for Windows from [this link](https://github.com/downloads/danga/memcached/memcached-1.4.4-win32-bin.zip).

2. Extract the contents of the downloaded ZIP file to a directory of your choice, e.g., `C:\memcached`.

3. Open a command prompt as an administrator by right-clicking on the Command Prompt icon and selecting "Run as administrator."

4. Navigate to the directory where Memcached is installed (e.g., `C:\memcached`).

5. Install Memcached as a Windows service:

    ```bash
    memcached.exe -vv
    ```

6. Start the Memcached service:

    ```bash
    memcached
    ```

7. installl python memcached:
    ```bash
    pip install python-memcached
    ```


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

