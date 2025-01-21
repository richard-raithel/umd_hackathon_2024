from openai import AzureOpenAI


# Azure OpenAI model and client configuration
model_name = "gpt-4o-2024-08-06"
client = AzureOpenAI(
    azure_endpoint="",
    api_key="",
    api_version="2024-02-01"
)

def openai_prompt_response(prompt):
    """
    Function to generate a response from the Azure OpenAI API.

    Parameters:
    - prompt (str): The input text prompt for the model.

    Returns:
    - response_text (str): The generated text from the Azure OpenAI API.
    """
    try:
        # Call the Azure OpenAI API for chat completions
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the generated text
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


def openai_sequence_response(prompt_list):
    """
    Function to generate a response from the Azure OpenAI API.

    Parameters:
    - prompt (str): The input text prompt for the model.

    Returns:
    - response_text (str): The generated text from the Azure OpenAI API.
    """
    try:
        # Call the Azure OpenAI API for chat completions
        response = client.chat.completions.create(
            model=model_name,
            messages=prompt_list
        )

        # Extract and return the generated text
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


# Example of a single prompt
example_prompt = "Hello, tell me about yourself"

# Example of a prompt list with multiple steps
example_prompt_list = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "system", "content": "You are searching through documents."}, # Example of adding an additional step
                {"role": "user", "content": example_prompt}
                # Add more system or user steps here if desired
            ]

# Execute the single prompt function
response_single = openai_prompt_response(example_prompt)
print("SINGLE PROMPT RESPONSE:")
print(response_single, '\n')

# Execute the sequence prompt function
response_sequence = openai_sequence_response(example_prompt_list)
print("SEQUENCE PROMPT RESPONSE:")
print(response_sequence)
