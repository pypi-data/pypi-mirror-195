# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowPartitionMessageRequest:

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
        'topic': 'str',
        'partition': 'int',
        'message_offset': 'str'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'topic': 'topic',
        'partition': 'partition',
        'message_offset': 'message_offset'
    }

    def __init__(self, instance_id=None, topic=None, partition=None, message_offset=None):
        """ShowPartitionMessageRequest

        The model defined in huaweicloud sdk

        :param instance_id: 实例ID。
        :type instance_id: str
        :param topic: Topic名称。  Topic名称必现以字母开头且只支持大小写字母、中横线、下划线以及数字。
        :type topic: str
        :param partition: 分区编号。
        :type partition: int
        :param message_offset: 消息位置。
        :type message_offset: str
        """
        
        

        self._instance_id = None
        self._topic = None
        self._partition = None
        self._message_offset = None
        self.discriminator = None

        self.instance_id = instance_id
        self.topic = topic
        self.partition = partition
        self.message_offset = message_offset

    @property
    def instance_id(self):
        """Gets the instance_id of this ShowPartitionMessageRequest.

        实例ID。

        :return: The instance_id of this ShowPartitionMessageRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ShowPartitionMessageRequest.

        实例ID。

        :param instance_id: The instance_id of this ShowPartitionMessageRequest.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def topic(self):
        """Gets the topic of this ShowPartitionMessageRequest.

        Topic名称。  Topic名称必现以字母开头且只支持大小写字母、中横线、下划线以及数字。

        :return: The topic of this ShowPartitionMessageRequest.
        :rtype: str
        """
        return self._topic

    @topic.setter
    def topic(self, topic):
        """Sets the topic of this ShowPartitionMessageRequest.

        Topic名称。  Topic名称必现以字母开头且只支持大小写字母、中横线、下划线以及数字。

        :param topic: The topic of this ShowPartitionMessageRequest.
        :type topic: str
        """
        self._topic = topic

    @property
    def partition(self):
        """Gets the partition of this ShowPartitionMessageRequest.

        分区编号。

        :return: The partition of this ShowPartitionMessageRequest.
        :rtype: int
        """
        return self._partition

    @partition.setter
    def partition(self, partition):
        """Sets the partition of this ShowPartitionMessageRequest.

        分区编号。

        :param partition: The partition of this ShowPartitionMessageRequest.
        :type partition: int
        """
        self._partition = partition

    @property
    def message_offset(self):
        """Gets the message_offset of this ShowPartitionMessageRequest.

        消息位置。

        :return: The message_offset of this ShowPartitionMessageRequest.
        :rtype: str
        """
        return self._message_offset

    @message_offset.setter
    def message_offset(self, message_offset):
        """Sets the message_offset of this ShowPartitionMessageRequest.

        消息位置。

        :param message_offset: The message_offset of this ShowPartitionMessageRequest.
        :type message_offset: str
        """
        self._message_offset = message_offset

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
        if not isinstance(other, ShowPartitionMessageRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
