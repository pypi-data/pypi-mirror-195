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
from printnanny_api_client.models.order_checkout import OrderCheckout  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestOrderCheckout(unittest.TestCase):
    """OrderCheckout unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OrderCheckout
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.order_checkout.OrderCheckout()  # noqa: E501
        if include_optional :
            return OrderCheckout(
                items = [
                    printnanny_api_client.models.order_item.OrderItem(
                        product = '', 
                        price = '', )
                    ], 
                email = '', 
                stripe_checkout_redirect_url = '', 
                stripe_checkout_session_id = ''
            )
        else :
            return OrderCheckout(
                items = [
                    printnanny_api_client.models.order_item.OrderItem(
                        product = '', 
                        price = '', )
                    ],
                email = '',
                stripe_checkout_redirect_url = '',
                stripe_checkout_session_id = '',
        )

    def testOrderCheckout(self):
        """Test OrderCheckout"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
