# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateSpec:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'spec_code': 'str',
        'stride_num': 'int'
    }

    attribute_map = {
        'spec_code': 'spec_code',
        'stride_num': 'stride_num'
    }

    def __init__(self, spec_code=None, stride_num=None):
        """CreateSpec

        The model defined in huaweicloud sdk

        :param spec_code: 规格编码
        :type spec_code: str
        :param stride_num: 步数
        :type stride_num: int
        """
        
        

        self._spec_code = None
        self._stride_num = None
        self.discriminator = None

        self.spec_code = spec_code
        self.stride_num = stride_num

    @property
    def spec_code(self):
        """Gets the spec_code of this CreateSpec.

        规格编码

        :return: The spec_code of this CreateSpec.
        :rtype: str
        """
        return self._spec_code

    @spec_code.setter
    def spec_code(self, spec_code):
        """Sets the spec_code of this CreateSpec.

        规格编码

        :param spec_code: The spec_code of this CreateSpec.
        :type spec_code: str
        """
        self._spec_code = spec_code

    @property
    def stride_num(self):
        """Gets the stride_num of this CreateSpec.

        步数

        :return: The stride_num of this CreateSpec.
        :rtype: int
        """
        return self._stride_num

    @stride_num.setter
    def stride_num(self, stride_num):
        """Sets the stride_num of this CreateSpec.

        步数

        :param stride_num: The stride_num of this CreateSpec.
        :type stride_num: int
        """
        self._stride_num = stride_num

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
        if not isinstance(other, CreateSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
