from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.prompts import MessagesPlaceholder
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

# Load the OpenAI API key
load_dotenv()

# Create an instance of ChatOpenAI with specific parameters
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Initialize an empty list to keep track of the chat history
chat_history = []

# Create a CSV agent using create_csv_agent
csv_agent = create_csv_agent(
    llm,
    "osu_clubs_data.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# Define a key to reference chat history in the prompt
MEMORY_KEY = "chat_history"

# Define the prompt for the chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            ("As an AI assistant dedicated to supporting Oregon State University students, "
             "your primary function is to guide students in discovering clubs and organizations "
             "that align with their interests and needs. You have access to a comprehensive dataframe "
             "containing detailed information about various clubs and organizations available at the "
             "university. Tailor your responses based on the specific queries or interests expressed "
             "by the students. Offer concise, relevant information that directly addresses their questions. When "
             "you mention any clubs or organizations in your response, it is imperative that you include the names of "
             "all relevant entities without omission. Never ever mention the underlying dataframe, or imply its "
             "existence in your responses. Keep the conversation natural and focused on the "
             "students' requests, as if you are drawing from a vast knowledge of university activities without "
             "referring to a specific data source. After providing information, always encourage further interaction "
             "by asking if the student would like more details about the topic discussed, or if they have any other "
             "questions. "),
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Define another agent to transform the response from the csv_agent
club_info_agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    # | llm_with_tools
    | llm
    | OpenAIToolsAgentOutputParser()
)

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page, rendering the main page template from the templates folder
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for handling POST requests to '/ask', which processes user queries and returns AI responses
@app.route('/ask', methods=['POST'])
def ask():
    # Get the user input from the request
    user_input = request.form['user_input']

    # Invoke the csv_agent with the user input and store the response
    csv_agent_response = csv_agent.invoke(user_input)

    # Create and invoke an AgentExecutor to get the chat response from the csv_agent based on the user's input
    agent_executor = AgentExecutor(agent=club_info_agent, tools=[], verbose=True)
    chat_response = agent_executor.invoke({"input": csv_agent_response, "chat_history": chat_history})

    # Update the chat history
    chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=chat_response["output"]),
        ]
    )

    # Extract the agent_executor's response
    ai_message_content = chat_response['output']

    # Return that message as a JSON response
    return jsonify({'response': ai_message_content})


if __name__ == '__main__':
    app.run(debug=True)
