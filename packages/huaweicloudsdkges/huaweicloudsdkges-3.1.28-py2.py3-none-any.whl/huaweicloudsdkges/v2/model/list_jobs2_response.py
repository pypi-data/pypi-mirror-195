# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListJobs2Response(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'job_count': 'int',
        'job_list': 'list[ListJobsRespJobList]'
    }

    attribute_map = {
        'job_count': 'job_count',
        'job_list': 'job_list'
    }

    def __init__(self, job_count=None, job_list=None):
        """ListJobs2Response

        The model defined in huaweicloud sdk

        :param job_count: 任务总数。
        :type job_count: int
        :param job_list: 任务列表。
        :type job_list: list[:class:`huaweicloudsdkges.v2.ListJobsRespJobList`]
        """
        
        super(ListJobs2Response, self).__init__()

        self._job_count = None
        self._job_list = None
        self.discriminator = None

        if job_count is not None:
            self.job_count = job_count
        if job_list is not None:
            self.job_list = job_list

    @property
    def job_count(self):
        """Gets the job_count of this ListJobs2Response.

        任务总数。

        :return: The job_count of this ListJobs2Response.
        :rtype: int
        """
        return self._job_count

    @job_count.setter
    def job_count(self, job_count):
        """Sets the job_count of this ListJobs2Response.

        任务总数。

        :param job_count: The job_count of this ListJobs2Response.
        :type job_count: int
        """
        self._job_count = job_count

    @property
    def job_list(self):
        """Gets the job_list of this ListJobs2Response.

        任务列表。

        :return: The job_list of this ListJobs2Response.
        :rtype: list[:class:`huaweicloudsdkges.v2.ListJobsRespJobList`]
        """
        return self._job_list

    @job_list.setter
    def job_list(self, job_list):
        """Sets the job_list of this ListJobs2Response.

        任务列表。

        :param job_list: The job_list of this ListJobs2Response.
        :type job_list: list[:class:`huaweicloudsdkges.v2.ListJobsRespJobList`]
        """
        self._job_list = job_list

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
        if not isinstance(other, ListJobs2Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
