from flask import Flask, render_template, Response, request, flash
import os
from werkzeug.utils import secure_filename
from pres import presentation, pres_split # functions to split and control presentation
from mouse import mouse # function to control mouse
from whiteboard import whiteboard # function to display and control whiteboard

UPLOAD_FOLDER = 'static/assets/pres/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HOME PAGE ROUTE
@app.route('/')
def index():
    return render_template("index.html")

# UPLOAD PAGE ROUTE
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
        return render_template('upload.html')

    # UPLOADING PRESENTATION
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    print("uploader")
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], "pres.pdf"))
        pres_split()
        return render_template('presentation.html')
    else:
        return render_template('upload.html')

# PRESENTATION PAGE ROUTE
@app.route('/presentation_page')
def presentation_page():
    return render_template("presentation.html")

    # DISPLAYING PRESENTATION VIDEO ON THE PAGE
@app.route('/presentation_display')
def presentation_display():
    return Response(presentation(), mimetype='multipart/x-mixed-replace; boundary=frame')

# MOUSE CONTROLLER PAGE ROUTE
@app.route('/mouse_page')
def mouse_page():
    return render_template("mouse.html")

    # DISPLAYING MOUSE VIDEO ON THE PAGE
@app.route('/mouse_display')
def mouse_display():
    return Response(mouse(), mimetype='multipart/x-mixed-replace; boundary=frame')

# WHITEBOARD PAGE ROUTE
@app.route('/whiteboard_page')
def whiteboard_page():
    return render_template("whiteboard.html")

    # DISPLAYING WHITEBOARD VIDEO ON THE PAGE
@app.route('/whiteboard_display')
def whiteboard_display():
    return Response(whiteboard(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=8000)