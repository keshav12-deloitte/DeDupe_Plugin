import json
import math
import guidance
import openai as openai
from SDET_AI_SUB.delete import lalu, code_snippet
from SDET_AI_SUB.reusable_resources.prompt import get_prompt_guidance
from SDET_AI_SUB.reusable_resources.supporting_metthod import (
    search_each_existing_method_for_similar,
    compare_methods,
    extract_methods_from_string_to_csv,
    find_code_snippet_similar_in_csv,
)

"""
File should contains only final method
"""

openai.api_key = "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"
# embedding_location = "SDET_AI_SUB/Resources/embedding_for_single_file.csv"
embedding_location = (
    "SDET_AI_SUB/Resources/embedding_checker_python07Aug_Percentage007.csv"
)


def find_similar_code_in_two_strings(
    full_file_code, code_snippet, number_of_results, model_to_use
):
    # Commenting below line as we already have, need to work on idea to do preprocess for next time iteration.
    # Before creating new embedding everytime, we will compare if there is any new method, if yes then only csv will be updated
    # embedding_csv_path = extract_methods_from_string_to_csv(full_file_code)
    embedding_csv_path = "C:/Users/vuchander/PycharmProjects/SDET_AI/SDET_AI_SUB/files/runtime_output/TestTaskAndInvitationCreation/TestTaskAndInvitationCreation.csv"
    search_each_existing_method_for_similar(
        code_snippet, embedding_csv_path, number_of_results
    )
    return find_code_snippet_similar_in_csv(
        code_snippet, embedding_csv_path, model_to_use, number_of_results
    )


a = find_similar_code_in_two_strings(full_file_code=lalu, code_snippet=code_snippet, number_of_results=2, model_to_use='gpt-4')
print(a)