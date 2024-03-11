from flask import Flask, request, redirect, url_for, session, Response
from flask import render_template
from flask import current_app as app
from application.functions import validate_email, valid_password, line_plot, song_plot
from application.models import User, Song, Playlist, PlaylistData,Album, Admin, Votes
from .database import db
from sqlalchemy import func
from datetime import datetime, timedelta
# from application.models import Article

@app.route("/",methods=["GET","POST"])
def home_login():
  if request.method=="GET":
    return render_template("home_login.html")
  elif request.method=="POST":
    u_name=request.form['user_name']
   #  print(request.form)
    password=request.form['pwd']
    user=User.query.filter_by(user_name=u_name).first()
    if not user:
        return "user name does not exist"
   #  print(user)
    if password==user.password:
      session['user_id'] = user.user_id
      # if user.creator==1:
      #   return redirect(url_for('home_creator'))
      return redirect(url_for('home'))
   #  print(u_name)
    return "Invalid password"
  else:
     return "Error"
   #  print("Error check")
@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method=="GET":
    return render_template('home_sign_up.html')
  elif request.method=="POST":
    name=request.form['name']
    username=request.form['user_name']
    email=request.form['email']
    password=request.form['pwd']
    c=0
    if request.form.get('creator'):
        c = 1
    if (not validate_email(email)):
        return render_template('home_sign_up.html')
    users = User.query.filter_by(user_name=username).first()
    if users:
      #   print(users)
        return "User Exists"
    email_check = User.query.filter_by(email=email).first()
    if email_check:
        return "Email exists"
    if (not valid_password(password)):
        return "password not correct"
    new_user=User(name=name,user_name=username,email=email,password=password,creator=c,joined= datetime.now().date())
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home_login'))
  else:
     return "Error"
   #  print("Error check")
@app.route("/home/creator", methods=["GET", "POST"])
def home_creator():
    usr_id = session.get('user_id')
    usr = User.query.filter_by(user_id=usr_id).first()
    u=User.query.all()
    songs_uploaded = Song.query.filter_by(uploaded_by=usr_id)

    if request.method == "GET":
        albums = Album.query.filter_by(uploaded_by=usr_id)
        return render_template("home_creator.html", songs_uploaded=songs_uploaded, albums=albums,user=u)

    elif request.method == "POST":
        song_name = request.form['s_name']
        song = request.files['song']
        song_data = song.read()
        lyrics = request.form['lyrics']
        album = request.form['Album']
        current_datetime = datetime.now().date()
      #   print(current_datetime)
        if album == "Independent":
            s = Song(song_name=song_name, song=song_data, uploaded_by=usr.user_id, lyrics=lyrics,date=current_datetime,upvote=0,downvote=0)
        elif album == "Current_album":
            # Check if the album with the specified name exists
            album_id = request.form['album_id']
            existing_album = Album.query.filter_by(album_id=album_id).first()

            if not existing_album:
                return "Invalid album name"

            s = Song(song_name=song_name, song=song_data, uploaded_by=usr.user_id, lyrics=lyrics, albums=existing_album.album_id,date=current_datetime,upvote=0,downvote=0)
        else:
            if request.form['album_name'] == "":
                return "Enter album name"
                
            a = Album(album_name=request.form['album_name'], uploaded_by=usr_id)
            db.session.add(a)
            db.session.commit()

            s = Song(song_name=song_name, song=song_data, uploaded_by=usr.user_id, lyrics=lyrics, albums=a.album_id,date=current_datetime,upvote=0,downvote=0)

        db.session.add(s)
        db.session.commit()
      #   print(s.song_id)
        return redirect(url_for('home_creator'))
@app.route('/logout')
def logout():
   session.pop('user_id', None)
   return redirect(url_for('home_login'))
@app.route("/home")
def home():
   u=session['user_id']
   s = Song.query.order_by(Song.date.desc()).all()
   flag=0
   if User.query.filter_by(user_id=u).first().flag==1:
      flag=1
   usrs=User.query.all()
   playlists=Playlist.query.filter_by(user_id=u)
   creator=User.query.filter_by(user_id=u).first()
   creator=creator.creator
   # print((usrs[0].user_id))
   # print(s)
   return render_template("home_user.html",songs=s,usrs=usrs,playlists=playlists,creator=creator,flag=flag)
@app.route('/play_audio/<int:song_id>')
def play_audio(song_id):
    # Assuming id is the primary key of your Song model
    audio_data = Song.query.filter_by(song_id=song_id).first()
    if audio_data:
        audio_data = audio_data.song
        def generate():
            yield audio_data
        return Response(generate(), mimetype="audio/mp3")
    else:
        return "Song not found", 404
@app.route('/upvote/<int:id>')
def upvote(id):
   u=session['user_id']
   s=Song.query.filter_by(song_id=id).first()
   l=Votes.query.filter_by(user_id=u,song_id=id).first()
   if l:
      if l.up_down==0:
         l.up_down=1
         s.downvote-=1
         s.upvote+=1
         db.session.commit()
   else:
      l=Votes(song_id=id,user_id=u,up_down=1)
      db.session.add(l)
      s.upvote+=1
      db.session.commit()
   return redirect(url_for('home'))
