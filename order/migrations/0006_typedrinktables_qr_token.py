from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='typedrinktables',
            name='qr_token',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
