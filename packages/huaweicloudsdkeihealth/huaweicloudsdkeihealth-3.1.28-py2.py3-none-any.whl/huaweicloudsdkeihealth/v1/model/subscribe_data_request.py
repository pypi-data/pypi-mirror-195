# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class SubscribeDataRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'eihealth_project_id': 'str',
        'body': 'SubscribeDataReq'
    }

    attribute_map = {
        'eihealth_project_id': 'eihealth_project_id',
        'body': 'body'
    }

    def __init__(self, eihealth_project_id=None, body=None):
        """SubscribeDataRequest

        The model defined in huaweicloud sdk

        :param eihealth_project_id: 资产订阅目标项目
        :type eihealth_project_id: str
        :param body: Body of the SubscribeDataRequest
        :type body: :class:`huaweicloudsdkeihealth.v1.SubscribeDataReq`
        """
        
        

        self._eihealth_project_id = None
        self._body = None
        self.discriminator = None

        self.eihealth_project_id = eihealth_project_id
        if body is not None:
            self.body = body

    @property
    def eihealth_project_id(self):
        """Gets the eihealth_project_id of this SubscribeDataRequest.

        资产订阅目标项目

        :return: The eihealth_project_id of this SubscribeDataRequest.
        :rtype: str
        """
        return self._eihealth_project_id

    @eihealth_project_id.setter
    def eihealth_project_id(self, eihealth_project_id):
        """Sets the eihealth_project_id of this SubscribeDataRequest.

        资产订阅目标项目

        :param eihealth_project_id: The eihealth_project_id of this SubscribeDataRequest.
        :type eihealth_project_id: str
        """
        self._eihealth_project_id = eihealth_project_id

    @property
    def body(self):
        """Gets the body of this SubscribeDataRequest.

        :return: The body of this SubscribeDataRequest.
        :rtype: :class:`huaweicloudsdkeihealth.v1.SubscribeDataReq`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this SubscribeDataRequest.

        :param body: The body of this SubscribeDataRequest.
        :type body: :class:`huaweicloudsdkeihealth.v1.SubscribeDataReq`
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
        if not isinstance(other, SubscribeDataRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
