# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowUpdateObjectSavingStatusRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'job_id': 'str',
        'x_language': 'str',
        'query_id': 'str'
    }

    attribute_map = {
        'job_id': 'job_id',
        'x_language': 'X-Language',
        'query_id': 'query_id'
    }

    def __init__(self, job_id=None, x_language=None, query_id=None):
        """ShowUpdateObjectSavingStatusRequest

        The model defined in huaweicloud sdk

        :param job_id: 任务ID。
        :type job_id: str
        :param x_language: 请求语言类型。
        :type x_language: str
        :param query_id: 保存对象接口返回的ID。
        :type query_id: str
        """
        
        

        self._job_id = None
        self._x_language = None
        self._query_id = None
        self.discriminator = None

        self.job_id = job_id
        if x_language is not None:
            self.x_language = x_language
        self.query_id = query_id

    @property
    def job_id(self):
        """Gets the job_id of this ShowUpdateObjectSavingStatusRequest.

        任务ID。

        :return: The job_id of this ShowUpdateObjectSavingStatusRequest.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this ShowUpdateObjectSavingStatusRequest.

        任务ID。

        :param job_id: The job_id of this ShowUpdateObjectSavingStatusRequest.
        :type job_id: str
        """
        self._job_id = job_id

    @property
    def x_language(self):
        """Gets the x_language of this ShowUpdateObjectSavingStatusRequest.

        请求语言类型。

        :return: The x_language of this ShowUpdateObjectSavingStatusRequest.
        :rtype: str
        """
        return self._x_language

    @x_language.setter
    def x_language(self, x_language):
        """Sets the x_language of this ShowUpdateObjectSavingStatusRequest.

        请求语言类型。

        :param x_language: The x_language of this ShowUpdateObjectSavingStatusRequest.
        :type x_language: str
        """
        self._x_language = x_language

    @property
    def query_id(self):
        """Gets the query_id of this ShowUpdateObjectSavingStatusRequest.

        保存对象接口返回的ID。

        :return: The query_id of this ShowUpdateObjectSavingStatusRequest.
        :rtype: str
        """
        return self._query_id

    @query_id.setter
    def query_id(self, query_id):
        """Sets the query_id of this ShowUpdateObjectSavingStatusRequest.

        保存对象接口返回的ID。

        :param query_id: The query_id of this ShowUpdateObjectSavingStatusRequest.
        :type query_id: str
        """
        self._query_id = query_id

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
        if not isinstance(other, ShowUpdateObjectSavingStatusRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
