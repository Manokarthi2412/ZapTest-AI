import os
import openai
import constant

client = openai.OpenAI(
    api_key=constant.api_key,
    base_url="https://api.sambanova.ai/v1",
)


def docAgent(content):
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
        messages=[{"role":"system",
                "content":"""You are a Documentation writer for APIs.
                    Generate API documentation for the following endpoint \\
                    
                    Do not include JSON body field and error response.

                    Action : Delete Book

                    Endpoint: /books/<book_id>

                    Method: DELETE

                    Description: Deletes a book by its unique ID.

                    Path Parameter:
                    book_id (string, required): Unique identifier for the book.

                    Example Request

                    ““DELETE /books/e7d4f90c-8a74-4e7b-b529-5a7a708070e3””

                    Example Response
                    {
                    "message": "Book deleted successfully"}
                    """
                },
                {"role":"user","content":content}],
        temperature =  0.1,
        top_p = 0.1
    )
    return response.choices[0].message.content

