lalu = """
import pytest
from base.basePage import BasePage
from constants import document_constants as DC
from constants import project_constants as PC
from constants import task_invitation_constants as TC
from page.document_page import DocumentPage
from page.genericFunctions import GenericFunctions
from page.project_page import ProjectPage
from page.task_invitation_page import TaskAndInvitationPage
from utils.environment_variables import EMAIL_ID, PASSWORD, HOST_HA_NAME_1, HOST_HA_EMAIL, HOST_HA_PASSWORD, \
    HOST_HA_NAME_2, RECIPIENT_URL, RECIPIENT_ID


@pytest.mark.usefixtures("setup", "before_test", "launch_application")
class TestTaskAndInvitationCreation:

    @pytest.fixture(autouse=True)
    def class_objects(self):
        self.gf = GenericFunctions(self.driver)
        self.pp = ProjectPage(self.driver)
        self.dp = DocumentPage(self.driver)
        self.tp = TaskAndInvitationPage(self.driver)
        self.bp = BasePage(self.driver)

    @pytest.fixture()
    def login(self):
     
        self.gf.login(EMAIL_ID, PASSWORD)

    @pytest.fixture()
    def create_project(self, login):
        
        self.pp.create_project(PC.PRODUCT_CODE["PRODUCT_A"], PC.REVIEW_TYPE["PROJECT_ORBIS"],
                               PC.REGULATORY_EVENT_NAME["EVENT_1"])

    def test_view_task_list_in_task_inbox(self, create_project):
       
        self.dp.create_gsp_for_task(DC.DOCUMENT_DOMAIN["REGULATORY_ADMINISTRATIVE"],
                                    DC.DOCUMENT_TYPE["REGULATORY_DOCUMENT"],
                                    DC.DOCUMENT_SUBTYPE["GLOBAL_SUBMISSIONS"],
                                    doc_name="document1",
                                    doc_status=DC.DOCUMENT_STATUS.get("STATUS_1"))
        self.dp.verify_document_creation(DC.GSP_SUBTYPE["GLOBAL_SUBMISSIONS"])
        self.dp.send_files_to_recipients(HOST_HA_NAME_1,
                                         TC.OPTIONAL_MSG,
                                         DC.WORKFLOW_TYPES["SEND_GSP_PACKAGE"])
        self.dp.verify_task_creation()
        self.gf.logout()
        self.gf.login(HOST_HA_EMAIL, HOST_HA_PASSWORD)
        self.tp.navigation_through_side_bar(TC.XP_TASK_TAB)
        self.tp.view_task_status(TC.STATUS["STATUS1"])

"""

methods = """
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


code_snippet = """
def class_objects(self):
        self.gf = GenericFunctions(self.driver)
        self.pp = ProjectPage(self.driver)
        self.dp = DocumentPage(self.driver)
        self.tp = TaskAndInvitationPage(self.driver)
        self.bp = BasePage(self.driver)
"""
