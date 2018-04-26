from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps



app = Flask(__name__)

app.secret_key= "ybblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/selametsamli/Programlama/VSCode/FLASK/blog/blog/todo.db'

db = SQLAlchemy(app)


#Kullanıcı giriş Decorator'ı

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function


# Kullanici Kayit Formu

class RegisterForm(Form):

    name = StringField("Isim Soyisim" ,validators=[validators.length(min = 4, max = 25)] )
    username = StringField("Kullanici Adi" ,validators=[validators.length(min = 5, max = 35)] )
    email = StringField("Email Adresi" ,validators=[validators.Email(message = "Lutfen Gecerli Bir Email Giriniz..")] )
    password = PasswordField("Parola:", validators=[
        validators.DataRequired(message = "Lutfen Bir Parola Belirleyin..."),
        validators.EqualTo(fieldname = "confirm",message = "Parola Uyusmuyor.")
    ])
    confirm = PasswordField("Parola Dogrula")

#Giriş Formu

class LoginForm(Form):
    username = StringField("Kullanıcı Adı:")
    password = PasswordField("Parola")

@app.route("/")
def index():
    article = [
        { "id":1,"title":5}]


    return  render_template("index.html", article = article)

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/dashboard")
@login_required
def dashboard():

    articles=Makale.query.order_by(Makale.author).all()


    return render_template("dashboard.html",articles=articles)


#Kayit Olma
@app.route("/register", methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form) 
    if request.method == "POST" and form.validate():

        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        ekle = Todo(name = name,username=username,email=email,password=password)  

        db.session.add(ekle)
        db.session.commit()
        flash("Başarıyla kayıt oldunuz..","success")


        return redirect (url_for("login"))
    else:    
        return render_template("register.html", form = form)



 #Login İşlemi

@app.route("/login", methods = ["GET","POST"])
def login():
    session['logged_in'] = False
    form = LoginForm(request.form)

    if request.method == "POST":
        name = form.username.data
        passw = form.password.data
        try:
            data =Todo.query.filter_by(username=name, password=passw).first()
            if data is not None:
               
                flash("Basarili","success")
                session['logged_in'] = True
                session["username"] = name
                return redirect (url_for("index"))
            else:
                flash("Böyle bir kullanıcı bulunmuyor ...","danger")
                return redirect(url_for("login"))
        except:
            flash("Böyle bir kullanıcı bulunmuyor ...","danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html",form = form)


# Logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


#Detay Sayfası

@app.route("/article/<string:id>")
def article(id):
    
    article=Makale.query.get(id)
    
    
    return render_template("article.html",article=article)



#Makale Sayfası
@app.route("/articles")
def articles():
    author = Makale.query.order_by(Makale.author).all()
    title = Makale.query.order_by(Makale.title).all()
    content = Makale.query.order_by(Makale.content).all()


    #articles = {"author":Makale.query.order_by(Makale.author).all(),"title" : Makale.query.order_by(Makale.title).all(),
     #"content":Makale.query.order_by(Makale.content).all()}

    return render_template("articles.html",title=title,author=author,content=content)
   



#Makale Ekleme
@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    
    if request.method == "POST" and form.validate():
        
        title = form.title.data
        content = form.content.data
        author = session["username"] 
        ekle = Makale(title = title,content=content,author=author)  

        db.session.add(ekle)
        db.session.commit()

        flash("Makale Başarıyla Eklendi..","success")
        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)



#Makale Form 
class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators=[validators.Length(min =5 , max = 50)])
    content = TextAreaField("Makale İçeriği",validators=[validators.Length(min = 10)])

        
# Tablodaki yerlerimizi belirliyoruz. 
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(15))
    email = db.Column(db.String(80))
    password = db.Column(db.String(15))


#makale için tablo oluşturuluyor
class Makale(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(20))
    content = db.Column(db.String(500))

if __name__ == "__main__":
    db.create_all() #uygulama çalışmadan hemen önce tüm classları tablo olarak ekliyoruz.
    app.run(debug = True) 
