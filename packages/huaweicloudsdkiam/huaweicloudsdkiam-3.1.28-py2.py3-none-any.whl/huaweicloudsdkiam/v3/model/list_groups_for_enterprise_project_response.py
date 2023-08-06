# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListGroupsForEnterpriseProjectResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'groups': 'list[ListGroupsForEnterpriseProjectResDetail]'
    }

    attribute_map = {
        'groups': 'groups'
    }

    def __init__(self, groups=None):
        """ListGroupsForEnterpriseProjectResponse

        The model defined in huaweicloud sdk

        :param groups: 用户组信息。
        :type groups: list[:class:`huaweicloudsdkiam.v3.ListGroupsForEnterpriseProjectResDetail`]
        """
        
        super(ListGroupsForEnterpriseProjectResponse, self).__init__()

        self._groups = None
        self.discriminator = None

        if groups is not None:
            self.groups = groups

    @property
    def groups(self):
        """Gets the groups of this ListGroupsForEnterpriseProjectResponse.

        用户组信息。

        :return: The groups of this ListGroupsForEnterpriseProjectResponse.
        :rtype: list[:class:`huaweicloudsdkiam.v3.ListGroupsForEnterpriseProjectResDetail`]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this ListGroupsForEnterpriseProjectResponse.

        用户组信息。

        :param groups: The groups of this ListGroupsForEnterpriseProjectResponse.
        :type groups: list[:class:`huaweicloudsdkiam.v3.ListGroupsForEnterpriseProjectResDetail`]
        """
        self._groups = groups

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
        if not isinstance(other, ListGroupsForEnterpriseProjectResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
