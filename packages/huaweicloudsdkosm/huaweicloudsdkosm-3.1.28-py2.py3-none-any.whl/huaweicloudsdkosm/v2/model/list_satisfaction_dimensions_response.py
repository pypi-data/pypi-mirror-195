# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListSatisfactionDimensionsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'total_count': 'int',
        'satisfaction_dimension_list': 'list[SatisfactionDimensionSimpleInfoV2]'
    }

    attribute_map = {
        'total_count': 'total_count',
        'satisfaction_dimension_list': 'satisfaction_dimension_list'
    }

    def __init__(self, total_count=None, satisfaction_dimension_list=None):
        """ListSatisfactionDimensionsResponse

        The model defined in huaweicloud sdk

        :param total_count: 总数
        :type total_count: int
        :param satisfaction_dimension_list: 满意度分类列表
        :type satisfaction_dimension_list: list[:class:`huaweicloudsdkosm.v2.SatisfactionDimensionSimpleInfoV2`]
        """
        
        super(ListSatisfactionDimensionsResponse, self).__init__()

        self._total_count = None
        self._satisfaction_dimension_list = None
        self.discriminator = None

        if total_count is not None:
            self.total_count = total_count
        if satisfaction_dimension_list is not None:
            self.satisfaction_dimension_list = satisfaction_dimension_list

    @property
    def total_count(self):
        """Gets the total_count of this ListSatisfactionDimensionsResponse.

        总数

        :return: The total_count of this ListSatisfactionDimensionsResponse.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """Sets the total_count of this ListSatisfactionDimensionsResponse.

        总数

        :param total_count: The total_count of this ListSatisfactionDimensionsResponse.
        :type total_count: int
        """
        self._total_count = total_count

    @property
    def satisfaction_dimension_list(self):
        """Gets the satisfaction_dimension_list of this ListSatisfactionDimensionsResponse.

        满意度分类列表

        :return: The satisfaction_dimension_list of this ListSatisfactionDimensionsResponse.
        :rtype: list[:class:`huaweicloudsdkosm.v2.SatisfactionDimensionSimpleInfoV2`]
        """
        return self._satisfaction_dimension_list

    @satisfaction_dimension_list.setter
    def satisfaction_dimension_list(self, satisfaction_dimension_list):
        """Sets the satisfaction_dimension_list of this ListSatisfactionDimensionsResponse.

        满意度分类列表

        :param satisfaction_dimension_list: The satisfaction_dimension_list of this ListSatisfactionDimensionsResponse.
        :type satisfaction_dimension_list: list[:class:`huaweicloudsdkosm.v2.SatisfactionDimensionSimpleInfoV2`]
        """
        self._satisfaction_dimension_list = satisfaction_dimension_list

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
        if not isinstance(other, ListSatisfactionDimensionsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
