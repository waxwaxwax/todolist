from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__)

# タスク管理の仮データベース
tasks = []

# 画像などを保存する assets フォルダを公開
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('content')
    if task_content:
        tasks.append({'content': task_content, 'done': False})  # タスクは未完了の状態で追加
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
    return redirect(url_for('index'))

# タスクの順番を変更
@app.route('/reorder', methods=['POST'])
def reorder():
    global tasks
    new_order = request.json.get("order", [])
    tasks = sorted(tasks, key=lambda x: next((o["position"] for o in new_order if int(o["id"]) == tasks.index(x)), len(tasks)))
    return jsonify({"status": "success", "tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)
