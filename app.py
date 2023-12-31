from flask import Flask, render_template, request, redirect, url_for
import memcache

app = Flask(__name__)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def generate_task_key(task):
    # Use the first few characters of the task name and due date for a concise key
    task_name = task['task'][:4]  # Use the first 4 characters of the task name
    due_date = task['due_date']
    task_key = f"{task_name}_{due_date}"
    return task_key

@app.route('/')
def index():
    all_task_keys = mc.get('all_task_keys') or []
    
    tasks = {}
    for key in all_task_keys:
        task = mc.get(key)
        if task is not None:
            tasks[key] = task

    blocked_tasks = {key: task for key, task in tasks.items() if task.get('status') == 'Blocked'}
    in_review_tasks = {key: task for key, task in tasks.items() if task.get('status') == 'In Review'}
    done_tasks = {key: task for key, task in tasks.items() if task.get('status') == 'Done'}
    
    return render_template('index.html', blocked_tasks=blocked_tasks, in_review_tasks=in_review_tasks, done_tasks=done_tasks)

@app.route('/add', methods=['POST'])
def add():
    new_task = {
        'task': request.form.get('task'),
        'due_date': request.form.get('due_date'),
        'status': 'Blocked'  # Default status is set to 'Blocked'
    }

    # Extract TTL from the form data, or set a default value if not provided
    ttl = int(request.form.get('expiration_time', 60))  # Default TTL is 60 seconds

    # Generate a unique key for the new task
    task_key = generate_task_key(new_task)

    # Store the task in Memcached using the generated key and set TTL
    mc.set(task_key, new_task, time=ttl)

    # Update the list of all task keys
    all_task_keys = mc.get('all_task_keys') or []
    all_task_keys.append(task_key)
    mc.set('all_task_keys', all_task_keys)

    return redirect(url_for('index'))

@app.route('/move/<task_key>/<new_status>')
def move(task_key, new_status):
    tasks = mc.get(task_key)  # Retrieve the individual task using its key
    all_task_keys = mc.get('all_task_keys') or []

    if task_key in all_task_keys and tasks:
        tasks['status'] = new_status
        mc.set(task_key, tasks)

    return redirect(url_for('index'))

@app.route('/delete/<task_key>')
def delete(task_key):
    tasks = mc.get(task_key)  # Retrieve the individual task using its key
    all_task_keys = mc.get('all_task_keys') or []

    if task_key in all_task_keys:
        # Remove the task key from the list of all task keys
        all_task_keys.remove(task_key)
        mc.set('all_task_keys', all_task_keys)

    if tasks:
        # Delete the individual task
        mc.delete(task_key)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
