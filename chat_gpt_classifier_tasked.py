import openai
import configparser

def get_gpt_context(object_name, desired_contexts=[], tasks=[]):
    # Set up the API key
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

   # If no specific contexts are provided, consider all available contexts
    if not desired_contexts:
        desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room"]

    # Refine the prompt to guide the model towards a shorter answer
    prompt = f"Which of the following contexts is the object '{object_name}' most likely associated with: {', '.join(desired_contexts)}? Please specify only the context as a response."



    # Determine the system message based on tasks
    if tasks:
        task_str = " and ".join(tasks)
        messages = [
            {"role": "system", "content": f"You are a helpful {task_str} assistant robot."},
            {"role": "user", "content": prompt}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are a helpful assistant robot."},
            {"role": "user", "content": prompt}
        ]

    for message in messages:
        print(f"{message['role']}: {message['content']}")

    # Use the chat interface
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.6,  # Adjusts the randomness of the output
        top_p=0.9,  # Adjusts the nucleus sampling
        messages=messages
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
object_name = "potato"


desired_contexts = [
    "kitchen", "garden"
    ]
tasks= [
    "gardening"
    ]

context = get_gpt_context(object_name, desired_contexts = desired_contexts,tasks=tasks )
print(f"The most relevant context for {object_name} is {context}.")
