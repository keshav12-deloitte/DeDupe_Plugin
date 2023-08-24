import ast
import datetime
import json
import math
import os
import pathlib
import re
from difflib import SequenceMatcher

import guidance.llms
import openai
import pandas as pd
import pytz
from openai.embeddings_utils import get_embedding, cosine_similarity

from SDET_AI_SUB.reusable_resources.prompt import get_prompt_guidance

"""
File contains all implementations of support method 
"""


class ParentNodeVisitor(ast.NodeVisitor):
    def __init__(self, node):
        self.node = node
        self.parent = None

    def visit(self, node):
        if any(isinstance(child, self.node) for child in ast.iter_child_nodes(node)):
            self.parent = node
        self.generic_visit(node)


def compare_methods(method1, method2):
    matcher = SequenceMatcher(None, method1, method2)
    similarity_ratio = matcher.ratio()
    return similarity_ratio


def get_parent(node, tree):
    visitor = ParentNodeVisitor(type(node))  # Pass the type of node
    visitor.visit(tree)
    return visitor.parent


def extract_function_names(code):
    pattern = r"\bdef\s+(\w+)\s*\("
    function_name = re.findall(pattern, code)
    return function_name


def search_each_existing_method_for_similar(
    search_query, file_path_csv, number_of_results=3
):
    df = pd.read_csv(file_path_csv)
    df.head()
    # convert embeddings from CSV str type back to list type
    df["code_embedding"] = df["Embedding"].apply(eval)
    embedding = get_embedding(search_query, engine="text-embedding-ada-002")
    df["similarities"] = df.code_embedding.apply(
        lambda x: cosine_similarity(x, embedding)
    )
    return df.sort_values("similarities", ascending=False).head(number_of_results)


def extract_methods_from_string(code_string):
    methods = []
    # Parse the code string into an AST
    tree = ast.parse(code_string)
    # Traverse the AST and extract function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)
    return methods


def checking_whether_code_is_similar_or_not(
    model_to_use, code_input_query, embedding_path, number_of_similarities=5
):
    global json_data_response1
    duplicate_count = 0
    method_return_string = ""
    query_header = """Check whether below method is similar or not. Similar method means they must have same functionality. If method is doing some different action or extra actions or extra steps then it is not similar. Response format must be, If yes {"Response": "Yes"}. If No, {"Response": "No"}"""
    a = search_each_existing_method_for_similar(
        search_query=code_input_query,
        file_path_csv=embedding_path,
        number_of_results=number_of_similarities,
    )
    for index, file_name in a["FileName"].items():
        chat_completion_query = ""
        similar_code_details = ""
        class_name = a["ClassName"][index]
        if isinstance(class_name, float):
            if math.isnan(class_name):
                class_name = "Class Name not present"
        method_code = a["MethodCode"][index]
        # Add the file name and class name if they exist
        if file_name:
            similar_code_details += f"-----------{file_name}-----------\n"
        if class_name:
            similar_code_details += f"-----------{class_name}-----------\n"
        chat_completion_query += f"{method_code}\n"
        score = compare_methods(code_input_query, method_code)
        if score < 1:
            template = get_prompt_guidance(code_input_query, chat_completion_query)
            guidance.llm = guidance.llms.OpenAI(model_to_use, temperature=0)
            program = guidance(template)
            executed_program = program(
                code_input1=code_input_query, code_input2=chat_completion_query
            )
            response = executed_program.get("evaluation_text")
            response_content = response
            # Find the JSON within the string
            start_index = response_content.find("{")
            end_index = response_content.rfind("}") + 1
            json_response_content = response_content[start_index:end_index]
            # Parse the JSON
            try:
                json_data_response = json.loads(json_response_content)
            except:
                json_response_content = "".join(
                    char
                    for char in json_response_content
                    if ord(char) > 31 or ord(char) == 9
                )

                # Parse the JSON string
                json_data_response = json.loads(json_response_content)
            if json_data_response.get("Response") == "No":
                print("")
            else:
                # similar_code_response_list.append(similar_code_details)
                response = openai.ChatCompletion.create(
                    model=model_to_use,
                    messages=[
                        {
                            "role": "user",
                            "content": query_header
                            + "code1 = \n"
                            + code_input_query
                            + "\n"
                            + "code2 ="
                            + chat_completion_query
                            + "\n answer = "
                            + response_content
                            + """\n Verify whether the answer is correct. Response format must be, If yes, {"Response": "Yes", "Reason" : "Explain the reason"}. If No, {"Response": "No", "Reason" : "Explain the reason"}""",
                        },
                    ],
                    max_tokens=444,
                    timeout=120,
                )

                response_content1 = response.choices[0].message["content"]
                print("Response 1", response_content1, "RESPONSE1OVER")
                start_index = response_content1.find("{")
                end_index = response_content1.rfind("}") + 1
                json_response_content1 = response_content1[start_index:end_index]
                # Parse the JSON
                try:
                    print("json 1", json_response_content1, "JSON1Over")
                    json_data_response1 = json.loads(json_response_content1)
                except:
                    json_data_response1 = json_data_response1.replace('"', "'")
                    json_data_response1 = json.loads(json_data_response1)
                if json_data_response1.get("Response") == "No":
                    print("")
                else:
                    duplicate_count = duplicate_count + 1
                    print(duplicate_count)
                    method_return_string += (
                        f"\nSimilar Code: {duplicate_count}\n"
                        + "------------------------------\n"
                        + "File Name = "
                        + file_name
                        + "\n"
                        + "Class Name ="
                        + class_name
                        + "\n"
                        + "Similar Code ="
                        + method_code
                        + "\n"
                    )

    return method_return_string


