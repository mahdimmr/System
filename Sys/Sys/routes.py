from Sys import app, bcrypt, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, logout_user, current_user, login_user
from Sys.models import User
from Sys.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from Sys import utils
import platform
import os
import psutil



#Login Route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form, title='Login')


#Register Route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)


#Route to Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    drive_storage = utils.get_system_storage('\\')
    machine_type = platform.machine()
    network_pcname = platform.node()
    cpu_realname = platform.processor()
    compiler_py = platform.python_compiler()
    pv = platform.python_branch()
    username_logon = os.getlogin()
    terminal = os.get_terminal_size()
    os_version = platform.win32_ver()
    locip = utils.local_ip()
    cpu_usage = psutil.cpu_percent()
    num_core = utils.cpu_core_count()
    imple_python = platform.python_implementation()
    os_name = platform.system()
    distro = utils.linux_distru()
    battery = utils.get_battery()
    percent_battery = utils.get_battery_percent()
    distro_linux = utils.linux_distru()
    ram = utils.ram_usage()

    return render_template('dashboard.html',  compiler_py=compiler_py, machine_type=machine_type,
                           network_pcname=network_pcname, cpu_realname=cpu_realname, pv=pv,
                           username_logon=username_logon, terminal=terminal, drive_storage=drive_storage,
                           os_version=os_version, distro=distro, battery=battery,
                           locip=locip, percent_battery=percent_battery,
                           cpu_usage=cpu_usage, imple_python=imple_python, distro_linux=distro_linux,
                           num_core=num_core, os_name=os_name, ram=ram)


#Logout Route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


#About Route
@app.route('/about')
def about():
    return render_template('about.html', title='About')


#Route for Request Reset Password
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        utils.send_reset_email(user)
        flash('an email has been sent with instructions to reset Your Password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


#Route for Reset Password
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return render_template(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


#Route for connection template for show the Connections and Port in Use
@app.route("/connections")
def connections():
    net_io = psutil.net_io_counters()
    conns = utils.connection_list()
    return render_template('connections.html', conns=conns, net_io=net_io)


#Route for show the Partitions of Disk Drive
@app.route("/partitions")
def partitions():
    disk_part = utils.disk_partition()
    return render_template('partitions.html', disk_part=disk_part)


#Route for show the task Running
@app.route("/task_running")
def task_running():
    psutil.test()
    return render_template('task_running.html')