@app.route('/downvote/<int:id>')
def downvote(id):
   u=session['user_id']
   s=Song.query.filter_by(song_id=id).first()
   l=Votes.query.filter_by(user_id=u,song_id=id).first()
   if l:
      if l.up_down==1:
         l.up_down=0
         s.downvote+=1
         s.upvote-=1
         db.session.commit()
   else:
      l=Votes(song_id=id,user_id=u,up_down=1)
      db.session.add(l)
      s.downvote+=1
      db.session.commit()
   return redirect(url_for('home'))         
    
@app.route("/home/my_playlists",methods=["GET","POST"])
def playlists():
   u=session['user_id']
   s=Song.query.all()
   playlists=Playlist.query.filter_by(user_id=u)
   if request.method=="GET":
    return render_template("playlist.html",all_songs=s,playlists=playlists)
   elif request.method=="POST":
      playlist_name = request.form['p_name']
      songs = request.form.getlist('songs[]')
      pl = Playlist(user_id=u, playlist_name=playlist_name)
      db.session.add(pl)
      db.session.commit()
      for song_id in songs:
          pl_data = PlaylistData(playlist_id=pl.playlist_id, song_id=song_id)
          db.session.add(pl_data)
      db.session.commit()
      return redirect(url_for('playlists'))
@app.route("/home/playlist/<int:playlist_id>")
def playlist_data(playlist_id):
   # print (playlist_id)
   playlist=Playlist.query.filter_by(playlist_id=playlist_id).first()
   x=[]
   playlists_songs=PlaylistData.query.filter_by(playlist_id=playlist_id)
   # print(playlists_songs[0])
   songs=[]
   for i in playlists_songs:
      # print(i)
      songs+=[Song.query.filter_by(song_id=i.song_id).first()]
   # print(songs)
   return render_template("playlistdata.html",songs=songs,playlist=playlist)
