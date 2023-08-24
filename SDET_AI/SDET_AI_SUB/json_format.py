import re
import json


def convert_to_json(input_string):
    # Split the input string into separate blocks for each method
    method_blocks = input_string.split(
        "Finding duplicate or similar methods for below method name."
    )

    json_output = []

    # Process each block
    for block in method_blocks:
        if block.strip() == "":
            continue

        # Extract the method name
        method_name = re.search(r"Method name =  \['(.*?)'\]", block).group(1)

        # Split the block into separate parts for each similar code
        code_parts = block.split("Similar Code:")

        similar_codes = []

        # Process each part
        for part in code_parts[1:]:
            # Extract the file name, class name, and similar code
            file_name = re.search(r"File Name = (.*?)\n", part).group(1)
            class_name = re.search(r"Class Name =(.*?)\n", part).group(1)
            similar_code = (
                re.search(r"Similar Code =(.*?)\n\n", part, re.DOTALL).group(1).strip()
            )

            # Add the extracted information to the similar codes list
            similar_codes.append(
                {
                    "File Name": file_name,
                    "Class Name": class_name,
                    "Similar Code": similar_code,
                }
            )

        # Add the method name and similar codes to the JSON output
        json_output.append({"Method Name": method_name, "Similar Code": similar_codes})

    # Convert the JSON output to a string and return it
    return json.dumps(json_output, indent=4)


