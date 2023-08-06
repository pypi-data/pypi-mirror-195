# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class DomainClassificationItem:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'total': 'int',
        'items': 'list[DomainItem]'
    }

    attribute_map = {
        'total': 'total',
        'items': 'items'
    }

    def __init__(self, total=None, items=None):
        """DomainClassificationItem

        The model defined in huaweicloud sdk

        :param total: DomainItem的总数量
        :type total: int
        :param items: DomainItem详细信息
        :type items: list[:class:`huaweicloudsdkwaf.v1.DomainItem`]
        """
        
        

        self._total = None
        self._items = None
        self.discriminator = None

        if total is not None:
            self.total = total
        if items is not None:
            self.items = items

    @property
    def total(self):
        """Gets the total of this DomainClassificationItem.

        DomainItem的总数量

        :return: The total of this DomainClassificationItem.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this DomainClassificationItem.

        DomainItem的总数量

        :param total: The total of this DomainClassificationItem.
        :type total: int
        """
        self._total = total

    @property
    def items(self):
        """Gets the items of this DomainClassificationItem.

        DomainItem详细信息

        :return: The items of this DomainClassificationItem.
        :rtype: list[:class:`huaweicloudsdkwaf.v1.DomainItem`]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this DomainClassificationItem.

        DomainItem详细信息

        :param items: The items of this DomainClassificationItem.
        :type items: list[:class:`huaweicloudsdkwaf.v1.DomainItem`]
        """
        self._items = items

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
        if not isinstance(other, DomainClassificationItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
