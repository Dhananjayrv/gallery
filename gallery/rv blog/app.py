from flask import Flask, render_template, request, redirect, url_for, flash, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename
from PIL import Image
import os
import zipfile

app = Flask(__name__)
app.secret_key = 'kdhananjay444'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'upload_folder'
db = SQLAlchemy(app)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

# Adjust the Post class based on your actual model definition
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
owner_credentials = {'rv': 'rv@82102'}

# Redirect home to gallery
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/course') 
def course():
    return render_template('course.html')

# Redirect signin to dashboard
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'rv' and password == owner_credentials['rv']:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('signin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Handle post editing and deletion as needed
        pass

    # Render dashboard template with media list
    media_list = Media.query.all()
    return render_template('dashboard.html', media_list=media_list)

# Add a new route for the gallery
@app.route('/gallery')
def gallery():
    media_list = Media.query.all()
    return render_template('gallery.html', media_list=media_list)

# Add media upload and deletion routes
@app.route('/upload_media', methods=['POST'])
def upload_media():
    title = request.form['title']
    media_file = request.files['media']

    if media_file:
        # Determine media type based on file extension
        media_type = 'image' if media_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else 'video'

        # Ensure the 'static/media' directory exists
        media_dir = os.path.join('static', 'media')
        os.makedirs(media_dir, exist_ok=True)

        # Save media file
        media_filename = secure_filename(media_file.filename)
        media_file.save(os.path.join(media_dir, media_filename))

        # Create Media object and add to the database
        new_media = Media(title=title, filename=media_filename)
        db.session.add(new_media)
        db.session.commit()

        flash('Media uploaded successfully!')
    else:
        flash('No media file selected.')

    return redirect(url_for('gallery'))

# Add route to handle media deletion
@app.route('/delete_media', methods=['POST'])
def delete_media():
    media_id = request.form['media_id']
    media_to_delete = Media.query.get(media_id)

    if media_to_delete:
        try:
            media_path = os.path.join('static/media', media_to_delete.filename)
            os.remove(media_path)
        except FileNotFoundError:
            pass

        db.session.delete(media_to_delete)
        db.session.commit()
        flash('Media deleted successfully!')
    else:
        flash('Media not found.')

    return redirect(url_for('gallery'))

@app.route('/view/<int:content_id>')
def view_content(content_id):
    content = Media.query.get(content_id)  # Assuming Media is the model for your content
    return render_template('view_content.html', content=content)

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/join_us')
def join_us():
    return render_template('join_us.html')





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
