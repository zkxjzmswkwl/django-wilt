from django.db import models
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class Update(models.Model):
    title = models.CharField(max_length=64, default="Title")
    timestamp = models.DateTimeField(auto_now_add=True)
    markdown = MarkdownField(rendered_field="markdown_rendered", validator=VALIDATOR_STANDARD)
    markdown_rendered = RenderedMarkdownField()

    # Apparently you have to migrate before accessing model.id?

