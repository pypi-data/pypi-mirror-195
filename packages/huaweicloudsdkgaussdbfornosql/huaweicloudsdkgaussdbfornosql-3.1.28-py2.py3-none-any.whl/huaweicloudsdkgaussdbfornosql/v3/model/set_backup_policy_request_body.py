# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class SetBackupPolicyRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'backup_policy': 'BackupPolicy'
    }

    attribute_map = {
        'backup_policy': 'backup_policy'
    }

    def __init__(self, backup_policy=None):
        """SetBackupPolicyRequestBody

        The model defined in huaweicloud sdk

        :param backup_policy: 
        :type backup_policy: :class:`huaweicloudsdkgaussdbfornosql.v3.BackupPolicy`
        """
        
        

        self._backup_policy = None
        self.discriminator = None

        self.backup_policy = backup_policy

    @property
    def backup_policy(self):
        """Gets the backup_policy of this SetBackupPolicyRequestBody.

        :return: The backup_policy of this SetBackupPolicyRequestBody.
        :rtype: :class:`huaweicloudsdkgaussdbfornosql.v3.BackupPolicy`
        """
        return self._backup_policy

    @backup_policy.setter
    def backup_policy(self, backup_policy):
        """Sets the backup_policy of this SetBackupPolicyRequestBody.

        :param backup_policy: The backup_policy of this SetBackupPolicyRequestBody.
        :type backup_policy: :class:`huaweicloudsdkgaussdbfornosql.v3.BackupPolicy`
        """
        self._backup_policy = backup_policy

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
        if not isinstance(other, SetBackupPolicyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
