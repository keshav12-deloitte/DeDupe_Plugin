def get_prompt_guidance(code_input1, code_input2):
    template = """{{#system~}}You are an expert software developer. You need to compare two methods and tell whether the methods are similar or not. 
Instructions
---------------------
1 - If the methods take different parameters, they are not similar. This includes both the number and type of parameters.
2 - If the methods perform different tasks, they are not similar. This can be determined by looking at the code within the methods.
3 - If the methods return different types of values, they are not similar.
4 - If the methods handle errors differently, they are not similar.
5 - If the methods rely on different external variables or methods, they are not similar.
6 - If one method interacts with the web driver or web elements in a way that the other does not, they are not similar. This could include differences in how they locate elements, how they interact with elements, or how they navigate the web page. Methods are not similar.
7 - If one method uses certain Selenium methods (like find_element_by_id, click, send_keys, etc.) that the other does not, they are not similar.
8 - If the methods interact with different web elements, they are not similar.
9 - If one method uses assertions (for example, to check that a certain condition is true) and the other does not, they are not similar.
10 - If one method uses global variables and the other does not, they are not similar. 
11 - If one method uses decorators and the other does not, they are not similar. 
12 - If one method uses generators and the other does not, they are not similar. 
13 - If one method uses certain locators (like ID, class name, CSS selector, XPath, etc.) that the other does not, they are not similar.
14 - If the methods interact with different web elements (like buttons, text boxes, drop-down menus, etc.), they are not similar.
15 - If one method uses certain Selenium commands (like get, navigate, switch_to, etc.) that the other does not, they are not similar.
{{~/system}}
        {{#user~}}
        Compare two methods built for Selenium actions and determine if they are similar or not. If the methods are similar,  {"Response": "Yes", "Reason":"Write the reason for your answer"}. If they are not similar, {"Response": "No"}.
        The code of two methods for compare:
        method1={{code_input1}}
        method2={{code_input2}}
        {{~/user}}
        {{#assistant~}}
        {{gen 'evaluation_text'}}
        {{~/assistant}}"""
    return template
