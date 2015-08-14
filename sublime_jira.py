# coding: utf-8
import sublime
import sublime_plugin

import issue
from conf import settings
from api_calls.get_issue import GetIssueApiCall
from api_calls.update_issue import UpdateIssueApiCall
from api_calls.create_issue import CreateIssueApiCall


class GetJiraIssueCommand(sublime_plugin.WindowCommand):

  def run(self, issue_key=None):
    if not issue_key:
      self.prompt()
    else:
      GetIssueApiCall(issue_key, callback=self.put_result).start()

  def put_result(self, text):
    self.window.new_file()
    view = self.window.active_view()
    view.run_command('replace_all', {'text': text})

  def prompt(self):
    view = self.window.active_view()

    # Try to retrieve selected text or text around cursor
    selection = view.sel()
    issue_text = view.substr(view.word(selection[0]))

    # default hint is project prefix
    project_prefix = '{}-'.format(settings().get('jira_default_project', ''))
    issue_key_hint = project_prefix

    # But if there is some text under selected or under the cursor
    if issue_text:

      # And it starts with project prefix
      if (issue_text.startswith(project_prefix)
          and issue_text[len(project_prefix):].isdigit()):
        issue_key_hint = issue_text

      # Or is a number
      elif issue_text.isdigit():
        issue_key_hint = project_prefix + issue_text

    callback = lambda v: self.window.run_command('get_jira_issue',
                                                 {'issue_key': v})
    self.window.show_input_panel('Issue key', issue_key_hint, callback, None, None)


class CreateJiraIssue(sublime_plugin.WindowCommand):

  def run(self, project=None, summary=None):
    if not project or not summary:
      self.prompt(project, summary)
    else:
      CreateIssueApiCall(project=project,
                         summary=summary,
                         callback=self.put_result).start()


  def prompt(self, project, summary):

    if not project:
      self.window.show_input_panel(
        'Project',
        settings().get('jira_default_project', ''),
        lambda project: self.run(project=project),
        None,
        None      )

    elif not summary:
      self.window.show_input_panel(
        'Summary',
        'no summary',
        lambda summary: self.run(project=project, summary=summary),
        None,
        None
      )

  def put_result(self, key):
    self.window.run_command('get_jira_issue', {'issue_key': key})


class UpdateJiraIssueCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('select_all')
    text = self.view.substr(self.view.sel()[0])
    UpdateIssueApiCall(text, callback=self.put_result).start()

  def put_result(self, result):
    if result:
      sublime.status_message('Issue updated: {}'.format(result))
    else:
      sublime.status_message('Issue NOT updated')

    self.view.sel().clear()


class ReplaceAllCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.run_command('select_all')
        self.view.replace(edit, self.view.sel()[0], text)
        self.view.sel().clear()
