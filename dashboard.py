from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from functools import wraps
import os
from werkzeug.utils import secure_filename
from models import db, Project, Message, Profile, Skill

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
    # Stats
    total_projects = Project.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()
    viewers_today = 0  # placeholder; could be implemented with analytics
    # Recent data for dashboard overview
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    profile = Profile.query.first()
    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    return render_template('dashboard/index.html',
                           total_projects=total_projects,
                           unread_messages=unread_messages,
                           visitors_today=viewers_today,
                           recent_projects=recent_projects,
                           profile=profile,
                           recent_messages=recent_messages)

# Helper for file upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------- PROJECT CRUD -----------------
@dashboard.route('/projects')
@login_required
def projects():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    pagination = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    projects = pagination.items
    return render_template('dashboard/projects.html', projects=projects, pagination=pagination)

@dashboard.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        github_link = request.form.get('github_link')
        live_link = request.form.get('live_link')
        # handle file upload
        image_file = 'default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # ensure upload folder exists
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                image_file = filename
        # create project
        new_project = Project(
            title=title,
            description=description,
            technologies=technologies,
            github_link=github_link,
            live_link=live_link,
            image_file=image_file
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Proyek berhasil ditambahkan!', 'success')
        return redirect(url_for('dashboard.projects'))
    return render_template('dashboard/add_project.html')

@dashboard.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technologies = request.form.get('technologies')
        project.github_link = request.form.get('github_link')
        project.live_link = request.form.get('live_link')
        # handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # delete old image if not default
                if project.image_file != 'default.jpg':
                    old_path = os.path.join(current_app.root_path, 'static', 'uploads', project.image_file)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                project.image_file = filename
        db.session.commit()
        flash('Proyek berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard.projects'))
    return render_template('dashboard/edit_project.html', project=project)

@dashboard.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    # delete image file if not default
    if project.image_file != 'default.jpg':
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', project.image_file)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(project)
    db.session.commit()
    flash('Proyek berhasil dihapus!', 'success')
    return redirect(url_for('dashboard.projects'))

# ----------------- PROFILE -----------------
@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Assume single profile (id=1) else create
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name='', headline='', about='', photo_file='default.jpg')
        db.session.add(profile)
        db.session.commit()
    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.headline = request.form.get('headline')
        profile.about = request.form.get('about')
        # handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                # delete old photo if not default
                if profile.photo_file != 'default.jpg':
                    old_path = os.path.join(current_app.root_path, 'static', 'uploads', profile.photo_file)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                profile.photo_file = filename
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard.profile'))
    # get skills for display
    skills = Skill.query.filter_by(profile_id=profile.id).all()
    return render_template('dashboard/profile.html', profile=profile, skills=skills)

# optional: manage skills (add/delete) - we can keep simple for now
@dashboard.route('/profile/skill/add', methods=['POST'])
@login_required
def add_skill():
    profile = Profile.query.first()
    if not profile:
        flash('Buat profil terlebih dahulu.', 'warning')
        return redirect(url_for('dashboard.profile'))
    name = request.form.get('skill_name')
    if name:
        # avoid duplicate
        exists = Skill.query.filter_by(profile_id=profile.id, name=name).first()
        if not exists:
            skill = Skill(name=name, profile_id=profile.id)
            db.session.add(skill)
            db.session.commit()
            flash('Keterampilan ditambahkan!', 'success')
        else:
            flash('Keterampilan sudah ada.', 'warning')
    return redirect(url_for('dashboard.profile'))

@dashboard.route('/profile/skill/<int:id>/delete', methods=['POST'])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Keterampilan dihapus!', 'success')
    return redirect(url_for('dashboard.profile'))

# ----------------- MESSAGES -----------------
@dashboard.route('/messages')
@login_required
def messages():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Message.query.order_by(Message.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    messages = pagination.items
    return render_template('dashboard/messages.html', messages=messages, pagination=pagination)

@dashboard.route('/messages/<int:id>/read', methods=['POST'])
@login_required
def mark_read(id):
    msg = Message.query.get_or_404(id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
        flash('Pesan ditandai sebagai dibaca.', 'info')
    return redirect(url_for('dashboard.messages'))

@dashboard.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Pesan dihapus.', 'info')
    return redirect(url_for('dashboard.messages'))