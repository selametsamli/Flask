from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

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


app = Flask(__name__)
app.secret_key = "Blog"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "8Kmrl?53"
app.config["MYSQL_DB"] = "ssblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_PORT"] = '5000'

mysql = MySQL(app)

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

        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data) 

        cur = mysql.connection.cursor()

       # sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)" 

        cur.execute('''sorgu,(name,email,username,password)''')
        mysql.connection.commit()

        


        return redirect (url_for("index"))
    else:    
        return render_template("register.html", form = form)


if __name__ == "__main__":
    app.run(debug = True) 
