from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId

def object_id_encoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'todo'
app.config['MONGO_URI'] = 'mongodb://root:123456seven@ds125602.mlab.com:25602/todo'

mongo = PyMongo(app)

@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        unserialize_tasks = mongo.db.tasks.find({})
        serialize_tasks = []
        for task in unserialize_tasks:
            serialize_tasks.append({
                #'id': task['_id'],
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
        task_cursor = mongo.db.tasks
        task_cursor.insert(task)
        return jsonify({'status': 'Success'})
    else:
        pass

@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)