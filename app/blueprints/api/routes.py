from . import api
from app.models import Post
from app.models import User
from flask import request

@api.route('/')
def index():
    return 'Hi'

#endpoint to get all of the posts
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return [post.to_dict() for post in posts]


#allows you to get each individual post
@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'error': f'Post with the ID of {post_id} does not exist.'}, 404
    return post.to_dict()

@api.route('/posts', methods=['POST'])
def create_post():
    if not request.is_json:
        #check to see that the request body is json
        return {'error': 'Your request content-type must be application/json'}, 400
    #get the data from the request body
    data = request.json
    #validate the incoming data
    required_fields = ['title', 'body', 'user_id']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    #gets the data from the request body
    title = data.get('title')
    body = data.get('body')
    image_url = data.get('image_url')
    user_id = data.get('user_id')

    #creates a new post instance w the dta from the request
    new_post = Post(title=title, body=body, image_url=image_url, user_id=user_id)

    return new_post.to_dict(), 201

@api.route('/user', methods=["POST"])
def create_user():
    # Check to see that the request body is JSON aka application/json content-type
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    required_fields = ['first_name', 'last_name', 'username', 'password', 'email']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            # If the field is not in the request body, add that to missing fields list
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get the data from the request body
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Create a new Post instance with the data from the request
    new_user = User(first_name=first_name, last_name=last_name, username=username, password=password, email=email)

    # Return the new post as a JSON response
    return new_user.to_dict(), 201


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return {'error': f'User with the ID of {id} does not exist.'}, 404
    return user.to_dict()
