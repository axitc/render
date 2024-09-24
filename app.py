# Parameters
THRESHOLD = 0.85
IMG_WIDTH, IMG_HEIGHT = 224, 224


#from tensorflow.keras.models import load_model
#cnn = load_model('cnn.keras')



from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'arbitrarilylongsecretkey'


class TrashForm(FlaskForm):
    image = FileField(u'Image File', validators=[DataRequired()])
    location = StringField(u'Trash Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

#import os
# pip install opencv-python
import cv2
import numpy as np
@app.route('/', methods=['GET', 'POST'])
def index():
    image = None
    location = None
    form = TrashForm()
    if form.validate_on_submit():
        image = form.image.data
        location = form.location.data

        #imagefilename = str(cur.lastrowid) + '.jpg'
        #image.save(os.path.join('images', imagefilename))

        #image = cv2.imread(os.path.join('images',imagefilename))
        #image = cv2.imread(image)
        image = np.asarray(bytearray(image.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
        image = image.astype('float32')
        image /= 225
        image = np.expand_dims(image, axis=0)

        prediction = 0.9
        label = 1 if prediction > THRESHOLD else 0

        if prediction > THRESHOLD:
            return redirect(url_for('positive'))
        else:
            return redirect(url_for('negative'))
    return render_template('index.html', form=form, image=image, location=location)

@app.route('/positive')
def positive():
    return render_template('positive.html')

class ReportForm(FlaskForm):
    submit = SubmitField('Report')

@app.route('/negative', methods=['GET', 'POST'])
def negative():
    form = ReportForm()
    if form.validate_on_submit():
        return redirect(url_for('report'))
    return render_template('negative.html', form=form)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def err500(e):
    return render_template('500.html'), 500
