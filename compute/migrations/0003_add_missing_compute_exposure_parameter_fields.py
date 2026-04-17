# Generated manually to sync the legacy SQLite schema with the current model.

from django.db import migrations


def add_missing_fields(apps, schema_editor):
    ComputeExposureParameters = apps.get_model('compute', 'ComputeExposureParameters')
    table_name = ComputeExposureParameters._meta.db_table
    model_fields = [
        'frequency_position',
        'operator_name',
        'call_sign',
        'email',
        'include_calculations',
        'mode_factor',
    ]

    with schema_editor.connection.cursor() as cursor:
        existing_columns = {column.name for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)}

    for field_name in model_fields:
        if field_name in existing_columns:
            continue

        field = ComputeExposureParameters._meta.get_field(field_name)
        schema_editor.add_field(ComputeExposureParameters, field)


class Migration(migrations.Migration):

    dependencies = [
        ('compute', '0002_alter_rfreport_options'),
    ]

    operations = [
        migrations.RunPython(add_missing_fields, migrations.RunPython.noop),
    ]
