# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class OsVersionResponse:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'status': 'str',
        'id': 'str',
        'links': 'list[Links]'
    }

    attribute_map = {
        'status': 'status',
        'id': 'id',
        'links': 'links'
    }

    def __init__(self, status=None, id=None, links=None):
        """OsVersionResponse

        The model defined in huaweicloud sdk

        :param status: 接口状态。
        :type status: str
        :param id: 接口ID。
        :type id: str
        :param links: 自描述信息。
        :type links: list[:class:`huaweicloudsdkims.v2.Links`]
        """
        
        

        self._status = None
        self._id = None
        self._links = None
        self.discriminator = None

        self.status = status
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links

    @property
    def status(self):
        """Gets the status of this OsVersionResponse.

        接口状态。

        :return: The status of this OsVersionResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OsVersionResponse.

        接口状态。

        :param status: The status of this OsVersionResponse.
        :type status: str
        """
        self._status = status

    @property
    def id(self):
        """Gets the id of this OsVersionResponse.

        接口ID。

        :return: The id of this OsVersionResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OsVersionResponse.

        接口ID。

        :param id: The id of this OsVersionResponse.
        :type id: str
        """
        self._id = id

    @property
    def links(self):
        """Gets the links of this OsVersionResponse.

        自描述信息。

        :return: The links of this OsVersionResponse.
        :rtype: list[:class:`huaweicloudsdkims.v2.Links`]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this OsVersionResponse.

        自描述信息。

        :param links: The links of this OsVersionResponse.
        :type links: list[:class:`huaweicloudsdkims.v2.Links`]
        """
        self._links = links

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
        if not isinstance(other, OsVersionResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
