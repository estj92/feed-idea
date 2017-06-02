import csv

from datetime import date

from django.db import models


def get_products():
    products = [
        {
            'id': 'A37842',
            'name': 'RAMBO THE VIDEO GAME',
            'price': 4900,
            'discount': 84,
            'stock': 100,
            'sku': 76195,
            'releasedate': date(2009, 5, 1),
            'department': 'Video Games'
        },
        {
            'id': 'AB3F8E',
            'name': 'LEGO Architecture - Buckingham Palace (21029)',
            'price': 35900,
            'discount': 28,
            'stock': 0,
            'sku': 1007923,
            'releasedate': date(2015, 1, 7),
            'department': 'Toys'
        },
        {
            'id': 'AG2NM8',
            'name': ('Squier Affinity HSS Stratocaster - Elektrisk Guitar '
                     'Start Pakke 2 (Brown Sunburst)'),
            'price': 199900,
            'discount': 13,
            'stock': 5,
            'sku': 198953,
            'releasedate': date(2020, 1, 1),
            'department': 'Music'
        },
        {
            'id': 'A479VP',
            'name': 'Uno',
            'price': 9900,
            'discount': 0,
            'stock': 10,
            'sku': 63581,
            'releasedate': date(2012, 11, 10),
            'department': 'Toys'
        },
    ]

    for product in products:
        yield product


class BaseFeed(models.Model):
    name = models.CharField(max_length=255)
    include_only_released = models.BooleanField(default=True)
    include_only_departments = models.TextField()  # Should be array
    exclude_departments = models.TextField()  # Should be Array

    def do_include(self, product):
        if (self.include_only_released and
                product['releasedate'] > date.today()):
            return False

        if (self.include_only_departments and
                product['department'] not in self.include_only_departments):
            return False

        if product['department'] in self.exclude_departments:
            return False

    def create_feed(self):
        raise NotImplementedError()

    def get_named_fields(self, product):
        row = [(m.feed_field_name, product[m.coolshop_name])
               for m in self.name_mapping.all()]
        return row


class NameMapping(models.Model):
    order = models.IntegerField()
    coolshop_name = models.CharField(max_length=255)
    feed_field_name = models.CharField(max_length=255)
    feed = models.ForeignKey(BaseFeed, related_name='name_mapping')

    class Meta:
        ordering = ['feed', 'order']
        unique_together = (
            ('order', 'feed'),
            ('order', 'coolshop_name', 'feed_field_name', 'feed')
        )


class BaseCSVFeed(BaseFeed):
    def get_named_fields(self, product):
        row = super().get_named_fields(product)
        row = [i[1] for i in row]
        return row

    def create_feed(self):
        header = [v.feed_field_name for v in self.name_mapping.all()]
        with open(self.name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                lineterminator='\n')  # Silly Windows
            writer.writerow(header)

            for product in get_products():
                fields = self.get_named_fields(product)
                writer.writerow(fields)
