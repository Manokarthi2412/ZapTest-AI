import openai
import constant

client = openai.OpenAI(
    api_key=constant.api_key,
    base_url="https://api.sambanova.ai/v1",
)


def testgenAgent(content):
    test_case_list = [
    {   
        "Test Case": "Valid Input",
        "URL": "/books",
        "Method": "POST",
        "Request Body (JSON)": '{"title": "Book1", "author": "Author1", "published_year": 2020, "genre": "Fiction"}',
        "Expected Response": "201 Created"
    }]

    full_prompt = """You are dataset generating Agent for testing the API which should contain all the edge cases maximum of 6 cases 
    with test case names
    .Do not generate any python code or any explanation
    Just give the dataset as a dict containing keys in double quotes in a list.Example response is given below"""+str(test_case_list[0])

    response = client.chat.completions.create(
    model='Meta-Llama-3.1-70B-Instruct',
    messages=[{"role":"system",
               "content":full_prompt },
               {"role":"user","content":content}],    
    temperature =  0.1,
    top_p = 0.1
)
    
    return response.choices[0].message.content