from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from models import db, Message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form data
        name = request.form.get('nama')
        email = request.form.get('email')
        message_body = request.form.get('pesan')
        # Save to database
        new_message = Message(name=name, email=email, message=message_body)
        db.session.add(new_message)
        db.session.commit()
        flash('Terima kasih! Pesan Anda telah dikirim.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')