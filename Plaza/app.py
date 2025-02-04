from flask import Flask,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_mail import Mail,Message
from form import RegistrationForm, LoginForm,ProductForm
from models import db,User,Product,Cart

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plaza.db'
app.config['SECRET_KEY'] = os.urandom(20)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail

@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(int(user_id))


@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products = products)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data,password = form.password.data,address = form.address.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login Successful', 'Success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, check your email and/or password', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out..', 'info')
    return redirect(url_for('home'))

@app.route('/add-product', methods = ['GET','POST'])
@login_required
def add_product(product_id = None):
    form = ProductForm()
    product = Product.query.get(product_id) if product_id else None
    if form.validate_on_submit():
        product = Product(name= form.name.data, description = form.description.data,price = form.price.data, stock = form.stock.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added!', 'Success')
        return redirect(url_for('home'))
    return render_template('add_product.html', form = form, product = product)

@app.route('/buy/<int:product_id>', methods = ['POSt'])
@login_required
def buy(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = Cart(user_id=current_user.id,product_id=product.id,quantity = 1)
    db.session.add(cart_item)
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return render_template('product_details.html', product = product)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)