# Test the function
input_string = """
Finding duplicate or similar methods for below method name.

 Method name =  ['wait_until_element_is_clickable']

Similar Code: 1
------------------------------
File Name = genericFunctions.py
Class Name =GenericFunctions
Similar Code =def wait_until_element_is_clickable(self, element, seconds=WAIT_TIME):
        \"\"\"
        Function to wait until the given web element is clickable
        :param seconds:
        :param element:
        :return:
        \"\"\"
        wait = WebDriverWait(self.driver, seconds)
        wait.until(EC.element_to_be_clickable((By.XPATH, element)))

Similar Code: 2
------------------------------
File Name = basePage.py
Class Name =BasePage
Similar Code =def wait_until_element_is_clickable(self, element, seconds=WAIT_TIME):
        \"\"\"
        Function to wait until the given web element is clickable
        :param seconds:
        :param element:
        :return:
        \"\"\"
        wait = WebDriverWait(self.driver, seconds)
        wait.until(EC.element_to_be_clickable((By.XPATH, element)))

Similar Code: 3
------------------------------
File Name = document_page.py
Class Name =DocumentPage
Similar Code =def wait_until_element_is_clickable(self, element, seconds=WAIT_TIME):
        \"\"\"
        Function to wait until the given web element is clickable
        :param seconds:
        :param element:
        :return:
        \"\"\"
        wait = WebDriverWait(self.driver, seconds)
        wait.until(EC.element_to_be_clickable((By.XPATH, element)))

Similar Code: 4
------------------------------
File Name = project_page.py
Class Name =ProjectPage
Similar Code =def wait_until_element_is_clickable(self, element, seconds=WAIT_TIME):
        \"\"\"
        Function to wait until the given web element is clickable
        :param seconds:
        :param element:
        :return:
        \"\"\"
        wait = WebDriverWait(self.driver, seconds)
        wait.until(EC.element_to_be_clickable((By.XPATH, element)))

 Finding duplicate or similar methods for below method name.

 Method name =  ['edit_the_added_health_authority']

Similar Code: 1
------------------------------
File Name = document_page.py
Class Name =DocumentPage
Similar Code =def edit_the_added_health_authority(self, proposed_indication):
        \"\"\"
        This function edits the added health authority
        :param:proposed_indication
        :return:
        \"\"\"
        self.move_to_element(DC.XP_EDIT_HA_PROPOSED_TEXT, msg=\"HA proposed indication text\")
        time.sleep(2)
        self.click(DC.XP_EDIT_HA_ICON, msg=\"edit ha icon\")
        self.clear(DC.XP_EDIT_HA_PROPOSED_FILED)
        self.click_and_type(DC.XP_EDIT_HA_PROPOSED_FILED, proposed_indication, msg=\"ha edit field\")
        self.click(DC.XP_EDIT_HA_SAVE_BTN, msg=\"HA save button\")
        edited_text = self.get_text(DC.XP_EDIT_HA_PROPOSED_TEXT)
        self.gf.check_values(edited_text, \"Edited\")
        self.gf.verify_document_confirmation()

Similar Code: 2
------------------------------
File Name = project_page.py
Class Name =ProjectPage
Similar Code =def added_health_authority_customise(self, proposed_indication):
        \"\"\"
        This function edits the added health authority
        :param:proposed_indication
        :return:
        \"\"\"
        self.move_to_element(DC.XP_EDIT_HA_PROPOSED_TEXT, msg=\"HA proposed indication text\")
        time.sleep(2)
        self.click(DC.XP_EDIT_HA_ICON, msg=\"edit ha icon\")
        self.clear(DC.XP_EDIT_HA_PROPOSED_FILED)
        self.click_and_type(DC.XP_EDIT_HA_PROPOSED_FILED, proposed_indication, msg=\"ha edit field\")
        self.click(DC.XP_EDIT_HA_SAVE_BTN, msg=\"HA save button\")
        edited_text = self.get_text(DC.XP_EDIT_HA_PROPOSED_TEXT)
        self.gf.check_values(edited_text, \"Edited\")
        self.gf.verify_document_confirmation()

Similar Code: 3
------------------------------
File Name = driver.py
Class Name =WebDriver
Similar Code =def edit_the_added_health_authority(self, proposed_indication):
        self.move_to_element(DC.XP_EDIT_HA_PROPOSED_TEXT, msg=\"HA proposed indication text\")
        time.sleep(2)
        self.click(DC.XP_EDIT_HA_ICON, msg=\"edit ha icon\")
        self.clear(DC.XP_EDIT_HA_PROPOSED_FILED)
        self.click_and_type(DC.XP_EDIT_HA_PROPOSED_FILED, proposed_indication, msg=\"ha edit field\")
        self.click(DC.XP_EDIT_HA_SAVE_BTN, msg=\"HA save button\")
        edited_text = self.get_text(DC.XP_EDIT_HA_PROPOSED_TEXT)
        self.gf.check_values(edited_text, \"Edited\")
        self.gf.verify_document_confirmation()

 Finding duplicate or similar methods for below method name.

 Method name =  ['verify_browser_is_not_auto_filling_login_credentials']

Similar Code: 1
------------------------------
File Name = task_invitation_page.py
Class Name =TaskAndInvitationPage
Similar Code =def verify_browser_is_not_auto_filling_login_credentials(self):
        \"\"\"
        This function to verify edit invitation form
        :return:
        \"\"\"
        text_username = self.get_text(GC.XP_EMAIL)
        text_password = self.get_text(GC.XP_PASSWORD)
        self.gf.check_values(text_username, '')
        self.gf.check_values(text_password, '')

 Finding duplicate or similar methods for below method name.

 Method name =  ['verify_edit_draft_invitation_form']

Similar Code: 1
------------------------------
File Name = task_invitation_page.py
Class Name =TaskAndInvitationPage
Similar Code =def verify_edit_draft_invitation_form(self):
        \"\"\"
        This function to verify edit invitation form
        :return:
        \"\"\"
        self.dp.wait_until_element_is_clickable(TC.XP_CONTINUE_EDITING_BTN)
        self.dp.click(TC.XP_CONTINUE_EDITING_BTN, msg=\"Continue edit button\")
        self.dp.wait_until_element_is_clickable(TC.XP_OPTIONAL_MSG)
        self.dp.clear(TC.XP_OPTIONAL_MSG)
        self.dp.send_keys(TC.XP_OPTIONAL_MSG, \"Arjun\", msg=\"Optional message\")

"""
print(convert_to_json(input_string))
