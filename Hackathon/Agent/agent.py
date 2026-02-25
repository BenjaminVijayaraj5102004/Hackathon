import asyncio
import os
from dotenv import load_dotenv
from pydantic_ai import Agent 
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from scm_tool.tools.scm_tools import (
    init_store, 
    process_day, 
    skip_holiday, 
    get_status, 
    get_summary, 
    export_csv
)

load_dotenv()


model = GroqModel(
    "openai/gpt-oss-120b",
    provider=GroqProvider(api_key=os.getenv("GROQ_API_KEY"))
)



# Define the Agent
agent = Agent(
    model=model,
    name="SupplyChainAgent",
    system_prompt=(
        "You are an expert Supply Chain Manager. Your goal is to maintain stock levels,"  
        "Take user commands : product-name:, initial-stock: , reorder-point: , cost-price: , selling-price: , lead-time-days: , forecast-window: to initialize the store. Then daily demand to process days. You can also skip holidays, check status, and generate summaries."
        "maximize profit, and minimize lost sales. Always initialize the store first."
        "Use the provided tools to process daily demand, skip holidays, check status, and generate summaries."
        "Report : {get_summary} at the end of each day to track performance and make informed decisions and predict future demand trends. Always use the tools to perform actions and provide accurate responses based on the current state of the store." \
        "create a pdf form after quitting the agent."
    )
)

#tools
agent.tool_plain(init_store)
agent.tool_plain(process_day)
agent.tool_plain(skip_holiday)
agent.tool_plain(get_status)
agent.tool_plain(get_summary)
agent.tool_plain(export_csv)

async def main():
    print("Supply Chain Agent is ready. Type 'exit' to quit.")
    while True:
        # Get user input first
        user_input = input("Enter your command for the Supply Chain Agent: ")
        
        # Check for exit condition
        if user_input.lower() in ["exit", "q", "quit"]:
            print("Exiting the agent.")
            break
    
        # Run the agent INSIDE the loop so it processes every command
        # The agent will call init_store() if you ask it to initialize/start
        result = await agent.run(user_input)
        
        # Use result.data to see the tool output or final response
        print("\nAgent Response:")
        print(result.output)
        print("=" * 30)


if __name__ == "__main__":
    asyncio.run(main())