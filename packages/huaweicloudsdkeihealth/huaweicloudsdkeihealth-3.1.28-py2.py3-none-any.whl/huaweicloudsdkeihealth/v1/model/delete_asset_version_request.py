# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class DeleteAssetVersionRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'asset_id': 'str',
        'version': 'str'
    }

    attribute_map = {
        'asset_id': 'asset_id',
        'version': 'version'
    }

    def __init__(self, asset_id=None, version=None):
        """DeleteAssetVersionRequest

        The model defined in huaweicloud sdk

        :param asset_id: 资产id
        :type asset_id: str
        :param version: version
        :type version: str
        """
        
        

        self._asset_id = None
        self._version = None
        self.discriminator = None

        self.asset_id = asset_id
        self.version = version

    @property
    def asset_id(self):
        """Gets the asset_id of this DeleteAssetVersionRequest.

        资产id

        :return: The asset_id of this DeleteAssetVersionRequest.
        :rtype: str
        """
        return self._asset_id

    @asset_id.setter
    def asset_id(self, asset_id):
        """Sets the asset_id of this DeleteAssetVersionRequest.

        资产id

        :param asset_id: The asset_id of this DeleteAssetVersionRequest.
        :type asset_id: str
        """
        self._asset_id = asset_id

    @property
    def version(self):
        """Gets the version of this DeleteAssetVersionRequest.

        version

        :return: The version of this DeleteAssetVersionRequest.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DeleteAssetVersionRequest.

        version

        :param version: The version of this DeleteAssetVersionRequest.
        :type version: str
        """
        self._version = version

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
        if not isinstance(other, DeleteAssetVersionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
