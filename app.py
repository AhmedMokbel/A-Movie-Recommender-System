import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
import MovieRecommenderSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))

bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = TextAreaField('Enter the name of movie', validators=[DataRequired()])
    submit = SubmitField('recommend')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        recommender = MovieRecommenderSystem.recommender(form.name.data)
        
        flash('Recommended Movies = ' + str(recommender) )
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
