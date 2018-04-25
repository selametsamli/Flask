from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt



app = Flask(__name__)

app.secret_key= "ybblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/selametsamli/Programlama/VSCode/FLASK/blog/blog/todo.db'

db = SQLAlchemy(app)


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

@app.route("/")
def index():
    article = [
        { "id":1,"title":5}]


    return  render_template("index.html", article = article)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/article/<string:id>")
def detail(id):
    return "Article Id: "+id


#Kayit Olma
@app.route("/register", methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form) 
    if request.method == "POST" and form.validate():

        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = sha256_crypt.encrypt(request.form.get("password"))   

        ekle = Todo(name = name,username=username,email=email,password=password)  

        db.session.add(ekle)
        db.session.commit()
        flash("Başarıyla kayıt oldunuz..","success")


        return redirect (url_for("index"))
    else:    
        return render_template("register.html", form = form)


# Tablodaki yerlerimizi belirliyoruz. 
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(15))
    email = db.Column(db.String(80))
    password = db.Column(db.String(15))


if __name__ == "__main__":
    db.create_all() #uygulama çalışmadan hemen önce tüm classları tablo olarak ekliyoruz.
    app.run(debug = True) 
