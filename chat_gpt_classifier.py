import openai
import configparser

def get_gpt_context(object_name, desired_contexts=None):
    # Set up the API key
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

   # If no specific contexts are provided, consider all available contexts
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room"]

    # Refine the prompt to guide the model towards a shorter answer
    prompt = f"Which context is the object '{object_name}' most likely associated with: {', '.join(desired_contexts)}? Please specify only the context."

    # Use the chat interface
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the model's response
    answer = response['choices'][0]['message']['content'].strip()

    # Post-process the response to extract just the context
    # This step can be refined further based on the model's typical responses
    for context in desired_contexts:
        if context in answer:
            return context
    return answer  # Return the raw answer if no context is found

# Test
object_name = "remote_control"
desired_contexts = ["office", "living_room", "bedroom"]
context = get_gpt_context(object_name)
print(f"The most relevant context for {object_name} is {context}.")
