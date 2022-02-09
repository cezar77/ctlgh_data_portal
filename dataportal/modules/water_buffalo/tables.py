from urllib.parse import urlparse

from django.utils.html import format_html, mark_safe

import django_tables2 as tables
from django_tables2 import A

from .models import Animal


class AnimalTable(tables.Table):
    study_accession = tables.Column(orderable=False)
    sample_accession = tables.Column(orderable=False)
    experiment_accession = tables.Column(orderable=False)
    run_accession = tables.Column(orderable=False)
    breed = tables.Column()
    tax_id = tables.Column(orderable=False)
    fastq_ftp = tables.Column(orderable=False)
    submitted_ftp = tables.Column(orderable=False)
    sra_ftp = tables.Column(orderable=False)

    export_formats = ['tsv']

    class Meta:
        model = Animal
        fields = (
            'study_accession', 'sample_accession', 'experiment_accession',
            'run_accession', 'breed', 'tax_id', 'fastq_ftp', 'submitted_ftp',
            'sra_ftp'
        )
        attrs = {
            'class': 'table table-responsive table-hover'
        }

    def render_study_accession(self, record, value):
        return format_html(
            '<a href="{url}">{value}</a>',
            url=record.get_study_accession_url(),
            value=value
        )

    def render_sample_accession(self, record, value):
        return format_html(
            '<a href="{url}">{value}</a>',
            url=record.get_sample_accession_url(),
            value=value
        )

    def render_experiment_accession(self, record, value):
        return format_html(
            '<a href="{url}">{value}</a>',
            url=record.get_experiment_accession_url(),
            value=value
        )

    def render_run_accession(self, record, value):
        return format_html(
            '<a href="{url}">{value}</a>',
            url=record.get_run_accession_url(),
            value=value
        )

    def render_tax_id(self, record, value):
        return format_html(
            '<a href="{url}">{value}</a>',
            url=record.get_tax_id_url(),
            value=value
        )

    def render_fastq_ftp(self, record, value):
        links = list(map(self.create_download_link, value))
        return mark_safe(''.join(links))

    def render_submitted_ftp(self, record, value):
        links = list(map(self.create_download_link, value))
        return mark_safe(''.join(links))

    def render_sra_ftp(self, record, value):
        return self.create_download_link(value)

    def create_download_link(self, url):
        p = urlparse(url)
        filename = p.path.rpartition('/')[-1]
        button = '<a href="{url}" class="btn btn-primary" role="button" style="display:block">{filename}</a>'
        return format_html(
            button,
            url=url,
            filename=filename
        )