@app.route('/edit/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
   song=Song.query.filter_by(song_id=song_id).first()
   if request.method=="POST":
    song.song_name=request.form['name']
    db.session.commit()
    return redirect(url_for('home'))
   return render_template('edit.html', song=song)
@app.route('/delete/<int:song_id>', methods=['GET', 'POST'])
def delete_song(song_id):
   song=Song.query.filter_by(song_id=song_id).first()
   playlist_data=PlaylistData.query.filter_by(song_id=song_id)
   for data in playlist_data:
        db.session.delete(data)  # Use delete to remove objects from the session

   db.session.delete(song)
   db.session.commit()
   return redirect(url_for('home'))
@app.route('/edit_lyrics/<int:song_id>',methods=["GET","POST"])
def edit_lyrics(song_id):
   if request.method=="POST":
      s=Song.query.filter_by(song_id=song_id).first()
      s.lyrics=request.form['lyrics']
      db.session.commit()
      return redirect(url_for('home_creator'))
   return render_template('edit_lyrics.html')
@app.route('/home/readlyrics/<int:song_id>')
def read_lyrics(song_id):
   s=Song.query.filter_by(song_id=song_id).first()
   return render_template("lyrics.html",lyrics=s.lyrics)
@app.route('/home/creator/albums')
def albums():
   usr=session['user_id']
   alb=Album.query.filter_by(uploaded_by=usr)
   return render_template('albums.html',album=alb)
@app.route('/home/creator/albums/<int:id>')
def album_data(id):
   s=Song.query.filter_by(albums=id)
   return render_template('album_data.html',songs=s)
@app.route('/home/search', methods=["GET", "POST"])
def search():
    u=session['user_id']
    ur=User.query.filter_by(user_id=u).first()
    u=User.query.all()
    if request.method == "GET":
        return render_template("search_results.html",creator=ur.creator,user=u)
    else:
      s = Song.query.all()
      if request.form['search_text']=='song':
      #   print("searching")
        searched = []
        k=request.form['txt']
      #   print(k)
        for i in s:
            # print(i.song_name)
            k=k.lower()
            l=len(k)
            if i.song_name.lower()[:l] == k.lower():
                searched.append(i)
      #   print(searched)
        return render_template('search_results.html', songs=searched,val=0,creator=ur.creator,user=u)
      elif request.form['search_text']=='artist':
         u=User.query.filter_by(user_name=request.form['txt'])
         # print("***")
         # print(u)
         songs=[]
         u_id=[]
         for i in u:
            u_id+=[i.user_id]
            for y in s:
                if y.uploaded_by==i.user_id:
                   songs+=[y]
         return render_template('search_results.html',songs=songs,val=0,creator=ur.creator,user=u)
      elif request.form['search_text']=='album':
         alb=Album.query.filter_by(album_name=request.form['txt'])
         songs=[]
         for i in alb:
            for y in s:
               if y.albums==i.album_id:
                  songs+=[y]
         return render_template('search_results.html',songs=songs,albums=alb,val=0,creator=ur.creator,user=u)
      else:
         plt=Playlist.query.all()
         playlist=[]
         for i in plt:
            k=request.form['txt']
            k=k.lower()

            l=len(k)
            if i.playlist_name.lower()[:l]==k.lower():
               playlist+=[i]
         return render_template('search_results.html',playlists=playlist,val=1,creator=ur.creator,user=u)
@app.route("/home/account")
def account():
   usr=session['user_id']
   user_info=User.query.filter_by(user_id=usr).first()
   return render_template('accounts.html',user_info=user_info,creator=user_info.creator)
@app.route("/home/account/creator")
def become_creator():
   # print(session['user_id'])
   u=User.query.filter_by(user_id=session['user_id']).first()
   u.creator=1
   db.session.commit()
   return redirect(url_for('home_creator'))
@app.route('/edit_album/<int:song_id>',methods=["GET","POST"])
def edit_album(song_id):
   if request.method=="POST":
      s=Song.query.filter_by(song_id=song_id).first()
      # print(request.form['Album'])
      if request.form['Album']=="Independent":
         # print("independent")
         s.albums=None
         db.session.commit()
      elif request.form['Album']=="Current_album":
         #  print("current")
          album_id = request.form['txt']
          existing_album = Album.query.filter_by(album_id=album_id).first()

          if not existing_album:
              return "Invalid album name"

          s.albums=album_id
          db.session.commit()
      else:
      #   print("new")
        alb=Album(album_name=request.form['txt'],uploaded_by=session['user_id'])
        db.session.add(alb)
        db.session.commit()
        s.albums=alb.album_id
        db.session.commit()
      return redirect(url_for('home_creator'))
   return render_template('edit_album.html')
@app.route('/admin_login',methods=["GET","POST"])
def admin_login():
   if request.method=="POST":
      name=request.form['name']
      password=request.form['password']
      admin=Admin.query.filter_by(admin_name=name).first()
      if not admin:
         return "Name not valid"
      if password!=admin.password:
         return "password not valid"
      return redirect(url_for('admin'))
   return render_template('admin_login.html')
@app.route('/admin',methods=["GET","POST"])
def admin():
   u = User.query.all()
   curr = datetime.now().date()
   bins = [0, 0, 0]
   x = timedelta(days=30)
   for user in u:
      if curr - user.joined < x:
         bins[2] += 1
      elif curr - user.joined < (x * 2):
         bins[1] += 1
      elif curr - user.joined < (x * 3):
         bins[0] += 1
   line_plot(bins)
   s=Song.query.all()
   bins=[0,0,0]
   for songs in s:
      if curr-songs.date>(x*3):
         bins[0]+=1
         bins[1]+=1
         bins[2]+=1
      elif curr-songs.date>(x*60):
         if curr-songs.date>(x*3):
          bins[0]+=1
          bins[1]+=1
      else:
         bins[0]+=1
   song_plot(bins)
   return render_template('home_admin.html')
@app.route('/admin/allsongs')
def allsongs():
   s=Song.query.all()
   a=Album.query.all()
   u=User.query.all()
   return render_template('all_songs.html',songs=s,albums=a,users=u)
@app.route('/admin/allsongs/remove/<int:id>')
def remove_song(id):
   s=Song.query.filter_by(song_id=id).first()
   p=PlaylistData.query.filter_by(song_id=id)
   for x in p:
      db.session.delete(x)
      db.session.commit()
   db.session.delete(s)
   db.session.commit()
   return redirect(url_for('allsongs'))
@app.route('/admin/allsongs/flag/<int:id>')
def flag(id):
   u=User.query.filter_by(user_id=id).first()
   u.flag=1
   db.session.commit()
   return redirect(url_for('allsongs'))
@app.route('/admin/allalbums')
def all_albums():
   a=Album.query.all()
   return render_template('all_albums.html',albums=a)
@app.route('/admin/allalbums/remove/<int:id>')
def remove_album(id):
   a=Album.query.filter_by(album_id=id).first()
   s=Song.query.filter_by(albums=id)
   for x in s:
      remove_song(x.song_id)
   db.session.delete(a)
   db.session.commit()
   return redirect(url_for('all_albums'))
@app.route('/home/liked_songs')
def liked():
   u=session['user_id']
   liked=Votes.query.filter_by(user_id=u)
   al=Album.query.all()
   users=User.query.all()
   songs=[]
   for i in liked:
      if i.up_down==1:
         songs+=[Song.query.filter_by(song_id=i.song_id).first()]
   return render_template('liked_songs.html',liked=songs,albums=al,users=users)
# @app.route("/", methods=["GET", "POST"])
# def articles():
#     articles = Article.query.all()    
#     return render_template("articles.html", articles=articles)

# @app.route("/articles_by/<user_name>", methods=["GET", "POST"])
# def articles_by_author(user_name):
#     articles = Article.query.filter(Article.authors.any(username=user_name))
#     return render_template("articles_by_author.html", articles=articles, username=user_name)
