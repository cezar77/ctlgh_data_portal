from django.template import Template, Context
from django.test import TestCase


class LonlatTagsTest(TestCase):
    lon_template = Template('{% load lonlat %}{{ gps|longitude }}')
    lat_template = Template('{% load lonlat %}{{ gps|latitude }}')

    def test_longitude_east(self):
        """
        Longitude of Johannesburg
        """
        gps = 28.04556
        t = self.lon_template.render(Context({'gps': gps}))
        self.assertIn(u'\u00b0', t)
        self.assertEqual('28\u00b002&#39;44&quot;E', t)

    def test_longitude_west(self):
        """
        Longitude of Edinburgh
        """
        gps = -3.188889
        t = self.lon_template.render(Context({'gps': gps}))
        self.assertEqual('3\u00b011&#39;20&quot;W', t)

    def test_latitude_north(self):
        """
        Latitude of Edinburgh
        """
        gps = 55.95306
        t = self.lat_template.render(Context({'gps': gps}))
        self.assertEqual('55\u00b057&#39;11&quot;N', t)

    def test_latitude_south(self):
        """
        Latitude of Johannesburg
        """
        gps = -26.20444
        t = self.lat_template.render(Context({'gps': gps}))
        self.assertEqual('26\u00b012&#39;16&quot;S', t)

    def test_zero_longitude(self):
        """
        Zero longitude
        """
        gps = 0
        t = self.lon_template.render(Context({'gps': gps}))
        self.assertEqual('0\u00b000&#39;00&quot;', t)

    def test_zero_latitude(self):
        """
        Zero latitude
        """
        gps = 0
        t = self.lat_template.render(Context({'gps': gps}))
        self.assertEqual('0\u00b000&#39;00&quot;', t)

    def test_invalid_longitude(self):
        """
        Invalid longitude
        """
        gps = -200.25
        t = self.lon_template.render(Context({'gps': gps}))
        self.assertEqual('-200.25', t)

    def test_invalid_latitude(self):
        """
        Invalid latitude
        """
        gps = 100.83333
        t = self.lat_template.render(Context({'gps': gps}))
        self.assertEqual('100.83333', t)
