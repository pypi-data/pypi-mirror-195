# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListLiveDataApiTestHistoryV2Request:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'instance_id': 'str',
        'ld_api_id': 'str',
        'offset': 'int',
        'limit': 'int'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'ld_api_id': 'ld_api_id',
        'offset': 'offset',
        'limit': 'limit'
    }

    def __init__(self, instance_id=None, ld_api_id=None, offset=None, limit=None):
        """ListLiveDataApiTestHistoryV2Request

        The model defined in huaweicloud sdk

        :param instance_id: 实例ID
        :type instance_id: str
        :param ld_api_id: 后端API的编号
        :type ld_api_id: str
        :param offset: 偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0
        :type offset: int
        :param limit: 每页显示的条目数量
        :type limit: int
        """
        
        

        self._instance_id = None
        self._ld_api_id = None
        self._offset = None
        self._limit = None
        self.discriminator = None

        self.instance_id = instance_id
        self.ld_api_id = ld_api_id
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit

    @property
    def instance_id(self):
        """Gets the instance_id of this ListLiveDataApiTestHistoryV2Request.

        实例ID

        :return: The instance_id of this ListLiveDataApiTestHistoryV2Request.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ListLiveDataApiTestHistoryV2Request.

        实例ID

        :param instance_id: The instance_id of this ListLiveDataApiTestHistoryV2Request.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def ld_api_id(self):
        """Gets the ld_api_id of this ListLiveDataApiTestHistoryV2Request.

        后端API的编号

        :return: The ld_api_id of this ListLiveDataApiTestHistoryV2Request.
        :rtype: str
        """
        return self._ld_api_id

    @ld_api_id.setter
    def ld_api_id(self, ld_api_id):
        """Sets the ld_api_id of this ListLiveDataApiTestHistoryV2Request.

        后端API的编号

        :param ld_api_id: The ld_api_id of this ListLiveDataApiTestHistoryV2Request.
        :type ld_api_id: str
        """
        self._ld_api_id = ld_api_id

    @property
    def offset(self):
        """Gets the offset of this ListLiveDataApiTestHistoryV2Request.

        偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0

        :return: The offset of this ListLiveDataApiTestHistoryV2Request.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListLiveDataApiTestHistoryV2Request.

        偏移量，表示从此偏移量开始查询，偏移量小于0时，自动转换为0

        :param offset: The offset of this ListLiveDataApiTestHistoryV2Request.
        :type offset: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this ListLiveDataApiTestHistoryV2Request.

        每页显示的条目数量

        :return: The limit of this ListLiveDataApiTestHistoryV2Request.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListLiveDataApiTestHistoryV2Request.

        每页显示的条目数量

        :param limit: The limit of this ListLiveDataApiTestHistoryV2Request.
        :type limit: int
        """
        self._limit = limit

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
        if not isinstance(other, ListLiveDataApiTestHistoryV2Request):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
