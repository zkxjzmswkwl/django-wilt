# Generated by Django 5.0.3 on 2024-04-03 08:23

import markdownfield.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Update",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="Title", max_length=64)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "markdown",
                    markdownfield.models.MarkdownField(
                        rendered_field="markdown_rendered"
                    ),
                ),
                ("markdown_rendered", markdownfield.models.RenderedMarkdownField()),
            ],
        ),
    ]
