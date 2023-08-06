# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ErrorCaseInfoBean:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'error_code': 'str',
        'error_msg': 'str',
        'testcase_id': 'str'
    }

    attribute_map = {
        'error_code': 'error_code',
        'error_msg': 'error_msg',
        'testcase_id': 'testcase_id'
    }

    def __init__(self, error_code=None, error_msg=None, testcase_id=None):
        """ErrorCaseInfoBean

        The model defined in huaweicloud sdk

        :param error_code: 失败错误码
        :type error_code: str
        :param error_msg: 失败错误信息
        :type error_msg: str
        :param testcase_id: 失败资源信息
        :type testcase_id: str
        """
        
        

        self._error_code = None
        self._error_msg = None
        self._testcase_id = None
        self.discriminator = None

        if error_code is not None:
            self.error_code = error_code
        if error_msg is not None:
            self.error_msg = error_msg
        if testcase_id is not None:
            self.testcase_id = testcase_id

    @property
    def error_code(self):
        """Gets the error_code of this ErrorCaseInfoBean.

        失败错误码

        :return: The error_code of this ErrorCaseInfoBean.
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code):
        """Sets the error_code of this ErrorCaseInfoBean.

        失败错误码

        :param error_code: The error_code of this ErrorCaseInfoBean.
        :type error_code: str
        """
        self._error_code = error_code

    @property
    def error_msg(self):
        """Gets the error_msg of this ErrorCaseInfoBean.

        失败错误信息

        :return: The error_msg of this ErrorCaseInfoBean.
        :rtype: str
        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, error_msg):
        """Sets the error_msg of this ErrorCaseInfoBean.

        失败错误信息

        :param error_msg: The error_msg of this ErrorCaseInfoBean.
        :type error_msg: str
        """
        self._error_msg = error_msg

    @property
    def testcase_id(self):
        """Gets the testcase_id of this ErrorCaseInfoBean.

        失败资源信息

        :return: The testcase_id of this ErrorCaseInfoBean.
        :rtype: str
        """
        return self._testcase_id

    @testcase_id.setter
    def testcase_id(self, testcase_id):
        """Sets the testcase_id of this ErrorCaseInfoBean.

        失败资源信息

        :param testcase_id: The testcase_id of this ErrorCaseInfoBean.
        :type testcase_id: str
        """
        self._testcase_id = testcase_id

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
        if not isinstance(other, ErrorCaseInfoBean):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
