import re
import sublime

from conf import settings
from jira.client import JIRA

_jira = None

class Issue(object):
  TEMPLATE = (
    "Key: {key}\n"
    "Link: {server}/browse/{key}\n"
    "Summary: {fields.summary}\n"
    "Type: {fields.issuetype.name}\n"
    "Status: {fields.status.name}\n"
    "Priority: {fields.priority.name}\n"
    "Reporter: {fields.reporter.displayName}\n"
    "Assignee: {assignee}\n"
    "Created: {fields.created}\n"
    "Updated: {fields.updated}\n"
    "Labels: {labels}\n"
    "\n"
    "{fields.description}\n"
  )

  DEFAULT_ISSUE_TYPE = 'Story'

  def __init__(self):
    global _jira
    login, password, self.options = self.load_config()
    if _jira is None:
      self.jira = JIRA(self.options, basic_auth=(login, password))
      _jira = self.jira
    else:
      self.jira = _jira

  def load_config(self):
    return (
      settings().get('jira_login'),
      settings().get('jira_password'),
      {'server': settings().get('jira_server')}
    )

  def get_issue(self, key):
    issue = self.jira.issue(key)
    return self.TEMPLATE.format(key=key,
                                server=self.options['server'],
                                fields=issue.fields,
                                assignee=issue.fields.assignee.displayName if issue.fields.assignee else '',
                                labels=', '.join(issue.fields.labels))

  def parse_issue(self, text):
    return self.extract_key(text), {
      'summary': self.extract_summary(text),
      'issuetype': {'name': self.extract_type(text)},
      'priority': {'name': self.extract_priority(text)},
      'labels': self.extract_labels(text),
      'description': self.extract_description(text),
    }

  def extract_key(self, text):
    return re.search(r'KEY: ([A-Z0-9]+\-\d+)', text.upper()).groups()[0].strip()

  def extract_summary(self, text):
    return re.search(r'Summary: (.+)', text).groups()[0].strip()

  def extract_type(self, text):
    return re.search(r'Type: (.+)', text).groups()[0].strip()

  def extract_priority(self, text):
    return re.search(r'Priority: (.+)', text).groups()[0].strip()

  def extract_labels(self, text):
    labels = re.search(r'Labels: (.*)', text).groups()[0]
    return [l.strip() for l in labels.split(',') if l]

  def extract_description(self, text):
    return re.search(r'\n\n([^$]+)', text).groups()[0]

  def update(self, text):
    key, issue_dict = self.parse_issue(text)
    issue = self.jira.issue(key)
    issue.update(fields=issue_dict)
    return key

  def create(self, project, summary):
    issue_dict = {
      'project': {'key': project},
      'summary': summary,
      'issuetype': {'name': self.DEFAULT_ISSUE_TYPE},
    }
    new_issue = self.jira.create_issue(fields=issue_dict)

    return new_issue.key
