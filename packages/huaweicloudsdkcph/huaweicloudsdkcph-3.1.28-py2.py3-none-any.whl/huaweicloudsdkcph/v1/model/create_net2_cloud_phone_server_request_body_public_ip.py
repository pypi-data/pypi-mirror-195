# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateNet2CloudPhoneServerRequestBodyPublicIp:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'ids': 'list[str]',
        'eip': 'CreateNet2CloudPhoneServerRequestBodyPublicIpEip'
    }

    attribute_map = {
        'ids': 'ids',
        'eip': 'eip'
    }

    def __init__(self, ids=None, eip=None):
        """CreateNet2CloudPhoneServerRequestBodyPublicIp

        The model defined in huaweicloud sdk

        :param ids: 指定已有的EIP进行服务器创建，当前只支持传入一个已有的EIP ID
        :type ids: list[str]
        :param eip: 
        :type eip: :class:`huaweicloudsdkcph.v1.CreateNet2CloudPhoneServerRequestBodyPublicIpEip`
        """
        
        

        self._ids = None
        self._eip = None
        self.discriminator = None

        if ids is not None:
            self.ids = ids
        if eip is not None:
            self.eip = eip

    @property
    def ids(self):
        """Gets the ids of this CreateNet2CloudPhoneServerRequestBodyPublicIp.

        指定已有的EIP进行服务器创建，当前只支持传入一个已有的EIP ID

        :return: The ids of this CreateNet2CloudPhoneServerRequestBodyPublicIp.
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this CreateNet2CloudPhoneServerRequestBodyPublicIp.

        指定已有的EIP进行服务器创建，当前只支持传入一个已有的EIP ID

        :param ids: The ids of this CreateNet2CloudPhoneServerRequestBodyPublicIp.
        :type ids: list[str]
        """
        self._ids = ids

    @property
    def eip(self):
        """Gets the eip of this CreateNet2CloudPhoneServerRequestBodyPublicIp.

        :return: The eip of this CreateNet2CloudPhoneServerRequestBodyPublicIp.
        :rtype: :class:`huaweicloudsdkcph.v1.CreateNet2CloudPhoneServerRequestBodyPublicIpEip`
        """
        return self._eip

    @eip.setter
    def eip(self, eip):
        """Sets the eip of this CreateNet2CloudPhoneServerRequestBodyPublicIp.

        :param eip: The eip of this CreateNet2CloudPhoneServerRequestBodyPublicIp.
        :type eip: :class:`huaweicloudsdkcph.v1.CreateNet2CloudPhoneServerRequestBodyPublicIpEip`
        """
        self._eip = eip

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
        if not isinstance(other, CreateNet2CloudPhoneServerRequestBodyPublicIp):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
