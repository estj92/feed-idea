from django.core.management.base import BaseCommand

from feeds.models import BaseCSVFeed, NameMapping


class Command(BaseCommand):
    def handle(self, *args, **options):
        feed, created = BaseCSVFeed.objects.get_or_create(
            name='test-feed.csv',
            include_only_released=True,
            include_only_departments='',
            exclude_departments='Video Games'
        )

        NameMapping.objects.get_or_create(
            order=0, coolshop_name='name', feed_field_name='PName', feed=feed
        )
        NameMapping.objects.get_or_create(
            order=1, coolshop_name='sku', feed_field_name='PID', feed=feed
        )
        NameMapping.objects.get_or_create(
            order=2, coolshop_name='stock', feed_field_name='Stock', feed=feed
        )
        NameMapping.objects.get_or_create(
            order=3, coolshop_name='releasedate', feed_field_name='Release',
            feed=feed
        )

        feed.create_feed()
