from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from models import db, Message
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Return all messages ordered by created_at in ascending order
        messages = Message.query.order_by(Message.created_at.asc()).all()
        if messages is not None:
            return jsonify([message.serialize() for message in messages]), 200
        else:
            return jsonify([]), 200

    elif request.method == 'POST':
        # Create a new message
        data = request.get_json()
        body = data.get('body')
        username = data.get('username')
        if body and username:
            new_message = Message(body=body, username=username)
            db.session.add(new_message)
            db.session.commit()
            return jsonify(new_message.serialize()), 201
        else:
            return jsonify({'error': 'Missing required parameters'}), 400

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'PATCH':
        # Update the body of the message
        data = request.get_json()
        body = data.get('body')
        if body:
            message.body = body
            db.session.commit()
            return jsonify(message.serialize()), 200

    elif request.method == 'DELETE':
        # Delete the message from the database
        db.session.delete(message)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(port=5555)