def extract_method_code_from_string(code_string, embedding_path):
    global duplicate_method_number
    print("Rajaji is here= ", datetime.datetime.now(pytz.timezone("Asia/Kolkata")))
    print(
        "-----------------------------------------------------------------------------------------------------------\n"
    )
    print(code_string)
    print(
        "-----------------------------------------------------------------------------------------------------------\n"
    )
    i = 0
    method_response_string = ""
    tree = ast.parse(code_string)
    method_codes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            method_code = ast.get_source_segment(code_string, node)
            method_codes.append(method_code)

    for method_code in method_codes:
        function_names = extract_function_names(method_code)

        print("Method Code : ", method_code)
        method_response_string += (
            f"\n Finding duplicate or similar methods for below method name.\n\n Method name =  "
            + str(function_names)
            + "\n"
        )
        a = checking_whether_code_is_similar_or_not(
            model_to_use="gpt-4",
            code_input_query=method_code,
            embedding_path=embedding_path,
            number_of_similarities=5,
        )
        print("A ", i, " =", a)
        # method_response_string += a
        print("Method Response String =", method_response_string)
        print("Rajaji is working on it.", i, "Done")
        i += 1
        if a:
            method_response_string = method_response_string + a
            print("===============Kesava===============")
            print(method_response_string)
            # duplicate_method_number = duplicate_method_number + 1

        else:
            method_response_string += "Similar not found"

    return method_response_string


def extract_methods_from_string_to_csv(code_string):
    data_list = []
    try:
        tree = ast.parse(code_string)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_name = node.name
                method_code = ast.get_source_segment(code_string, node)
                class_name = None
                parent = get_parent(node, tree)
                if isinstance(parent, ast.ClassDef):
                    class_name = parent.name
                embedded_code = get_embedding(
                    text=method_code, engine="text-embedding-ada-002"
                )
                data_list.append(
                    {
                        "ClassName": class_name,
                        "MethodName": method_name,
                        "MethodCode": method_code,
                        "Embedding": embedded_code,
                    }
                )
    except SyntaxError:
        print("Syntax error in code string")

    df = pd.DataFrame(data_list)
    embedded_csv_path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "\\files\\runtime_output\\"
        + class_name
        + "\\"
    )
    embedded_csv_file_name = class_name + ".csv"
    # print("File Path =", embedded_csv_path)
    if not os.path.exists(embedded_csv_path):
        print("lala")
        os.makedirs(embedded_csv_path)
        filepath = pathlib.Path(embedded_csv_path) / embedded_csv_file_name
        filepath.touch(exist_ok=True)
    df.to_csv(embedded_csv_path + embedded_csv_file_name, index=False)
    return embedded_csv_path + embedded_csv_file_name


