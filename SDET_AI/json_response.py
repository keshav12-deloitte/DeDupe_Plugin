import json

json_body = """
[
  {
    "method name": "['wait_until_element_is_clickable']",
    "Similar code": [
      {
        "File Name": "genericFunctions.py",
        "Class Name": "GenericFunctions",
        "Similar code": "def wait_until_element_is_clickable(self, element, seconds"
      },
      {
        "File Name": "basePage.py",
        "Class Name": "BasePage",
        "Similar code": "def wait_until_element_is_clickable(self, element, seconds"
      },
      {
        "File Name": "project_page.py",
        "Class Name": "ProjectPage",
        "Similar code": "def wait_until_element_is_clickable(self, element, seconds"
      },
      {
        "File Name": "document_page.py",
        "Class Name": "DocumentPage",
        "Similar code": "def wait_until_element_is_clickable(self, element, seconds"
      }
    ]
  },
  {
    "method name": "['edit_the_added_health_authority']",
    "Similar code": [
      {
        "File Name": "document_page.py",
        "Class Name": "DocumentPage",
        "Similar code": "def edit_the_added_health_authority(self, proposed_indication):"
      },
      {
        "File Name": "project_page.py",
        "Class Name": "ProjectPage",
        "Similar code": "def added_health_authority_customise(self, proposed_indication):"
      },
      {
        "File Name": "driver.py",
        "Class Name": "WebDriver",
        "Similar code": "def edit_the_added_health_authority(self, proposed_indication):"
      }
    ]
  },
  {
    "method name": "['verify_browser_is_not_auto_filling_login_credentials']",
    "Similar code": [
      {
        "File Name": "task_invitation_page.py",
        "Class Name": "TaskAndInvitationPage",
        "Similar code": "def verify_browser_is_not_auto_filling_login_credentials(self):"
      }
    ]
  },
  {
    "method name": "['verify_edit_draft_invitation_form']",
    "Similar code": [
      {
        "File Name": "task_invitation_page.py",
        "Class Name": "TaskAndInvitationPage",
        "Similar code": "def verify_edit_draft_invitation_form(self):"
      }
    ]
  }
]

"""
formatted_dta = json.loads(json_body)
print(formatted_dta[1]["Similar code"])
