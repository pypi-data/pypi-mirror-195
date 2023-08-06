# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.127.4
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class Product(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'djstripe_product': 'DjStripeProduct',
        'prices': 'list[DjStripePrice]',
        'deleted': 'datetime',
        'created_dt': 'datetime',
        'updated_dt': 'datetime',
        'sku': 'str',
        'slug': 'str',
        'unit_label': 'str',
        'name': 'str',
        'description': 'str',
        'statement_descriptor': 'str',
        'images': 'list[str]',
        'is_active': 'bool',
        'is_shippable': 'bool',
        'is_preorder': 'bool',
        'is_subscription': 'bool',
        'stripe_price_lookup_key': 'str',
        'stripe_product_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'djstripe_product': 'djstripe_product',
        'prices': 'prices',
        'deleted': 'deleted',
        'created_dt': 'created_dt',
        'updated_dt': 'updated_dt',
        'sku': 'sku',
        'slug': 'slug',
        'unit_label': 'unit_label',
        'name': 'name',
        'description': 'description',
        'statement_descriptor': 'statement_descriptor',
        'images': 'images',
        'is_active': 'is_active',
        'is_shippable': 'is_shippable',
        'is_preorder': 'is_preorder',
        'is_subscription': 'is_subscription',
        'stripe_price_lookup_key': 'stripe_price_lookup_key',
        'stripe_product_id': 'stripe_product_id'
    }

    def __init__(self, id=None, djstripe_product=None, prices=None, deleted=None, created_dt=None, updated_dt=None, sku=None, slug=None, unit_label=None, name=None, description=None, statement_descriptor=None, images=None, is_active=None, is_shippable=None, is_preorder=None, is_subscription=None, stripe_price_lookup_key=None, stripe_product_id=None, local_vars_configuration=None):  # noqa: E501
        """Product - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._djstripe_product = None
        self._prices = None
        self._deleted = None
        self._created_dt = None
        self._updated_dt = None
        self._sku = None
        self._slug = None
        self._unit_label = None
        self._name = None
        self._description = None
        self._statement_descriptor = None
        self._images = None
        self._is_active = None
        self._is_shippable = None
        self._is_preorder = None
        self._is_subscription = None
        self._stripe_price_lookup_key = None
        self._stripe_product_id = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.djstripe_product = djstripe_product
        self.prices = prices
        self.deleted = deleted
        self.created_dt = created_dt
        self.updated_dt = updated_dt
        self.sku = sku
        self.slug = slug
        self.unit_label = unit_label
        self.name = name
        self.description = description
        self.statement_descriptor = statement_descriptor
        if images is not None:
            self.images = images
        if is_active is not None:
            self.is_active = is_active
        self.is_shippable = is_shippable
        self.is_preorder = is_preorder
        self.is_subscription = is_subscription
        self.stripe_price_lookup_key = stripe_price_lookup_key
        self.stripe_product_id = stripe_product_id

    @property
    def id(self):
        """Gets the id of this Product.  # noqa: E501


        :return: The id of this Product.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Product.


        :param id: The id of this Product.  # noqa: E501
        :type id: str
        """

        self._id = id

    @property
    def djstripe_product(self):
        """Gets the djstripe_product of this Product.  # noqa: E501


        :return: The djstripe_product of this Product.  # noqa: E501
        :rtype: DjStripeProduct
        """
        return self._djstripe_product

    @djstripe_product.setter
    def djstripe_product(self, djstripe_product):
        """Sets the djstripe_product of this Product.


        :param djstripe_product: The djstripe_product of this Product.  # noqa: E501
        :type djstripe_product: DjStripeProduct
        """
        if self.local_vars_configuration.client_side_validation and djstripe_product is None:  # noqa: E501
            raise ValueError("Invalid value for `djstripe_product`, must not be `None`")  # noqa: E501

        self._djstripe_product = djstripe_product

    @property
    def prices(self):
        """Gets the prices of this Product.  # noqa: E501


        :return: The prices of this Product.  # noqa: E501
        :rtype: list[DjStripePrice]
        """
        return self._prices

    @prices.setter
    def prices(self, prices):
        """Sets the prices of this Product.


        :param prices: The prices of this Product.  # noqa: E501
        :type prices: list[DjStripePrice]
        """
        if self.local_vars_configuration.client_side_validation and prices is None:  # noqa: E501
            raise ValueError("Invalid value for `prices`, must not be `None`")  # noqa: E501

        self._prices = prices

    @property
    def deleted(self):
        """Gets the deleted of this Product.  # noqa: E501


        :return: The deleted of this Product.  # noqa: E501
        :rtype: datetime
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this Product.


        :param deleted: The deleted of this Product.  # noqa: E501
        :type deleted: datetime
        """
        if self.local_vars_configuration.client_side_validation and deleted is None:  # noqa: E501
            raise ValueError("Invalid value for `deleted`, must not be `None`")  # noqa: E501

        self._deleted = deleted

    @property
    def created_dt(self):
        """Gets the created_dt of this Product.  # noqa: E501


        :return: The created_dt of this Product.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this Product.


        :param created_dt: The created_dt of this Product.  # noqa: E501
        :type created_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `created_dt`, must not be `None`")  # noqa: E501

        self._created_dt = created_dt

    @property
    def updated_dt(self):
        """Gets the updated_dt of this Product.  # noqa: E501


        :return: The updated_dt of this Product.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this Product.


        :param updated_dt: The updated_dt of this Product.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

        self._updated_dt = updated_dt

    @property
    def sku(self):
        """Gets the sku of this Product.  # noqa: E501


        :return: The sku of this Product.  # noqa: E501
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """Sets the sku of this Product.


        :param sku: The sku of this Product.  # noqa: E501
        :type sku: str
        """
        if self.local_vars_configuration.client_side_validation and sku is None:  # noqa: E501
            raise ValueError("Invalid value for `sku`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sku is not None and len(sku) > 255):
            raise ValueError("Invalid value for `sku`, length must be less than or equal to `255`")  # noqa: E501

        self._sku = sku

    @property
    def slug(self):
        """Gets the slug of this Product.  # noqa: E501


        :return: The slug of this Product.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """Sets the slug of this Product.


        :param slug: The slug of this Product.  # noqa: E501
        :type slug: str
        """
        if self.local_vars_configuration.client_side_validation and slug is None:  # noqa: E501
            raise ValueError("Invalid value for `slug`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and len(slug) > 64):
            raise ValueError("Invalid value for `slug`, length must be less than or equal to `64`")  # noqa: E501

        self._slug = slug

    @property
    def unit_label(self):
        """Gets the unit_label of this Product.  # noqa: E501


        :return: The unit_label of this Product.  # noqa: E501
        :rtype: str
        """
        return self._unit_label

    @unit_label.setter
    def unit_label(self, unit_label):
        """Sets the unit_label of this Product.


        :param unit_label: The unit_label of this Product.  # noqa: E501
        :type unit_label: str
        """
        if self.local_vars_configuration.client_side_validation and unit_label is None:  # noqa: E501
            raise ValueError("Invalid value for `unit_label`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                unit_label is not None and len(unit_label) > 255):
            raise ValueError("Invalid value for `unit_label`, length must be less than or equal to `255`")  # noqa: E501

        self._unit_label = unit_label

    @property
    def name(self):
        """Gets the name of this Product.  # noqa: E501


        :return: The name of this Product.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Product.


        :param name: The name of this Product.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 255):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Product.  # noqa: E501


        :return: The description of this Product.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Product.


        :param description: The description of this Product.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 255):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `255`")  # noqa: E501

        self._description = description

    @property
    def statement_descriptor(self):
        """Gets the statement_descriptor of this Product.  # noqa: E501


        :return: The statement_descriptor of this Product.  # noqa: E501
        :rtype: str
        """
        return self._statement_descriptor

    @statement_descriptor.setter
    def statement_descriptor(self, statement_descriptor):
        """Sets the statement_descriptor of this Product.


        :param statement_descriptor: The statement_descriptor of this Product.  # noqa: E501
        :type statement_descriptor: str
        """
        if self.local_vars_configuration.client_side_validation and statement_descriptor is None:  # noqa: E501
            raise ValueError("Invalid value for `statement_descriptor`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                statement_descriptor is not None and len(statement_descriptor) > 255):
            raise ValueError("Invalid value for `statement_descriptor`, length must be less than or equal to `255`")  # noqa: E501

        self._statement_descriptor = statement_descriptor

    @property
    def images(self):
        """Gets the images of this Product.  # noqa: E501


        :return: The images of this Product.  # noqa: E501
        :rtype: list[str]
        """
        return self._images

    @images.setter
    def images(self, images):
        """Sets the images of this Product.


        :param images: The images of this Product.  # noqa: E501
        :type images: list[str]
        """

        self._images = images

    @property
    def is_active(self):
        """Gets the is_active of this Product.  # noqa: E501


        :return: The is_active of this Product.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this Product.


        :param is_active: The is_active of this Product.  # noqa: E501
        :type is_active: bool
        """

        self._is_active = is_active

    @property
    def is_shippable(self):
        """Gets the is_shippable of this Product.  # noqa: E501


        :return: The is_shippable of this Product.  # noqa: E501
        :rtype: bool
        """
        return self._is_shippable

    @is_shippable.setter
    def is_shippable(self, is_shippable):
        """Sets the is_shippable of this Product.


        :param is_shippable: The is_shippable of this Product.  # noqa: E501
        :type is_shippable: bool
        """
        if self.local_vars_configuration.client_side_validation and is_shippable is None:  # noqa: E501
            raise ValueError("Invalid value for `is_shippable`, must not be `None`")  # noqa: E501

        self._is_shippable = is_shippable

    @property
    def is_preorder(self):
        """Gets the is_preorder of this Product.  # noqa: E501


        :return: The is_preorder of this Product.  # noqa: E501
        :rtype: bool
        """
        return self._is_preorder

    @is_preorder.setter
    def is_preorder(self, is_preorder):
        """Sets the is_preorder of this Product.


        :param is_preorder: The is_preorder of this Product.  # noqa: E501
        :type is_preorder: bool
        """
        if self.local_vars_configuration.client_side_validation and is_preorder is None:  # noqa: E501
            raise ValueError("Invalid value for `is_preorder`, must not be `None`")  # noqa: E501

        self._is_preorder = is_preorder

    @property
    def is_subscription(self):
        """Gets the is_subscription of this Product.  # noqa: E501


        :return: The is_subscription of this Product.  # noqa: E501
        :rtype: bool
        """
        return self._is_subscription

    @is_subscription.setter
    def is_subscription(self, is_subscription):
        """Sets the is_subscription of this Product.


        :param is_subscription: The is_subscription of this Product.  # noqa: E501
        :type is_subscription: bool
        """
        if self.local_vars_configuration.client_side_validation and is_subscription is None:  # noqa: E501
            raise ValueError("Invalid value for `is_subscription`, must not be `None`")  # noqa: E501

        self._is_subscription = is_subscription

    @property
    def stripe_price_lookup_key(self):
        """Gets the stripe_price_lookup_key of this Product.  # noqa: E501


        :return: The stripe_price_lookup_key of this Product.  # noqa: E501
        :rtype: str
        """
        return self._stripe_price_lookup_key

    @stripe_price_lookup_key.setter
    def stripe_price_lookup_key(self, stripe_price_lookup_key):
        """Sets the stripe_price_lookup_key of this Product.


        :param stripe_price_lookup_key: The stripe_price_lookup_key of this Product.  # noqa: E501
        :type stripe_price_lookup_key: str
        """
        if (self.local_vars_configuration.client_side_validation and
                stripe_price_lookup_key is not None and len(stripe_price_lookup_key) > 255):
            raise ValueError("Invalid value for `stripe_price_lookup_key`, length must be less than or equal to `255`")  # noqa: E501

        self._stripe_price_lookup_key = stripe_price_lookup_key

    @property
    def stripe_product_id(self):
        """Gets the stripe_product_id of this Product.  # noqa: E501


        :return: The stripe_product_id of this Product.  # noqa: E501
        :rtype: str
        """
        return self._stripe_product_id

    @stripe_product_id.setter
    def stripe_product_id(self, stripe_product_id):
        """Sets the stripe_product_id of this Product.


        :param stripe_product_id: The stripe_product_id of this Product.  # noqa: E501
        :type stripe_product_id: str
        """
        if (self.local_vars_configuration.client_side_validation and
                stripe_product_id is not None and len(stripe_product_id) > 255):
            raise ValueError("Invalid value for `stripe_product_id`, length must be less than or equal to `255`")  # noqa: E501

        self._stripe_product_id = stripe_product_id

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Product):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Product):
            return True

        return self.to_dict() != other.to_dict()
