from sample_server.models import Instructions


def validate_int_uuid(int_uuid):
    integrations = Instructions.query.filter(Instructions.int_uuid == int_uuid).count()
    if integrations == 0:
        return False
    else:
        return True


def validate_tenant_id(tenant_id):
    tenants = Instructions.query.filter(Instructions.tenant_id == tenant_id).count()
    if tenants == 0:
        return False
    else:
        return True
