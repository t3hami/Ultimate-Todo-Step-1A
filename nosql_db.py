from flask_pymongo import PyMongo, ObjectId

class NoSQL:
    def __init__(self, app):
        mlab_uri = 'mongodb://root:123456seven@ds125602.mlab.com:25602/todo'
        local_uri = 'mongodb://localhost/todo'
        app.config['MONGO_DBNAME'] = 'todo'
        app.config['MONGO_URI'] = local_uri
        self.mongo = PyMongo(app)
    
    def get_all_tasks(self):
        unserialize_tasks = self.mongo.db.tasks.find({})
        serialize_tasks = []
        for task in unserialize_tasks:
            serialize_tasks.append({
                'id': str(task['_id']),
                'title': task['title'],
                'description': task['description'],
                'done': task['done']
            })
        return serialize_tasks
    
    def post_task(self, task):
        return self.mongo.db.tasks.insert(task)
    
    def is_task_present(self, task_id):
        try:
            task_cursor = self.mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        except:
            return False
        if task_cursor:
            return True
        else:
            False

    def get_task(self, task_id):
        task_cursor = self.mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task_cursor:
            task = {
                '_id': str(task_cursor['_id']),
                'title': task_cursor['title'],
                'description': task_cursor['description'],
                'done': task_cursor['done']
            }
        return task
    
    def delete_task(self, task_id):
        self.mongo.db.tasks.remove({'_id': ObjectId(task_id)})

    def update_task(self, task_id, task):
        self.mongo.db.tasks.save(task)