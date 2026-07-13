from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
import os

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Simple admin credentials from environment (for demo)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('dashboard.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user_id'] = 1
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Username atau password salah.', 'error')
    return render_template('dashboard/login.html')

@dashboard.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('dashboard.login'))

@dashboard.route('/')
@login_required
def index():
    # Placeholder stats
    total_projects = 0
    unread_messages = 0
    visitors_today = 0
    return render_template('dashboard/index.html',
                           total_projects=total_projects,
                           unread_messages=unread_messages,
                           visitors_today=visitors_today)

# Placeholder routes for other dashboard pages
@dashboard.route('/projects')
@login_required
def projects():
    return '<h1>Kelola Proyek</h1><p>Halaman ini akan diimplementasikan selanjutnya.</p><a href=\"' + url_for('dashboard.index') + '\">Kembali</a>'

@dashboard.route('/profile')
@login_required
def profile():
    return '<h1>Edit Profil</h1><p>Halaman ini akan diimplementasikan selanjutnya.</p><a href=\"' + url_for('dashboard.index') + '\">Kembali</a>'

@dashboard.route('/messages')
@login_required
def messages():
    return '<h1>Kotak Masuk</h1><p>Halaman ini akan diimplementasikan selanjutnya.</p><a href=\"' + url_for('dashboard.index') + '\">Kembali</a>'