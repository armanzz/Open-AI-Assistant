import openai
import requests
from serpapi import GoogleSearch
import time
import wikipediaapi





# Set up your OpenAI API key
openai.api_key='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'

class wikipedia:
    @staticmethod
    def run():
        wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (armansingh1132@gmail.com)', 'en')

        page_py = wiki_wiki.page('Python_(programming_language)')
       
        print("Page - Exists: %s" % page_py.exists())
#Page - Exists: True
        
        print("Page - Title: %s" % page_py.title)
    # Page - Title: Python (programming language)

        print("Page - Summary: %s" % page_py.summary[0:60])


result1 = wikipedia.run()



    

class FileManagementTool:
    @staticmethod
    def write_file(filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(content))
        

    @staticmethod
    def read_file(filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                
                return content
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None

     
        
class SerpAPIWrapper:
    @staticmethod
    def run(query, api_key):
        serpapi_endpoint = 'https://serpapi.com/search.json?engine=google&q=currentevents'
        params = {
            'q': query,
            'key': api_key,
            # Add other parameters as needed based on the SerpApi documentation
        }

        try:
            search = GoogleSearch(params)
            json_response = search.get_dict()
            organic_results = json_response.get('organic_results', [])

            # Extract 'title' and 'link' for each result
            titles_and_links = [{'title': result.get('title', ''), 'link': result.get('link', '')} for result in organic_results]

            # Print or use the titles_and_links as needed
            print("Titles and Links:")
            file_tool.write_file("search_result_serpapi.txt", titles_and_links)
            

            

            return json_response

        except requests.exceptions.RequestException as e:
            print(f"Error interacting with SerpApi: {e}")
            return None

file_tool = FileManagementTool()
# add your serpapi key here
serp_api_key = '1508c9070eceea9e3b331a2a2c2b08fc010725ba62bdb10be57ce660791aa222'

# Perform a search using SerpAPI
search_result = SerpAPIWrapper.run("current events", serp_api_key)


# Read the file
content = file_tool.read_file("search_result_serpapi.txt")
print(content)
#print(content)


    #add your openai api key
# Initialize the client
client = openai.OpenAI(api_key='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')

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Big Tom",
    instructions="You are an assistant.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo"
)

# Step 2: Create a Thread
thread = client.beta.threads.create()

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="write a weather report for SF today"
)

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Arakoo."
)

print(run.model_dump_json(indent=4))

while True:
    # Wait for 5 seconds
    time.sleep(50)  

    # Retrieve the run status
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(run_status.model_dump_json(indent=4))

    # If run is completed, get messages
    if run_status.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Loop through messages and print content based on role
        for msg in messages.data:
            role = msg.role
            content = msg.content[0].text.value
            print(f"{role.capitalize()}: {content}")
            file_tool.write_file("auto_gpt_response.txt", content)

            #Read AutoGPT response from the file
            read_auto_gpt_response = file_tool.read_file("auto_gpt_response.txt")
            print(f"AutoGPT Response: {read_auto_gpt_response}")
            
    break