def find_code_snippet_similar_in_csv(
    code_snippet, embedding_path, model_to_use, number_of_results=3
):
    global json_data_response1
    duplicate_count = 0
    method_return_string = ""
    query_header = """Check whether below method is similar or not. Similar method means they must have same 
    functionality. If method is doing some different action or extra actions or extra steps then it is not similar. 
    Response format must be, If yes {"Response": "Yes"}. If No, {"Response": "No"}"""
    a = search_each_existing_method_for_similar(
        search_query=code_snippet,
        file_path_csv=embedding_path,
        number_of_results=number_of_results,
    )
    for index, method_name in a["MethodCode"].items():
        chat_completion_query = ""
        similar_code_details = " "
        class_name = a["ClassName"][index]
        if isinstance(class_name, float):
            if math.isnan(class_name):
                class_name = "Class Name not present"
        method_code = a["MethodCode"][index]
        if class_name:
            similar_code_details += f"----------{class_name}----------\n"

        chat_completion_query += f"{method_code}\n"
        score = compare_methods(code_snippet, method_code)
        if score < 2:
            template = get_prompt_guidance(code_snippet, method_code)
            guidance.llm = guidance.llms.OpenAI(model_to_use, temperature=0)
            program = guidance(template)
            exe_template = program(code_input1=code_snippet, code_input2=method_code)
            response_content = exe_template.get("evaluation_text")
            start_index = response_content.find("{")
            end_index = response_content.rfind("}") + 1
            json_response_content = response_content[start_index:end_index]
            # print("----------------------Response------------------------")
            # print(response_content)
            print("----------------------Response------------------------")
            print(json_response_content)
            print("----------------------Response------------------------")

            try:
                json_data_response = json.loads(json_response_content)
            except:
                json_response_content = "".join(
                    char
                    for char in json_response_content
                    if ord(char) > 31 or ord(char) == 9
                )

                json_data_response = json.loads(json_response_content)
            if json_data_response.get("Response") == "Yes":
                response = openai.ChatCompletion.create(
                    model=model_to_use,
                    messages=[
                        {
                            "role": "user",
                            "content": query_header
                            + "code1 = \n"
                            + code_snippet
                            + "\n"
                            + "code2 ="
                            + chat_completion_query
                            + "\n answer = "
                            + response_content
                            + """\n Verify whether the answer is correct. Response format must be, If yes, {"Response": "Yes", "Reason" : "Explain the reason"}. If No, {"Response": "No", "Reason" : "Explain the reason"}""",
                        },
                    ],
                    max_tokens=444,
                    timeout=120,
                )
                response_content1 = response.choices[0].message["content"]
                start_index = response_content1.find("{")
                end_index = response_content1.rfind("}") + 1
                json_response_content1 = response_content1[start_index:end_index]
                try:
                    json_data_response1 = json.loads(json_response_content1)
                except:
                    json_data_response1 = json_data_response1.replace('"', "'")
                    json_data_response1 = json.loads(json_data_response1)
                if json_data_response1.get("Response") == "Yes":
                    duplicate_count = duplicate_count + 1
                    method_return_string += (
                        f"\nSimilar Code: {duplicate_count}\n"
                        + "------------------------------\n"
                        + "Class Name ="
                        + class_name
                        + "\n"
                        + "Similar Code ="
                        + method_code
                        + "\n"
                    )
    print("Rajaji")
    print("==========================================================================")
    print(method_return_string)
    print("==========================================================================")
    return method_return_string
