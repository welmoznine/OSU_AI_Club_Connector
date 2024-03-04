# OSU_AI_Club_Connector

OSU Hackathon Club - Winter 2024 Submission


## Introduction

OSU AI Club Connector leverages OpenAI’s GPT-4, alongside a carefully curated collection of all clubs and organizations at Oregon State University, to seamlessly connect students with groups that align with their passions and interests. Through an intuitive interface that encourages students to explore their interests, OSU AI Club Connector offers personalized recommendations, making it effortless to uncover and join communities perfect for nurturing and exploring their emerging hobbies, even if they start without a clear direction.

## Getting Started
To run the project locally, follow these steps:
1. Get an OpenAI API Key at https://openai.com/blog/openai-api:
2. Clone the repo with GitHub CLI
`gh repo clone welmoznine/OSU_AI_Club_Connector`
   
4. Install the necessary packages:
   - To run the Flask app: `pip install python-dotenv langchain langchain-core langchain_experimental langchain_openai`
   - To run the OSU club data scraper:`pip install requests beautifulsoup4`

5. Run the Flass app with the following command:
`python3 app.py`


## Usage
Open the app and type anything into the input box
![OSU_AI_Club_Connector #1](https://github.com/welmoznine/OSU_AI_Club_Connector/blob/main/static/OSU_AI_Club_Connector.png)

Chat with the app and discover clubs and organizations at OSU that align with your hobbies and unique passions 
![OSU_AI_Club_Connector #2](https://github.com/welmoznine/OSU_AI_Club_Connector/blob/main/static/OSU_AI_Club_Connector2.png)

## Built With
- Flask for the web framework
- Python3 for the backend logic
- HTML/CSS for the frontend
- Bootstrap for styling and responsive design
- Heroku for deployment
- Python’s beautifulSoup4, requests, and re packages for web scraping and data gathering
- Python's csv package for handling CSV files and data storage
- LangChain and OpenAI's GPT-4 for AI-driven recommendations

## Acknowledgments
The following resources were extremely helpful in learning about LangChain:
- [Official LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Talk to your CSV & Excel with LangChain](https://www.youtube.com/watch?v=xQ3mZhw69bc)
- [LangChain Basics Tutorial #2 Tools and Chains](https://www.youtube.com/watch?v=hI2BY7yl_Ac&list=PL8motc6AQftk1Bs42EW45kwYbyJ4jOdiZ)
  
The UI for the project was inspired by the following video: 
- [Learn How to Build a Chatbot with Flask - Step-by-Step Tutorial with HTML, CSS, and JavaScript](https://www.youtube.com/watch?v=70H_7C0kMbI)
