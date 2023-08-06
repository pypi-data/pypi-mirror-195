# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateGeoipRuleRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'enterprise_project_id': 'str',
        'policy_id': 'str',
        'rule_id': 'str',
        'body': 'UpdateGeoipRuleRequestBody'
    }

    attribute_map = {
        'enterprise_project_id': 'enterprise_project_id',
        'policy_id': 'policy_id',
        'rule_id': 'rule_id',
        'body': 'body'
    }

    def __init__(self, enterprise_project_id=None, policy_id=None, rule_id=None, body=None):
        """UpdateGeoipRuleRequest

        The model defined in huaweicloud sdk

        :param enterprise_project_id: 您可以通过调用企业项目管理服务（EPS）的查询企业项目列表接口（ListEnterpriseProject）查询企业项目id
        :type enterprise_project_id: str
        :param policy_id: 防护策略id，您可以通过调用查询防护策略列表（ListPolicy）获取策略id，响应体的id字段
        :type policy_id: str
        :param rule_id: 地理位置控制规则id，规则id从查询地理位置规则列表（ListGeoipRule）接口获取，响应体的id字段
        :type rule_id: str
        :param body: Body of the UpdateGeoipRuleRequest
        :type body: :class:`huaweicloudsdkwaf.v1.UpdateGeoipRuleRequestBody`
        """
        
        

        self._enterprise_project_id = None
        self._policy_id = None
        self._rule_id = None
        self._body = None
        self.discriminator = None

        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        self.policy_id = policy_id
        self.rule_id = rule_id
        if body is not None:
            self.body = body

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this UpdateGeoipRuleRequest.

        您可以通过调用企业项目管理服务（EPS）的查询企业项目列表接口（ListEnterpriseProject）查询企业项目id

        :return: The enterprise_project_id of this UpdateGeoipRuleRequest.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this UpdateGeoipRuleRequest.

        您可以通过调用企业项目管理服务（EPS）的查询企业项目列表接口（ListEnterpriseProject）查询企业项目id

        :param enterprise_project_id: The enterprise_project_id of this UpdateGeoipRuleRequest.
        :type enterprise_project_id: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def policy_id(self):
        """Gets the policy_id of this UpdateGeoipRuleRequest.

        防护策略id，您可以通过调用查询防护策略列表（ListPolicy）获取策略id，响应体的id字段

        :return: The policy_id of this UpdateGeoipRuleRequest.
        :rtype: str
        """
        return self._policy_id

    @policy_id.setter
    def policy_id(self, policy_id):
        """Sets the policy_id of this UpdateGeoipRuleRequest.

        防护策略id，您可以通过调用查询防护策略列表（ListPolicy）获取策略id，响应体的id字段

        :param policy_id: The policy_id of this UpdateGeoipRuleRequest.
        :type policy_id: str
        """
        self._policy_id = policy_id

    @property
    def rule_id(self):
        """Gets the rule_id of this UpdateGeoipRuleRequest.

        地理位置控制规则id，规则id从查询地理位置规则列表（ListGeoipRule）接口获取，响应体的id字段

        :return: The rule_id of this UpdateGeoipRuleRequest.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """Sets the rule_id of this UpdateGeoipRuleRequest.

        地理位置控制规则id，规则id从查询地理位置规则列表（ListGeoipRule）接口获取，响应体的id字段

        :param rule_id: The rule_id of this UpdateGeoipRuleRequest.
        :type rule_id: str
        """
        self._rule_id = rule_id

    @property
    def body(self):
        """Gets the body of this UpdateGeoipRuleRequest.

        :return: The body of this UpdateGeoipRuleRequest.
        :rtype: :class:`huaweicloudsdkwaf.v1.UpdateGeoipRuleRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateGeoipRuleRequest.

        :param body: The body of this UpdateGeoipRuleRequest.
        :type body: :class:`huaweicloudsdkwaf.v1.UpdateGeoipRuleRequestBody`
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
        if not isinstance(other, UpdateGeoipRuleRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
