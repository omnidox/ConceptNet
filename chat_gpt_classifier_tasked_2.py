# import openai
# import configparser
# import time

# def get_gpt_context(object_name, desired_contexts=[], tasks=[]):

#     # Start timing for the first implementation
#     start_time_1 = time.time()


#     # Set up the API key
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

#    # If no specific contexts are provided, consider all available contexts
#     if not desired_contexts:
#         desired_contexts = ["kitchen", "office", "playroom", "living_room", "bedroom", 
#                             "dining_room", "pantry", "garden", "laundry_room"]

#     # Refine the prompt to guide the model towards a shorter answer
#     prompt = f"Which of the following contexts is the object '{object_name}' most likely associated with: {', '.join(desired_contexts)}? Please specify only the context as a response."



#     # Determine the system message based on tasks
#     if tasks:
#         task_str = " and ".join(tasks)
#         messages = [
#             {"role": "system", "content": f"You are a helpful {task_str} assistant robot."},
#             {"role": "user", "content": prompt}
#         ]
#     else:
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant robot."},
#             {"role": "user", "content": prompt}
#         ]

#     for message in messages:
#         print(f"{message['role']}: {message['content']}")

#     # Use the chat interface
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         # temperature=0.6,  # Adjusts the randomness of the output
#         # top_p=0.9,  # Adjusts the nucleus sampling
#         messages=messages
#     )

#     # Extract the model's response
#     answer = response['choices'][0]['message']['content'].strip()

#     # Post-process the response to extract just the context
#     # This step can be refined further based on the model's typical responses
#     for context in desired_contexts:
#         if context in answer:
#             end_time_1 = time.time()

#             execution_time_1 = end_time_1 - start_time_1
#             print(f"Execution time for the chatgpt implementation: {execution_time_1:.4f} seconds")

#             return context
        
#     end_time_1 = time.time()

#     execution_time_1 = end_time_1 - start_time_1
#     print(f"Execution time for the chatgpt implementation: {execution_time_1:.4f} seconds")

#     return answer  # Return the raw answer if no context is found

# # Test

# def get_chat_gpt_context(object_name, desired_contexts=None, focus_contexts=None):
#     # If desired_contexts or focus_contexts are not provided, set default values
#     if desired_contexts is None:
#         desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
#                             "dining_room", "pantry", "garden", "laundry_room"]

#     if focus_contexts is None:
#         focus_contexts = []

#     # Assuming get_gpt_context is a function that takes object_name, desired_contexts, and tasks (focus_contexts)
#     # and returns the most relevant context
#     context = get_gpt_context(object_name, desired_contexts=desired_contexts, tasks=focus_contexts)
#     print(f"The most relevant context for {object_name} is {context}.")
#     return context

# # Example usage
# # get_chat_gpt_context("apple", ["kitchen", "garden"], ["kitchen"])




import openai
import configparser
import time
import threading


def api_call_thread(object_name, desired_contexts, tasks, response_container):
    # Create the prompt
    prompt = f"Which of the following contexts is the object '{object_name}' most likely associated with: {', '.join(desired_contexts)}? Please specify only the context as a response."

    # Create the system message
    if tasks:
        task_str = " and ".join(tasks)
        messages = [{"role": "system", "content": f"You are a helpful {task_str} assistant robot."},
                    {"role": "user", "content": prompt}]
    else:
        messages = [{"role": "system", "content": "You are a helpful assistant robot."},
                    {"role": "user", "content": prompt}]

    for message in messages:
        print(f"{message['role']}: {message['content']}")

    # Use the chat interface
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    # Store the response in the provided container
    response_container['response'] = response


def get_gpt_context(object_name, desired_contexts=[], tasks=[]):
    start_time_1 = time.time()

    # Set up the API key
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

    # If no specific contexts are provided, consider all available contexts
    if not desired_contexts:
        desired_contexts = ["kitchen", "office", "playroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room"]

    # Refine the prompt
    prompt = f"Which of the following contexts is the object '{object_name}' most likely associated with: {', '.join(desired_contexts)}? Please specify only the context as a response."

    max_retries = 3
    retries = 0

    while retries < max_retries:
        response_container = {}

        # API call thread
        api_thread = threading.Thread(target=api_call_thread, args=(object_name, desired_contexts, tasks, response_container))
        api_thread.start()
        api_thread.join(timeout=10)  # Timeout in seconds

        if 'response' in response_container:
            # Extract response
            answer = response_container['response']['choices'][0]['message']['content'].strip()
            for context in desired_contexts:
                if context in answer:
                    end_time_1 = time.time()
                    execution_time_1 = end_time_1 - start_time_1
                    print(f"Execution time: {execution_time_1:.4f} seconds")
                    return context
            end_time_1 = time.time()
            execution_time_1 = end_time_1 - start_time_1
            print(f"Execution time: {execution_time_1:.4f} seconds")
            return answer
        else:
            print(f"API call timed out, retrying ({retries + 1}/{max_retries})")
            retries += 1

    print("API call failed after maximum retries")
    return "API Call Failed"

def get_chat_gpt_context(object_name, desired_contexts=None, focus_contexts=None):
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "playroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room"]
    if focus_contexts is None:
        focus_contexts = []

    context = get_gpt_context(object_name, desired_contexts=desired_contexts, tasks=focus_contexts)
    print(f"Most relevant context for {object_name}: {context}")
    return context

# Example usage
# get_chat_gpt_context("apple", ["kitchen", "garden"], ["kitchen"])