# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class DeleteServerMetadataRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'key': 'str',
        'server_id': 'str'
    }

    attribute_map = {
        'key': 'key',
        'server_id': 'server_id'
    }

    def __init__(self, key=None, server_id=None):
        """DeleteServerMetadataRequest

        The model defined in huaweicloud sdk

        :param key: 待删除的云服务器metadata键值
        :type key: str
        :param server_id: 云服务器ID。
        :type server_id: str
        """
        
        

        self._key = None
        self._server_id = None
        self.discriminator = None

        self.key = key
        self.server_id = server_id

    @property
    def key(self):
        """Gets the key of this DeleteServerMetadataRequest.

        待删除的云服务器metadata键值

        :return: The key of this DeleteServerMetadataRequest.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this DeleteServerMetadataRequest.

        待删除的云服务器metadata键值

        :param key: The key of this DeleteServerMetadataRequest.
        :type key: str
        """
        self._key = key

    @property
    def server_id(self):
        """Gets the server_id of this DeleteServerMetadataRequest.

        云服务器ID。

        :return: The server_id of this DeleteServerMetadataRequest.
        :rtype: str
        """
        return self._server_id

    @server_id.setter
    def server_id(self, server_id):
        """Sets the server_id of this DeleteServerMetadataRequest.

        云服务器ID。

        :param server_id: The server_id of this DeleteServerMetadataRequest.
        :type server_id: str
        """
        self._server_id = server_id

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
        if not isinstance(other, DeleteServerMetadataRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
