from sample_server import DB


class Instructions(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    integration_name = DB.Column(DB.String(100), nullable=False)
    int_uuid = DB.Column(DB.String(40), nullable=False)
    tenant_id = DB.Column(DB.String(40), nullable=False)
    command = DB.Column(DB.Text, nullable=False)
    active = DB.Column(DB.Boolean, nullable=False)
    schedule = DB.Column(DB.String(255))
    run_next = DB.Column(DB.Boolean, nullable=False)
    db_info = DB.Column(DB.Text)
