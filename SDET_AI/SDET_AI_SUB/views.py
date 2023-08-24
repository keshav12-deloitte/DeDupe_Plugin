from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from SDET_AI_SUB.reusable_resources.support_method import (
    find_similar_code_in_two_strings,
)
from SDET_AI_SUB.reusable_resources.supporting_metthod import (
    extract_method_code_from_string,
)

"""
File contains only url implementation methods only
"""


@csrf_exempt
def deDupe_repo_checker(request):
    if request.method == "POST":
        code_string = request.POST.get("code_string")
        methods = extract_method_code_from_string(
            code_string,
            "SDET_AI_SUB/Resources/embedding_checker_python07Aug_Percentage007.csv",
        )
        response = HttpResponse(methods, content_type="text/plain")
        return response


@csrf_exempt
def deDupe_file_checker(request):
    if request.method == "POST":
        code_string1 = request.POST.get("code_string1")
        code_string2 = request.POST.get("code_string2")
        print("Rajaji")
        print(code_string1)
        print(
            "----------------------------------------------------------------------------------"
        )
        print(code_string2)
        print(
            "----------------------------------------------------------------------------------"
        )
        methods = find_similar_code_in_two_strings(
            code_string1, code_string2, number_of_results=5, model_to_use="gpt-4"
        )
        response = HttpResponse(methods, content_type="text/plain")
        return response
