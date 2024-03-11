from .database import db

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_name=db.Column(db.String,unique=True,nullable=False)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    creator=db.Column(db.Integer,nullable=False)
    joined=db.Column(db.Date)
    flag=db.Column(db.Integer)
    playlists=db.relationship('Playlist',backref='created_by',lazy=True)
    uploads=db.relationship('Song',backref='song_uploaded_by',lazy=True)
class Song(db.Model):
    __tablename__='songs'
    song_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    song_name=db.Column(db.String,nullable=False)
    uploaded_by=db.Column(db.Integer,db.ForeignKey('user.user_id'))
    song = db.Column(db.LargeBinary)
    lyrics=db.Column(db.String)
    albums=db.Column(db.Integer,db.ForeignKey('album.album_id'))
    date=db.Column(db.Date)
    upvote=db.Column(db.Integer)
    downvote=db.Column(db.Integer)
    playlists=db.relationship('PlaylistData',backref='songss',lazy=True)

class Votes(db.Model):
    __tablename__='likes'
    song_id=db.Column(db.Integer,db.ForeignKey('songs.song_id'),nullable=False,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)  
    up_down=db.Column(db.Integer,default=0)
    
class Playlist(db.Model):
    __tablename__='playlist'
    playlist_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    playlist_name=db.Column(db.String,nullable=False)
    playlist_data_entries = db.relationship('PlaylistData', backref='playlist', lazy=True)
    # songs=db.relationship('playlist_song',backref='song',lazy=True)
class PlaylistData(db.Model):
    __tablename__='playlist_data'
    playlist_id=db.Column(db.Integer,db.ForeignKey('playlist.playlist_id'),nullable=False,primary_key=True)
    song_id=db.Column(db.Integer,db.ForeignKey('songs.song_id'),nullable=False,primary_key=True)
class Album(db.Model):
    __tablename__='album'
    album_id=db.Column(db.Integer,autoincrement=True,primary_key=True, nullable=False)
    album_name=db.Column(db.String,nullable=False)
    uploaded_by=db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
class Admin(db.Model):
    __tablename__='admin'
    admin_id=db.Column(db.Integer,autoincrement=True,primary_key=True, nullable=False)
    admin_name=db.Column(db.String)
    password=db.Column(db.String)

