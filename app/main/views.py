from flask import render_template, redirect, request, url_for, flash, abort
from . import main
from flask_login import login_required, current_user
from ..models import User, Blog
from .. import db
from .forms import BlogForm, UpdateProfile
from .. import db, photos

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(
        Blog.posted_on.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', blogs=blogs, title="Blogs | Welcome to G~Blog")


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
