import re


def extract_function_names(code):
    pattern = r"\bdef\s+(\w+)\s*\("
    function_names = re.findall(pattern, code)
    return function_names


# Example code snippet
code_snippet = """
def my_function():
    # Function body here

def search_each_existing_method_for_similar(search_query, file_path_csv, number_of_results=3):
    df = pd.read_csv(
        file_path_csv)
    df.head()
    # convert embeddings from CSV str type back to list type
    df['code_embedding'] = df['Embedding'].apply(eval)
    embedding = get_embedding(search_query, engine='text-embedding-ada-002')
    df['similarities'] = df.code_embedding.apply(lambda x: cosine_similarity(x, embedding))
    return df.sort_values('similarities', ascending=False).head(number_of_results)


def compare_methods(method1, method2):
    matcher = SequenceMatcher(None, method1, method2)
    similarity_ratio = matcher.ratio()
    return similarity_ratio
    
def compare_methods(method1, method2):
    matcher = SequenceMatcher(None, method1, method2)
    similarity_ratio = matcher.ratio()
    return similarity_ratio

"""

function_names = extract_function_names(code_snippet)
print(function_names)  # Output: ['my_function', 'another_function']
