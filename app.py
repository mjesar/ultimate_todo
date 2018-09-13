from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(65))
    description=db.Column(db.String(90))
    complete = db.Column(db.Boolean)

db.create_all()


@app.route('/', methods=['GET'])
def get_all():
    title = Todo.query.all()

    output = []

    for todo in title:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['title'] = todo.title
        todo_data['description'] = todo.description
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'title' : output})

@app.route('/todo/<id>', methods=['GET'])

def get_one_by_one( id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['title'] = todo.title
    todo_data['description'] = todo.description
    todo_data['complete'] = todo.complete
    return jsonify(todo_data)

@app.route('/todo', methods=['POST'])
def create_title():
    data = request.get_json()

    new_title = Todo(title=data['title'], description=data['description'], complete=False)
    db.session.add(new_title)
    db.session.commit()

    return jsonify({'message' : "Todo created!"})

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({'message' : 'Not found!'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message' : 'title deleted'})

@app.route('/todo/<id>', methods=['PUT'])
def complete_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo.complete = True
    db.session.commit()

    return jsonify({'message' : 'title completed!'})


if __name__ == '__main__':
    app.run(debug=True)