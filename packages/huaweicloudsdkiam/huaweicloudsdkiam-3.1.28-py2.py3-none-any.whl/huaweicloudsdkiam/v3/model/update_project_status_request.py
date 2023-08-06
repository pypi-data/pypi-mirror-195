# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateProjectStatusRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'project_id': 'str',
        'body': 'UpdateProjectStatusRequestBody'
    }

    attribute_map = {
        'project_id': 'project_id',
        'body': 'body'
    }

    def __init__(self, project_id=None, body=None):
        """UpdateProjectStatusRequest

        The model defined in huaweicloud sdk

        :param project_id: 待设置状态的项目ID，获取方式请参见：[获取账号、IAM用户、项目、用户组、委托的名称和ID](https://support.huaweicloud.com/api-iam/iam_17_0002.html)。
        :type project_id: str
        :param body: Body of the UpdateProjectStatusRequest
        :type body: :class:`huaweicloudsdkiam.v3.UpdateProjectStatusRequestBody`
        """
        
        

        self._project_id = None
        self._body = None
        self.discriminator = None

        self.project_id = project_id
        if body is not None:
            self.body = body

    @property
    def project_id(self):
        """Gets the project_id of this UpdateProjectStatusRequest.

        待设置状态的项目ID，获取方式请参见：[获取账号、IAM用户、项目、用户组、委托的名称和ID](https://support.huaweicloud.com/api-iam/iam_17_0002.html)。

        :return: The project_id of this UpdateProjectStatusRequest.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this UpdateProjectStatusRequest.

        待设置状态的项目ID，获取方式请参见：[获取账号、IAM用户、项目、用户组、委托的名称和ID](https://support.huaweicloud.com/api-iam/iam_17_0002.html)。

        :param project_id: The project_id of this UpdateProjectStatusRequest.
        :type project_id: str
        """
        self._project_id = project_id

    @property
    def body(self):
        """Gets the body of this UpdateProjectStatusRequest.

        :return: The body of this UpdateProjectStatusRequest.
        :rtype: :class:`huaweicloudsdkiam.v3.UpdateProjectStatusRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateProjectStatusRequest.

        :param body: The body of this UpdateProjectStatusRequest.
        :type body: :class:`huaweicloudsdkiam.v3.UpdateProjectStatusRequestBody`
        """
        self._body = body

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
        if not isinstance(other, UpdateProjectStatusRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
