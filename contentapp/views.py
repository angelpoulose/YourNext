from django.shortcuts import render,redirect
from .models import *
from .movies import *
from .books import *

genre_map = fetch_genre_map()

def index(request):
    return render(request,"index.html")

def login(request):
    msg=""
    
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists()==True:
            user=User.objects.get(email=email)
            if user.check_password(password) == True:
                request.session["uid"] = user.id
                return redirect("/userhome")
            else:
                msg="Password Incorrect"
        else:
            msg="Email is not registered"
    return render(request,"login.html",{"msg":msg})

def registration(request):
    msg=""
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        selected_genres = request.POST.getlist('genre')
        genres = ""
        for i in selected_genres:
            genres+=i+","
        if User.objects.filter(email=email).exists() != True and User.objects.filter(username=username).exists() != True :
            user=User.objects.create_user(username=username,email=email,password=password,genres=genres)
            user.save()
            msg = "Registration Successfull"
        else:
            msg="Username or Email Already Exists"

        
    return render(request,"registration.html",{'msg':msg})

def userhome(request):
    user = User.objects.get(id=request.session['uid'])
    msg = ""
    if request.method == 'GET':
        request.session['shown_movies'] = []
        request.session['shown_books'] = []

    shown_movies = set(request.session.get('shown_movies', []))
    shown_books = set(request.session.get('shown_books', []))
    watched_titles = set(
        Watched.objects.filter(user=user, content='movie').values_list('title', flat=True)
    )

    genres = [g.strip() for g in user.genres.split(',') if g.strip()]
    movie_keywords = {'movie', 'watch', 'film', 'cinema'}
    book_keywords = {'book', 'read', 'novel', 'story'}

    if request.method == 'POST':
        query = request.POST.get('query', '').strip().lower()

        if not query:
            request.session['shown_movies'] = []
            request.session['shown_books'] = []
            msg = "Type something like 'watch movie' or 'read book'"
            return render(request, "userhome.html", {'user': user, 'msg': msg})

        words = set(query.split())

        if words & movie_keywords:
            genre_ids = [str(genre_map[g.lower()]) for g in genres if g.lower() in genre_map]
            movies = get_movies(genre_ids, 'en')
            filtered = [m for m in movies if m['title'] not in shown_movies and m['title'] not in watched_titles]
            shown_movies.update(m['title'] for m in filtered)
            request.session['shown_movies'] = list(shown_movies)
            return render(request, "userhome.html", {'user': user, 'movies': filtered})

        elif words & book_keywords:
            books = get_books_by_genres(genres, exclude_titles=shown_books)
            shown_books.update(b['title'] for b in books)
            request.session['shown_books'] = list(shown_books)
            return render(request, "userhome.html", {'user': user, 'books': books})

        else:
            msg = "Type something like 'watch movie' or 'read book'"
            return render(request, "userhome.html", {'user': user, 'msg': msg})

    books = get_books_by_genres(genres, exclude_titles=[])
    return render(request, "userhome.html", {'user': user, 'books': books})







def toggleWatched(request):
    id = request.GET['id']
    content = request.GET['type']
    user = User.objects.get(id=request.session['uid'])
    if Watched.objects.filter(title =id).exists() != True:
        watched = Watched.objects.create(user = user,content=content,title=id)
        watched.save()
    else:
        watched = Watched.objects.get(title=id)
        watched.delete()
    return redirect('/userhome')


def profile(request):
    user = User.objects.get(id=request.session['uid'])
    msg=""
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        genres = request.POST['genres']
        languages = request.POST['languages']
        user.username = username
        user.email = email
        user.genres = genres
        user.languages = languages
        user.save()
        msg="Profile Updated"
    return render(request,"profile.html",{'user':user,"msg":msg})

def watched(request):
    user = User.objects.get(id=request.session['uid'])
    watched_ids = Watched.objects.filter(user=user).values_list('title', flat=True)
    movies=get_movies_by_ids(watched_ids)
    print(movies)
    return render(request,"watched.html",{"movies":movies})


def about(request):
    return render(request,"about.html")