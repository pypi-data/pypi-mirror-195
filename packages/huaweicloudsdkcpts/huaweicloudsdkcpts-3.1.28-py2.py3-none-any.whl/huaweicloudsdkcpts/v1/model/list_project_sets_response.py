# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListProjectSetsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'code': 'str',
        'message': 'str',
        'projects': 'list[ProjectsSet]'
    }

    attribute_map = {
        'code': 'code',
        'message': 'message',
        'projects': 'projects'
    }

    def __init__(self, code=None, message=None, projects=None):
        """ListProjectSetsResponse

        The model defined in huaweicloud sdk

        :param code: 状态码
        :type code: str
        :param message: 描述
        :type message: str
        :param projects: 工程集详细信息
        :type projects: list[:class:`huaweicloudsdkcpts.v1.ProjectsSet`]
        """
        
        super(ListProjectSetsResponse, self).__init__()

        self._code = None
        self._message = None
        self._projects = None
        self.discriminator = None

        if code is not None:
            self.code = code
        if message is not None:
            self.message = message
        if projects is not None:
            self.projects = projects

    @property
    def code(self):
        """Gets the code of this ListProjectSetsResponse.

        状态码

        :return: The code of this ListProjectSetsResponse.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this ListProjectSetsResponse.

        状态码

        :param code: The code of this ListProjectSetsResponse.
        :type code: str
        """
        self._code = code

    @property
    def message(self):
        """Gets the message of this ListProjectSetsResponse.

        描述

        :return: The message of this ListProjectSetsResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ListProjectSetsResponse.

        描述

        :param message: The message of this ListProjectSetsResponse.
        :type message: str
        """
        self._message = message

    @property
    def projects(self):
        """Gets the projects of this ListProjectSetsResponse.

        工程集详细信息

        :return: The projects of this ListProjectSetsResponse.
        :rtype: list[:class:`huaweicloudsdkcpts.v1.ProjectsSet`]
        """
        return self._projects

    @projects.setter
    def projects(self, projects):
        """Sets the projects of this ListProjectSetsResponse.

        工程集详细信息

        :param projects: The projects of this ListProjectSetsResponse.
        :type projects: list[:class:`huaweicloudsdkcpts.v1.ProjectsSet`]
        """
        self._projects = projects

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
        if not isinstance(other, ListProjectSetsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
