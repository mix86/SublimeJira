from .base import JiraApiCall
from issue import Issue


class CreateIssueApiCall(JiraApiCall):

  def __init__(self, project, summary, callback):
    JiraApiCall.__init__(self, callback)
    self.project = project
    self.summary = summary

  def payload(self):
    self.result = Issue().create(self.project, self.summary)
