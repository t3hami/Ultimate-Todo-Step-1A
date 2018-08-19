from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

mlab_uri = 'mongodb://root:123456seven@ds125602.mlab.com:25602/todo'
local_uri = 'mongodb://localhost/todo'

app.config['MONGO_DBNAME'] = 'todo'
app.config['MONGO_URI'] = local_uri

mongo = PyMongo(app)


@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        unserialize_tasks = mongo.db.tasks.find({})
        serialize_tasks = []
        for task in unserialize_tasks:
            serialize_tasks.append({
                'id': str(task['_id']),
                'title': task['title'],
                'description': task['description'],
                'done': task['done']
            })
        return jsonify(serialize_tasks)

    elif request.method == 'POST':
        task = {
            'title': request.json['title'],
            'description': request.json['description'],
            'done': False
        }
        mongo.db.tasks.insert(task)
        return jsonify({'status': 'Success'})

    else:
        pass


@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    if request.method == 'GET':
        task_cursor = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task_cursor:
            task = {
                '_id': str(task_cursor['_id']),
                'title': task_cursor['title'],
                'description': task_cursor['description'],
                'done': task_cursor['done']
            }
            return jsonify(task)

    elif request.method == 'PUT':
        mongo.db.tasks.save({
            '_id': ObjectId(task_id),
            'title': request.json['title'],
            'description': request.json['description'],
            'done': request.json['done']
            })
        return jsonify({'status': 'Success'})

    elif request.method == 'DELETE':
        mongo.db.tasks.remove({'_id': ObjectId(task_id)})
        return jsonify({'status': 'Success'})
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)