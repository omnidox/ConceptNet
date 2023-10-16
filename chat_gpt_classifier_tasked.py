import openai
import configparser
import time

def get_gpt_context(object_name, desired_contexts=[], tasks=[]):

    # Start timing for the first implementation
    start_time_1 = time.time()


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
            end_time_1 = time.time()

            execution_time_1 = end_time_1 - start_time_1
            print(f"Execution time for the chatgpt implementation: {execution_time_1:.4f} seconds")

            return context
        
    end_time_1 = time.time()

    execution_time_1 = end_time_1 - start_time_1
    print(f"Execution time for the chatgpt implementation: {execution_time_1:.4f} seconds")

    return answer  # Return the raw answer if no context is found

# Test
object_name = "potato"


desired_contexts = [
    "kitchen", "garden"
    ]


# Prompt the user for tasks
available_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                     "dining_room", "pantry", "garden", "laundry_room"]

prompt_message = ("Please input what contexts or multiple contexts separated by commas for the robot to focus on. "
                 f"These are the possible contexts: {', '.join(available_contexts)} "
                 "(or press Enter to continue without specifying tasks): ")

while True:
    user_input = input(prompt_message).strip()

    # Split the input by commas and strip whitespace
    tasks = [task.strip() for task in user_input.split(",")] if user_input else []

    # Check if all tasks are in available_contexts
    if all(task in available_contexts for task in tasks) or not tasks:
        if tasks:
            print(f"You have set the robot's focus on: {', '.join(tasks)}")
        else:
            print("There will be no focus.")
        break

    else:
        print("One or more of the contexts you entered are not valid. Please try again.")


context = get_gpt_context(object_name, desired_contexts = desired_contexts,tasks=tasks )
print(f"The most relevant context for {object_name} is {context}.")
