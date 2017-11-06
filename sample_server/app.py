# This will be the app for serving the instructions and receiving the files
from flask import (render_template,
                   url_for,
                   redirect,
                   jsonify,
                   make_response,
                   request,
                   send_from_directory)
from sample_server import create_app, DB
from sample_server.models import Instructions
from forms import InstructionForm
from flask_uploads import UploadSet, configure_uploads
import os
import sqlalchemy

app = create_app()

file_set = UploadSet('approvedfiletypes', extensions='csv')
app.config['UPLOADED_APPROVEDFILETYPES_DEST'] = 'data/client_files'
configure_uploads(app, file_set)


@app.cli.command()
def initdb():
    DB.create_all()


@app.cli.command()
def redodb():
    DB.drop_all()
    DB.create_all()
    tester = Instructions(
        int_uuid='cb10d0df-7407-470d-a72e-6588b29c93cc',
        tenant_id='39468c53-157d-4952-999e-1ec37f1d6026',
        integration_name='My Test Integration Instructions',
        active=True,
        run_next=False,
        db_info='some db info',
        command='This is my query'
    )
    DB.session.add(tester)
    DB.session.commit()


@app.route('/home')
def index():
    integrations = Instructions.query.order_by(Instructions.tenant_id, Instructions.integration_name).all()
    return render_template('index.html', data=integrations)


@app.route('/integration/new', methods=['GET', 'POST'])
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


@app.route('/api/upload_files', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if file_set.save(request.files['file_set']):
            return make_response(jsonify({'success': 'OK'}), 200)
        else:
            return make_response(jsonify({'error': 'file save failed'}), 200)
    elif request.method == 'GET' and 'file_set' in request.files:
        return make_response(jsonify({'error': 'wrong method to send file'}), 405)
    else:
        return make_response(jsonify({'error': 'no file provided'}), 400)


@app.route('/files', methods=['GET'])
def list_files():
    filepath = os.path.join(app.root_path, '../' + app.config['UPLOADED_APPROVEDFILETYPES_DEST'])
    data = sorted(os.listdir(filepath))
    return render_template('files.html', files=data)


@app.route('/files/<path:path>', methods=['GET'])
def serve_file(path):
    filename = path.split(os.sep)[-1]
    return send_from_directory(
        os.path.join(app.root_path, '../' + app.config['UPLOADED_APPROVEDFILETYPES_DEST']),
        filename,
        as_attachment=True
    )


# print(query.compile(compile_kwargs={"literal_binds": True}))
@app.route('/api/<tenant_id>/<int_uuid>', methods=['GET'])
def send_instructions(tenant_id, int_uuid):
    info = DB.session.query(Instructions).filter(Instructions.int_uuid == int_uuid,
                                                 Instructions.tenant_id == tenant_id,
                                                 Instructions.active,
                                                 Instructions.run_next).all()
    # need to create a dictionary of the data we need to send down.
    data = {}
    for each in info[0].__dict__.keys():
        if isinstance(info[0].__dict__[each], sqlalchemy.orm.state.InstanceState):
            app.logger.info('not serializable!!')
        else:
            data[each] = info[0].__dict__[each]
    return make_response(jsonify({'success': 'OK', 'data': data}), 200)


if __name__ == "__main__":
    app.run()
