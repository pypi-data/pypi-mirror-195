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
from printnanny_api_client.models.video_recording_request import VideoRecordingRequest  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestVideoRecordingRequest(unittest.TestCase):
    """VideoRecordingRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test VideoRecordingRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.video_recording_request.VideoRecordingRequest()  # noqa: E501
        if include_optional :
            return VideoRecordingRequest(
                id = '', 
                cloud_sync_done = True, 
                combine_done = True, 
                recording_start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                recording_end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                gcode_file_name = '0'
            )
        else :
            return VideoRecordingRequest(
        )

    def testVideoRecordingRequest(self):
        """Test VideoRecordingRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
