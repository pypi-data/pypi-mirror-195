# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class StartGraphReq:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'graph_backup_id': 'str'
    }

    attribute_map = {
        'graph_backup_id': 'graph_backup_id'
    }

    def __init__(self, graph_backup_id=None):
        """StartGraphReq

        The model defined in huaweicloud sdk

        :param graph_backup_id: 启动图时关联的备份ID，设置此参数时，表示从备份进行启动；如果为空，表示从上次关闭图时的状态启动。
        :type graph_backup_id: str
        """
        
        

        self._graph_backup_id = None
        self.discriminator = None

        if graph_backup_id is not None:
            self.graph_backup_id = graph_backup_id

    @property
    def graph_backup_id(self):
        """Gets the graph_backup_id of this StartGraphReq.

        启动图时关联的备份ID，设置此参数时，表示从备份进行启动；如果为空，表示从上次关闭图时的状态启动。

        :return: The graph_backup_id of this StartGraphReq.
        :rtype: str
        """
        return self._graph_backup_id

    @graph_backup_id.setter
    def graph_backup_id(self, graph_backup_id):
        """Sets the graph_backup_id of this StartGraphReq.

        启动图时关联的备份ID，设置此参数时，表示从备份进行启动；如果为空，表示从上次关闭图时的状态启动。

        :param graph_backup_id: The graph_backup_id of this StartGraphReq.
        :type graph_backup_id: str
        """
        self._graph_backup_id = graph_backup_id

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
        if not isinstance(other, StartGraphReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
