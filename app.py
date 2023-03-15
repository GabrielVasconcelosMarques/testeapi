from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    videos = db.relationship('Video', backref='user', lazy=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    video_id = db.Column(db.String(20))
    video_link = db.Column(db.String(100))
    channel_title = db.Column(db.String(50))
    thumbnail = db.Column(db.String(100))
    duration = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserResource(Resource):
    def get(self, user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            videos = [{'title': video.title, 'video_id': video.video_id,
                       'video_link': video.video_link, 'channel_title': video.channel_title,
                       'thumbnail': video.thumbnail, 'duration': video.duration} for video in user.videos]
            return {'name': user.name, 'email': user.email, 'videos': videos}
        except:
            return {'message': 'Usuário não encontrado'}
        

    def post(self):
        name = request.json['name']
        email = request.json['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return {'id': user.id, 'name': user.name, 'email': user.email}

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.name = request.json['name']
        user.email = request.json['email']
        db.session.commit()
        return {'id': user.id, 'name': user.name, 'email': user.email}

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}


class VideoResource(Resource):
    def post(self, user_id):
        title = request.json['title']
        video_id = request.json['video_id']
        video_link = request.json['video_link']
        channel_title = request.json['channel_title']
        thumbnail = request.json['thumbnail']
        duration = request.json['duration']
        video = Video(title=title, video_id=video_id, video_link=video_link,
                      channel_title=channel_title, thumbnail=thumbnail, duration=duration,
                      user_id=user_id)
        db.session.add(video)
        db.session.commit()
        return {'id': video.id, 'title': video.title, 'video_id': video.video_id,
                'video_link': video.video_link, 'channel_title': video.channel_title,
                'thumbnail': video.thumbnail, 'duration': video.duration, 'user_id': video.user_id}


api.add_resource(UserResource, '/user/<int:user_id>', '/user')
api.add_resource(VideoResource, '/user/<int:user_id>/video')

if __name__ == '__main__':
    app.run(debug=True)


# /user/<int:user_id>/video
'''
{
    "title": "Vídeo do João",
    "video_id": "1234567890",
    "video_link": "https://www.youtube.com/watch?v=1234567890",
    "channel_title": "Canal do João",
    "thumbnail": "https://i.ytimg.com/vi/1234567890/hqdefault.jpg",
    "duration": "5:43"
}
'''
# http://127.0.0.1:5000/user/1
'''
{
    "name": "João Silva",
    "email": "joao.silva@example.com"
}
'''