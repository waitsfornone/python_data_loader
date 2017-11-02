# This will be the app for serving the instructions and receiving the files
# need a database (sqllite will do)
from flask import (render_template)
from sample_server import create_app, DB
from sample_server.models import Instructions
from forms import InstructionForm


app = create_app()


@app.cli.command()
def initdb():
    DB.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def add_instructions():
    form = InstructionForm()
    return render_template('add_instructions.html', form=form)


if __name__ == "__main__":
    app.run()
