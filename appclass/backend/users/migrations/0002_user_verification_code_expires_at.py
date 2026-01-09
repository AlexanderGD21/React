# Generated manually for the verification-code expiration field.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
