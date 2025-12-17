# Generated migration for add-unique-cont-id change

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlitem',
            name='cont_id',
            field=models.CharField(
                help_text='ThePaper content ID',
                max_length=50,
                unique=True,
            ),
        ),
    ]

