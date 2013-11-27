SublimeJira
===========

SublimeJira lets you view update and create Jira tickets from the comfort of your favorite editor.

Features
---------
* Create, view and update issues using Sublime Text only
* Integraton with any Jira instance (version >= 5)

Installing
---------
**With the Package Control plugin:** The easiest way to install SublimeJira is through Package Control, which can be found at http://wbond.net/sublime_packages/package_control


Usage
---------

The plugin adds command palette three items:

* Get issue – prompt issue key and show it in a new tab
* Update issue – save changes
* Create issue – prompt project key, summary, create new issue and open show it in new tab

and some two-pass shortcuts:
* cmd + option + j, cmd + option + i – get **i**ssue
* cmd + option + j, cmd + option + u – **u**pdate issue
* cmd + option + j, cmd + option + n – create **n**ew issue

Configure
---------
Go to "Preferences => Package Settings => Sublime Jira => Settings – User"
and paste some like this:
```
{
  "jira_server": "https://yourdomain.atlassian.net",
  "jira_login": "username",
  "jira_password": "password",
  "jira_default_project": "YOURPROJECT"
}
```
