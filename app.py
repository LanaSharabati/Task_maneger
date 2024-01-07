from flask import Flask, render_template, request, redirect, url_for
import memcache
import time
import json



app = Flask(__name__)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)



def generate_task_key(task):
    # Normalize data and ensure uniqueness
    task_name = task['task'].lower().replace(' ', '-')[:20]  # Replace spaces with "-" and use the first 20 characters
    due_date = str(task['due_date'])  # Convert due_date to string
    votes = str(task['votes'])  # Convert votes to string

    # Incorporate a timestamp or a random component for additional uniqueness
    timestamp = str(int(time.time()))

    # Use a hash function for a fixed-length key
    key_components = [task_name, due_date, votes, timestamp]
    key_string = ':'.join(key_components)
    return key_string



def generate_cache_key(sort_by):
    return f'tasks:sorted_by_{sort_by}'


@app.route('/')
def index():
    all_task_keys = mc.get('all_task_keys') or {}

    tasks = {key: mc.get(key) for key in all_task_keys if mc.get(key) is not None}

    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    new_task = {
        'task': request.form.get('task'),
        'due_date': request.form.get('due_date'),
        'status': 'Blocked',
        'votes': 0  # Default votes is set to 0
    }

    ttl = int(request.form.get('expiration_time', 60))

    task_key = generate_task_key(new_task)

    if mc.get(task_key) is not None:
        mc.replace(task_key, new_task, time=ttl)
    else:
        mc.set(task_key, new_task, time=ttl)

        all_task_keys = mc.get('all_task_keys') or []
        all_task_keys.append(task_key)
        mc.set('all_task_keys', all_task_keys)

    return redirect(url_for('index'))



@app.route('/upvote/<task_key>')
def upvote(task_key):
    
    tasks = mc.get(task_key)
    mc.set_multi(tasks)

    if tasks:
        mc.incr('votes',1)
        # Increment the 'votes' field to simulate upvoting
        tasks['votes'] = mc.get('votes')
        mc.replace(task_key, tasks)

    return redirect(url_for('index'))


@app.route('/downvote/<task_key>')
def downvote(task_key):
    tasks = mc.get(task_key)
    mc.set_multi(tasks)

    if tasks:
        mc.decr('votes',1)
        # Decrement the 'votes' field, ensuring it doesn't go below 0 (simulate downvoting)
        tasks['votes'] = mc.get('votes')
        mc.replace(task_key, tasks)

    return redirect(url_for('index'))


@app.route('/sort-and-show/<sort_by>')
def sort_and_show_combined(sort_by):
    sorted_key = f'sorted:{sort_by}'
    all_task_keys = mc.get('all_task_keys') or []

    tasks = {key: mc.get(key) for key in all_task_keys if mc.get(key) is not None}

    if sort_by == 'due_date':
        sorted_tasks = sorted(tasks.values(), key=lambda x: x['due_date'])
    elif sort_by == 'votes':
        sorted_tasks = sorted(tasks.values(), key=lambda x: x.get('votes', 0), reverse=True)

    # Set an appropriate expiration time, e.g., 300 seconds (5 minutes)
    expiration_time = 30
    mc.set(sorted_key, sorted_tasks, time=expiration_time)

    return render_template('sorted_list.html', sorted_tasks=sorted_tasks)





@app.route('/move/<task_key>/<new_status>')
def move(task_key, new_status):
    tasks = mc.get(task_key)
    all_task_keys = mc.get('all_task_keys') or []

    if task_key in all_task_keys and tasks:
        tasks['status'] = new_status
        mc.replace(task_key, tasks)

    return "Success"  # You can return any response indicating success to the client


@app.route('/delete/<task_key>')
def delete(task_key):
    tasks = mc.get(task_key)
    all_task_keys = mc.get('all_task_keys') or []

    if task_key in all_task_keys:
        all_task_keys.remove(task_key)
        mc.set('all_task_keys', all_task_keys)

    if tasks:
        mc.delete(task_key)

    return redirect(url_for('index'))


@app.route('/show-all-keys')
def show_all_keys():
    all_keys = mc.get('all_task_keys') or []
    all_values = {key: mc.get(key) for key in all_keys if mc.get(key) is not None}

    sorted_due_date_key = 'sorted:due_date'
    sorted_votes_key = 'sorted:votes'

    sorted_due_date_values = mc.get(sorted_due_date_key) or []
    sorted_votes_values = mc.get(sorted_votes_key) or []

    return render_template('show_all_keys.html', all_values=all_values,
                           sorted_due_date_key=sorted_due_date_key, sorted_due_date_values=sorted_due_date_values,
                           sorted_votes_key=sorted_votes_key, sorted_votes_values=sorted_votes_values)


@app.route('/flush-cache', methods=['POST'])
def flush_cache():
    mc.flush_all()
    return redirect(url_for('show_all_keys'))

@app.route('/memcached-stats')
def memcached_stats():
    try:
        # Use mc.get_stats() instead of mc.stats()
        stats = mc.get_stats()
        # Extract statistics from the first server in the list (assuming you have only one server)
        stats = stats[0][1] if stats else {}
        return json.dumps(stats, indent=2), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return str(e), 500

@app.route('/extend-expiration/<task_key>', methods=['POST'])
def extend_expiration(task_key):
    ttl = int(request.form.get('expiration_time', 60))

    # Use mc.touch to update the expiration time for the specified task_key
    mc.touch(task_key, time=ttl)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)