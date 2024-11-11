from duckduckgo_search import DDGS
from swarm import Swarm, Agent
from datetime import datetime

import os
os.environ["OPENAI_API_KEY"] = "12312312312312312312312"

# Models OK
#model_to_use = "llama3.2"
model_to_use = "llama3.2:1b"

os.environ["OPENAI_MODEL_NAME"] = model_to_use
os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:11434/v1"

# export ENAI_MODEL_NAME = dolphin-mixtral:8x7b
# export OPENAI_BASE_URL = http://127.0.0.1:11434/V1
current_date = datetime.now().strftime("%Y-%m")

# Initialize Swarm client
client = Swarm()

# 1. Create Internet Search Tool

def get_news_articles(topic):
    print(f"Running DuckDuckGo news search for {topic}...")
    
    # DuckDuckGo search
    ddg_api = DDGS()
    results = ddg_api.text(f"{topic} {current_date}", max_results=5)
    if results:
        news_results = "\n\n".join([f"Title: {result['title']}\nURL: {result['href']}\nDescription: {result['body']}" for result in results])
        return news_results
    else:
        return f"Could not find news results for {topic}."
    
# 2. Create AI Agents

# News Agent to fetch news
news_agent = Agent(
    name="News Assistant",
    instructions="Search in internet",
    functions=[get_news_articles],
    model=model_to_use
)

# Editor Agent to edit news
editor_agent = Agent(
    name="Editor Assistant",
    instructions="Write an article.",
    model=model_to_use
)

# 3. Create workflow

def run_news_workflow(topic):
    print("Running news Agent workflow...")
    
    # Step 1: Fetch news
    news_response = client.run(
        agent=news_agent,
        messages=[{"role": "user", "content": f"Get me infomration about {topic} on {current_date}"}],
    )
    
    raw_news = news_response.messages[-1]["content"]
    
    # Step 2: Pass news to editor for final review
    edited_news_response = client.run(
        agent=editor_agent,
        messages=[{"role": "user", "content": raw_news }],
    )
    
    return edited_news_response.messages[-1]["content"]

# Example of running the news workflow for a given topic
print(run_news_workflow("AI"))