from flask import render_template, flash, request, redirect, url_for, session
from .forms import LoginForm, RegisterForm, ResetForm, EditForm, PostForm
from app import app, db, admin, models
from flask_admin.contrib.sqla import ModelView
import datetime
import logging


@app.route('/')
def index():
    app.logger.debug('Redirected to /index route. A redirect to /login should follow.')
    return redirect( url_for( 'login' ))


@app.route('/friends', methods = ['GET', 'POST'])
def friends():
    app.logger.debug('Redirected to /friends route')
    if 'key' in session:
        return render_template('friends.html', models = models.Account.query.all(),
            model = models.Account.query.get(session['key']),
                fs = models.Friends.query.filter_by( other_id = session['key']).all(),
                    fg = models.Friends.query.filter_by( this_id = session['key']).all())
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    app.logger.debug('Redirected to /profile route')
    if 'key' in session:
        posts = models.Post.query.filter_by( account_id = session['key']).all()
        return render_template('profile.html', model = models.Account.query.get(session['key']), posts = posts)
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/visit', methods = ['GET', 'POST'])
def visit():
    app.logger.debug('Redirected to /visit route')
    if 'key' in session:
        if request.args.get('id'):
            app.logger.info('New account id retrieved successfully')
            for m in models.Friends.query.filter_by(this_id = session['key']).all():
                if m.other_id == int(request.args.get('id')):
                    app.logger.info('Relationship between accounts found')
                    return render_template('visit-profile.html', followed = 0, model = models.Account.query.get(request.args.get('id')),
                        models = models.Account.query.all())
            return render_template('visit-profile.html', followed = 1,
                model = models.Account.query.get(request.args.get('id')), models = models.Account.query.all())
        else:
            app.logger.error('Failed to retrieve account id!')
            app.logger.warning('Redirecting to other profiles may be unavailable')
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/follow', methods = ['GET', 'POST'])
def follow():
    app.logger.debug('Redirected to /follow route')
    if 'key' in session:
        if request.args.get('id'):
            app.logger.debug('Args successfully received')
            f = models.Friends( this_id = session['key'], other_id = request.args.get('id'))
            models.Account.query.get(f.this_id).following += 1
            models.Account.query.get(f.other_id).followers += 1
            db.session.add(f)
            db.session.commit()
            app.logger.info('Relationship established')
            return redirect( url_for( 'friends' ))
        else:
            app.logger.error('Failed to retrieve account id!')
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/unfollow', methods = ['GET', 'POST'])
def unfollow():
    app.logger.debug('Redirected to /unfollow route')
    if 'key' in session:
        if request.args.get('id'):
            app.logger.debug('Args successfully received')
            f = models.Friends.query.filter_by( this_id = session['key'], other_id = request.args.get('id')).all()
            for t in f:
                db.session.delete(t)
            models.Account.query.get(session['key']).following -= 1
            models.Account.query.get(request.args.get('id')).followers -= 1
            db.session.commit()
            app.logger.info('Relationship successfully deleted')
            return redirect( url_for( 'friends' ))
        else:
            app.logger.error('Failed to retrieve account id!')
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    app.logger.debug('Redirected to /edit route')
    if 'key' in session:
        form = EditForm()
        if form.validate_on_submit():
            if form.name.data != '' or form.surname.data != '' or form.description.data != '':
                if form.name.data != '':
                    models.Account.query.get(session['key']).name = form.name.data
                if form.surname.data != '':
                    models.Account.query.get(session['key']).surname = form.surname.data
                if form.description.data != '':
                    models.Account.query.get(session['key']).description = form.description.data
                app.logger.info('Successfully changed profile details')
                db.session.commit()
            else:
                app.logger.info('Empty EditForm submitted')
                flash("• Please fill at least one field")
                return render_template('edit.html', model = models.Account.query.get(session['key']), form = form)
            flash("• Details changed successfully")
        return render_template('edit.html', model = models.Account.query.get(session['key']), form = form)
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/newpost', methods = ['GET', 'POST'])
def newpost():
    app.logger.debug('Redirected to /newpost route')
    if 'key' in session:
        form = PostForm()
        if form.validate_on_submit():
            p = models.Post( date = datetime.date.today(), description = form.description.data,
                account_id = models.Account.query.get(session['key']).id)
            models.Account.query.get(session['key']).np += 1
            db.session.add(p)
            db.session.commit()
            app.logger.info('New post created')
            flash("• Post created")
        return render_template('newpost.html', form = form, model = models.Account.query.get(session['key']))
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    app.logger.debug('Redirected to /logout route')
    if 'key' in session:
        session.pop('key', None)
        app.logger.info('Session key popped successfully')
        return redirect( url_for( 'login' ))
    else:
        app.logger.info('Unauthorized access attempted')
        return redirect( url_for( 'login' ))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    app.logger.debug('Redirected to /login route')
    form = LoginForm()
    if form.validate_on_submit():
        for m in models.Account.query.all():
            if m.username == form.username.data and m.password == form.password.data:
                app.logger.debug('Input matched with details in the database')
                session.pop('key', None)
                session['key'] = m.id
                app.logger.info('Login successful. New session key was acquired.')
                return redirect( url_for( 'profile' ))
        app.logger.info('Unsuccessful login attempt')
        flash("• Incorrect details")
    return render_template('login.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    app.logger.debug('Redirected to /register route')
    form = RegisterForm()
    if form.validate_on_submit():
        for m in models.Account.query.all():
            if m.username == form.username.data:
                app.logger.info('Registration with existing username attempted')
                flash("• This username already exists")
                return render_template('register.html', form = form)
        m = models.Account( name = form.name.data, surname = form.surname.data, username = form.username.data,
            password = form.password.data, description = "No information given", following = 0, followers = 0, np = 0)
        db.session.add(m)
        db.session.commit()
        app.logger.info('Successfully created a new account')
        flash("• Registration successful")
        return redirect( url_for( 'login' ))
    return render_template('register.html', form = form)


@app.route('/reset', methods = ['GET', 'POST'])
def reset():
    app.logger.debug('Redirected to /reset route')
    form = ResetForm()
    if form.validate_on_submit():
        for m in models.Account.query.all():
            if m.username == form.username.data and m.password == form.newpass.data:
                app.logger.info('A request to change password to the same one')
                flash("• You cannot change your password to the same one!")
                return render_template('reset.html', form = form)
            elif m.username == form.username.data:
                m.password = form.newpass.data
                db.session.commit()
                app.logger.info('Successfully changed password')
                flash("• Password changed successfully")
                return redirect( url_for( 'login' ))
        app.logger.info('Wrong username inputted')
        flash("• Wrong username")
    return render_template('reset.html', form = form)
