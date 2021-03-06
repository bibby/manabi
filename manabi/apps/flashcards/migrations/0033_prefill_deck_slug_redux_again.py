# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-12-03 21:27
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    from autoslug.settings import slugify

    Deck = apps.get_model('flashcards', 'Deck')

    for deck in Deck.objects.all().iterator():
        deck.slug = slugify(deck.name)
        deck.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0032_add_deck_slug_as_non_unique_and_optional'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
