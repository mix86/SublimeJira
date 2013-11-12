from .base import JiraApiCall
from issue import Issue


class UpdateIssueApiCall(JiraApiCall):

  def __init__(self, text, callback):
    JiraApiCall.__init__(self, callback)
    self.text = text

  def payload(self):
    self.result = Issue().update(self.text)
