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


def generate_cache_key(sort_by):
    return f'tasks:sorted_by_{sort_by}'



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
    sorted_key = f'sorted_{sort_by}'
    all_task_keys = mc.get('all_task_keys') or []

    tasks = {key: mc.get(key) for key in all_task_keys if mc.get(key) is not None}

    if sort_by == 'due_date':
        sorted_tasks = sorted(tasks.values(), key=lambda x: x['due_date'])
    elif sort_by == 'votes':
        sorted_tasks = sorted(tasks.values(), key=lambda x: x.get('votes', 0), reverse=True)

    # Set an appropriate expiration time, e.g., 300 seconds (5 minutes)
    expiration_time = 300
    mc.set(sorted_key, sorted_tasks, time=expiration_time)

    return render_template('sorted_list.html', sorted_tasks=sorted_tasks)



@app.route('/sort-and-show/<sort_by>')
def sort_and_show(sort_by):
    sorted_key = f'sorted_{sort_by}'
    sorted_tasks = mc.get(sorted_key) or []

    return render_template('sorted_list.html', sorted_tasks=sorted_tasks)


@app.route('/move/<task_key>/<new_status>')
def move(task_key, new_status):
    tasks = mc.get(task_key)
    all_task_keys = mc.get('all_task_keys') or []

    if task_key in all_task_keys and tasks:
        tasks['status'] = new_status
        mc.replace(task_key, tasks)

    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run(debug=True)
