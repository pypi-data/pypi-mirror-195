# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.127.4
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.octo_print_settings import OctoPrintSettings  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestOctoPrintSettings(unittest.TestCase):
    """OctoPrintSettings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OctoPrintSettings
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.octo_print_settings.OctoPrintSettings()  # noqa: E501
        if include_optional :
            return OctoPrintSettings(
                id = 56, 
                octoprint_enabled = True, 
                events_enabled = True, 
                sync_gcode = True, 
                sync_printer_profiles = True, 
                sync_backups = True, 
                auto_backup = '', 
                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                octoprint_server = 56
            )
        else :
            return OctoPrintSettings(
                id = 56,
                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                octoprint_server = 56,
        )

    def testOctoPrintSettings(self):
        """Test OctoPrintSettings"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
