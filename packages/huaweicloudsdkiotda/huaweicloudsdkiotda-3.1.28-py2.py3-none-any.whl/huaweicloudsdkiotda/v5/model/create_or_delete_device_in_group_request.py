# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateOrDeleteDeviceInGroupRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'instance_id': 'str',
        'group_id': 'str',
        'action_id': 'str',
        'device_id': 'str'
    }

    attribute_map = {
        'instance_id': 'Instance-Id',
        'group_id': 'group_id',
        'action_id': 'action_id',
        'device_id': 'device_id'
    }

    def __init__(self, instance_id=None, group_id=None, action_id=None, device_id=None):
        """CreateOrDeleteDeviceInGroupRequest

        The model defined in huaweicloud sdk

        :param instance_id: **参数说明**：实例ID。物理多租下各实例的唯一标识，一般华为云租户无需携带该参数，仅在物理多租场景下从管理面访问API时需要携带该参数。您可以在IoTDA管理控制台界面，选择左侧导航栏“总览”页签查看当前实例的ID
        :type instance_id: str
        :param group_id: **参数说明**：设备组ID，用于唯一标识一个设备组，在创建设备组时由物联网平台分配。 **取值范围**：长度不超过36，十六进制字符串和连接符（-）的组合
        :type group_id: str
        :param action_id: **参数说明**：操作类型，支持添加设备和删除设备。 **取值范围**： - addDevice: 添加设备。添加已注册的设备到指定的设备组中。 - removeDevice: 删除设备。从指定的设备组中删除设备，只是解除了设备和设备组的关系，该设备在平台仍然存在。
        :type action_id: str
        :param device_id: **参数说明**：设备ID，用于唯一标识一个设备。在注册设备时直接指定，或者由物联网平台分配获得。由物联网平台分配时，生成规则为\&quot;product_id\&quot; + \&quot;_\&quot; + \&quot;node_id\&quot;拼接而成。 **取值范围**：长度不超过128，只允许字母、数字、下划线（_）、连接符（-）的组合。
        :type device_id: str
        """
        
        

        self._instance_id = None
        self._group_id = None
        self._action_id = None
        self._device_id = None
        self.discriminator = None

        if instance_id is not None:
            self.instance_id = instance_id
        self.group_id = group_id
        self.action_id = action_id
        self.device_id = device_id

    @property
    def instance_id(self):
        """Gets the instance_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：实例ID。物理多租下各实例的唯一标识，一般华为云租户无需携带该参数，仅在物理多租场景下从管理面访问API时需要携带该参数。您可以在IoTDA管理控制台界面，选择左侧导航栏“总览”页签查看当前实例的ID

        :return: The instance_id of this CreateOrDeleteDeviceInGroupRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：实例ID。物理多租下各实例的唯一标识，一般华为云租户无需携带该参数，仅在物理多租场景下从管理面访问API时需要携带该参数。您可以在IoTDA管理控制台界面，选择左侧导航栏“总览”页签查看当前实例的ID

        :param instance_id: The instance_id of this CreateOrDeleteDeviceInGroupRequest.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def group_id(self):
        """Gets the group_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：设备组ID，用于唯一标识一个设备组，在创建设备组时由物联网平台分配。 **取值范围**：长度不超过36，十六进制字符串和连接符（-）的组合

        :return: The group_id of this CreateOrDeleteDeviceInGroupRequest.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """Sets the group_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：设备组ID，用于唯一标识一个设备组，在创建设备组时由物联网平台分配。 **取值范围**：长度不超过36，十六进制字符串和连接符（-）的组合

        :param group_id: The group_id of this CreateOrDeleteDeviceInGroupRequest.
        :type group_id: str
        """
        self._group_id = group_id

    @property
    def action_id(self):
        """Gets the action_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：操作类型，支持添加设备和删除设备。 **取值范围**： - addDevice: 添加设备。添加已注册的设备到指定的设备组中。 - removeDevice: 删除设备。从指定的设备组中删除设备，只是解除了设备和设备组的关系，该设备在平台仍然存在。

        :return: The action_id of this CreateOrDeleteDeviceInGroupRequest.
        :rtype: str
        """
        return self._action_id

    @action_id.setter
    def action_id(self, action_id):
        """Sets the action_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：操作类型，支持添加设备和删除设备。 **取值范围**： - addDevice: 添加设备。添加已注册的设备到指定的设备组中。 - removeDevice: 删除设备。从指定的设备组中删除设备，只是解除了设备和设备组的关系，该设备在平台仍然存在。

        :param action_id: The action_id of this CreateOrDeleteDeviceInGroupRequest.
        :type action_id: str
        """
        self._action_id = action_id

    @property
    def device_id(self):
        """Gets the device_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：设备ID，用于唯一标识一个设备。在注册设备时直接指定，或者由物联网平台分配获得。由物联网平台分配时，生成规则为\"product_id\" + \"_\" + \"node_id\"拼接而成。 **取值范围**：长度不超过128，只允许字母、数字、下划线（_）、连接符（-）的组合。

        :return: The device_id of this CreateOrDeleteDeviceInGroupRequest.
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        """Sets the device_id of this CreateOrDeleteDeviceInGroupRequest.

        **参数说明**：设备ID，用于唯一标识一个设备。在注册设备时直接指定，或者由物联网平台分配获得。由物联网平台分配时，生成规则为\"product_id\" + \"_\" + \"node_id\"拼接而成。 **取值范围**：长度不超过128，只允许字母、数字、下划线（_）、连接符（-）的组合。

        :param device_id: The device_id of this CreateOrDeleteDeviceInGroupRequest.
        :type device_id: str
        """
        self._device_id = device_id

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
        if not isinstance(other, CreateOrDeleteDeviceInGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
