from .base import JiraApiCall
from issue import Issue


class GetIssueApiCall(JiraApiCall):

  def __init__(self, key, callback):
    JiraApiCall.__init__(self, callback)
    self.issue_key = key

  def payload(self):
    self.result = Issue().get_issue(self.issue_key)


