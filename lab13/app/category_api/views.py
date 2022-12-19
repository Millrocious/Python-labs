from datetime import datetime
from flask import make_response, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required
from .. import db
from functools import wraps

from ..auth.models import User
from ..todo.models import Category

from . import category_bp


def admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'admin' and auth.password == 'admin_pass':
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@category_bp.route('/token', methods=['POST'])
def get_token():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    if user.verify_password(auth.password):
        token = create_access_token(identity=user.username)
        return jsonify(token=token)

    return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()

    categories_list = [dict(id=category.id, name=category.name) for category in categories]

    return jsonify(categories_list)


@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    new_category_data = request.get_json()
    print(new_category_data)

    if not new_category_data:
        return {'message': 'No input data provided'}, 400

    name = new_category_data.get('name')
    if not name:
        return jsonify({'message': 'Not key with name'}), 422

    category = Category.query.filter_by(name=name).first()
    if category:
        return jsonify({'message': f'Категорія з назвою {name} існує'}), 400

    try:
        category_new = Category(name=name)
        db.session.add(category_new)
        db.session.commit()
    except:
        return jsonify({'message': f'Невідома помилка на стороні сервера'}), 500

    category_add = Category.query.filter_by(name=name).first()

    return jsonify(dict(id=category_add.id, name=category_add.name)), 201


@category_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)

    return jsonify(dict(id=category.id, name=category.name))


@category_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def edit_category(id):
    new_category_data = request.get_json()

    name = new_category_data.get('name')
    if not name:
        return jsonify({'message': 'Not key with name'})

    category = Category.query.get_or_404(id)

    try:
        category.name = name
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'Category already exist'}), 409

    return jsonify({'id': id, 'name': name}), 204


@category_bp.route('/categories/<int:id>', methods=['DELETE'])
@admin
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
    except:
        return jsonify({'message': f'Server issue'}), 500

    return jsonify({'message': 'The category has been deleted!'}), 204