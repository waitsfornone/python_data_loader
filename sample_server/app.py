# This will be the app for serving the instructions and receiving the files
from flask import (render_template, url_for, redirect)
from sample_server import create_app, DB
from sample_server.models import Instructions
from forms import InstructionForm


app = create_app()


@app.cli.command()
def initdb():
    DB.create_all()


@app.cli.command()
def redodb():
    DB.drop_all()
    DB.create_all()
    tester = Instructions(
        int_uuid = 'cb10d0df-7407-470d-a72e-6588b29c93cc',
        tenant_id = '39468c53-157d-4952-999e-1ec37f1d6026',
        integration_name = 'My Test Integration Instructions',
        active = True,
        run_next = False,
        db_info = 'some db info',
        command = 'This is my query'
    )
    DB.session.add(tester)
    DB.session.commit()


@app.route('/')
def index():
    integrations = Instructions.query.order_by(Instructions.tenant_id, Instructions.integration_name).all()
    return render_template('index.html', data=integrations)


@app.route('/new', methods=['GET', 'POST'])
def add_instructions():
    form = InstructionForm()
    if form.validate_on_submit():
        # create a record
        job = Instructions(
            integration_name=form.integration_name.data,
            int_uuid=form.int_uuid.data,
            tenant_id=form.tenant_id.data,
            active=form.active.data,
            run_next=form.run_next.data,
            db_info=form.db_info.data,
            command=form.command.data
        )
        DB.session.add(job)
        DB.session.commit()
        return redirect(url_for('index'))
    return render_template('add_instructions.html', form=form)


@app.route('/integration/<int:id>', methods=['GET', 'POST'])
def edit_instruction(id):
    instruction = Instructions.query.get(id)
    form = InstructionForm(obj=instruction)
    if form.validate_on_submit():
        instruction.integration_name = form.integration_name.data
        instruction.int_uuid = form.int_uuid.data
        instruction.db_info = form.db_info.data
        instruction.tenant_id = form.tenant_id.data
        instruction.active = form.active.data
        instruction.run_next = form.run_next.data
        instruction.command = form.command.data
        DB.session.add(instruction)
        DB.session.commit()
        return redirect(url_for('index'))
    return render_template('add_instructions.html', form=form)


@app.route('/files')
def uploaded_files():
    pass


if __name__ == "__main__":
    app.run()
