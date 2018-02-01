# encoding: utf-8
from django.db import models
from google.cloud import bigquery
import os
import json
import csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = "django-jquery-file-upload/media"

class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.FileField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)
        print("Uploading data to BIG Query")
        self.upload_to_big_query(os.path.join( BASE_DIR, MEDIA_ROOT, self.file.name))

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)

    def parse_file(self, file_path):
        data_rows = []
        with open(file_path, 'rb') as csvfile:
            r = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in r:
                if len(row) == 7 and "Electric usage" in row[0]:
                    row_item = {}
                    row_item["zip"] = zipcode
                    row_item["type"] = row[0]
                    row_item["date"] = row[1]
                    row_item["start"] = row[2]
                    row_item["end"] = row[3]
                    row_item["usage"] = row[4]
                    row_item["units"] = row[5]
                    data_rows.append(json.loads(json.dumps(row_item)))
                elif "Address" in row:
                    zipcode = self.get_zipcode(row)
            return data_rows

    def get_zipcode(self, address):
        return address[-1].split()[1].strip('\"')

    def upload_to_big_query(self, file_path):
        # DO CSV Stuff for content
        rows = self.parse_file(file_path)
        bigquery_client = bigquery.Client()
        dataset_ref = bigquery_client.dataset("gbd_store")
        table_ref = dataset_ref.table("pge_electric")
        table = bigquery_client.get_table(table_ref)
        errors = bigquery_client.create_rows(table, rows)
        if not errors:
            print("Successfully uploaded data to big query")
        else:
            print("ERRORS:")
            print(errors)
