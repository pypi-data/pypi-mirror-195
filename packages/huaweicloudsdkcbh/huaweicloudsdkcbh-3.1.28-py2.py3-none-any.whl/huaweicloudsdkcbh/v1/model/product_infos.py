# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ProductInfos:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'product_id': 'str',
        'cloud_service_type': 'str',
        'resource_type': 'str',
        'resource_spec_code': 'str',
        'available_zone_id': 'str',
        'resource_size_measure_id': 'str',
        'resource_size': 'str'
    }

    attribute_map = {
        'product_id': 'product_id',
        'cloud_service_type': 'cloud_service_type',
        'resource_type': 'resource_type',
        'resource_spec_code': 'resource_spec_code',
        'available_zone_id': 'available_zone_id',
        'resource_size_measure_id': 'resource_size_measure_id',
        'resource_size': 'resource_size'
    }

    def __init__(self, product_id=None, cloud_service_type=None, resource_type=None, resource_spec_code=None, available_zone_id=None, resource_size_measure_id=None, resource_size=None):
        """ProductInfos

        The model defined in huaweicloud sdk

        :param product_id: 产品标识，通过订购询价接口获得
        :type product_id: str
        :param cloud_service_type: CBH云服务类型
        :type cloud_service_type: str
        :param resource_type: CBH资源类型
        :type resource_type: str
        :param resource_spec_code: CBH资源规格
        :type resource_spec_code: str
        :param available_zone_id: 可用区id
        :type available_zone_id: str
        :param resource_size_measure_id: 资源容量度量标识
        :type resource_size_measure_id: str
        :param resource_size: 资源容量大小
        :type resource_size: str
        """
        
        

        self._product_id = None
        self._cloud_service_type = None
        self._resource_type = None
        self._resource_spec_code = None
        self._available_zone_id = None
        self._resource_size_measure_id = None
        self._resource_size = None
        self.discriminator = None

        self.product_id = product_id
        self.cloud_service_type = cloud_service_type
        self.resource_type = resource_type
        self.resource_spec_code = resource_spec_code
        if available_zone_id is not None:
            self.available_zone_id = available_zone_id
        self.resource_size_measure_id = resource_size_measure_id
        self.resource_size = resource_size

    @property
    def product_id(self):
        """Gets the product_id of this ProductInfos.

        产品标识，通过订购询价接口获得

        :return: The product_id of this ProductInfos.
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this ProductInfos.

        产品标识，通过订购询价接口获得

        :param product_id: The product_id of this ProductInfos.
        :type product_id: str
        """
        self._product_id = product_id

    @property
    def cloud_service_type(self):
        """Gets the cloud_service_type of this ProductInfos.

        CBH云服务类型

        :return: The cloud_service_type of this ProductInfos.
        :rtype: str
        """
        return self._cloud_service_type

    @cloud_service_type.setter
    def cloud_service_type(self, cloud_service_type):
        """Sets the cloud_service_type of this ProductInfos.

        CBH云服务类型

        :param cloud_service_type: The cloud_service_type of this ProductInfos.
        :type cloud_service_type: str
        """
        self._cloud_service_type = cloud_service_type

    @property
    def resource_type(self):
        """Gets the resource_type of this ProductInfos.

        CBH资源类型

        :return: The resource_type of this ProductInfos.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this ProductInfos.

        CBH资源类型

        :param resource_type: The resource_type of this ProductInfos.
        :type resource_type: str
        """
        self._resource_type = resource_type

    @property
    def resource_spec_code(self):
        """Gets the resource_spec_code of this ProductInfos.

        CBH资源规格

        :return: The resource_spec_code of this ProductInfos.
        :rtype: str
        """
        return self._resource_spec_code

    @resource_spec_code.setter
    def resource_spec_code(self, resource_spec_code):
        """Sets the resource_spec_code of this ProductInfos.

        CBH资源规格

        :param resource_spec_code: The resource_spec_code of this ProductInfos.
        :type resource_spec_code: str
        """
        self._resource_spec_code = resource_spec_code

    @property
    def available_zone_id(self):
        """Gets the available_zone_id of this ProductInfos.

        可用区id

        :return: The available_zone_id of this ProductInfos.
        :rtype: str
        """
        return self._available_zone_id

    @available_zone_id.setter
    def available_zone_id(self, available_zone_id):
        """Sets the available_zone_id of this ProductInfos.

        可用区id

        :param available_zone_id: The available_zone_id of this ProductInfos.
        :type available_zone_id: str
        """
        self._available_zone_id = available_zone_id

    @property
    def resource_size_measure_id(self):
        """Gets the resource_size_measure_id of this ProductInfos.

        资源容量度量标识

        :return: The resource_size_measure_id of this ProductInfos.
        :rtype: str
        """
        return self._resource_size_measure_id

    @resource_size_measure_id.setter
    def resource_size_measure_id(self, resource_size_measure_id):
        """Sets the resource_size_measure_id of this ProductInfos.

        资源容量度量标识

        :param resource_size_measure_id: The resource_size_measure_id of this ProductInfos.
        :type resource_size_measure_id: str
        """
        self._resource_size_measure_id = resource_size_measure_id

    @property
    def resource_size(self):
        """Gets the resource_size of this ProductInfos.

        资源容量大小

        :return: The resource_size of this ProductInfos.
        :rtype: str
        """
        return self._resource_size

    @resource_size.setter
    def resource_size(self, resource_size):
        """Sets the resource_size of this ProductInfos.

        资源容量大小

        :param resource_size: The resource_size of this ProductInfos.
        :type resource_size: str
        """
        self._resource_size = resource_size

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProductInfos):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
