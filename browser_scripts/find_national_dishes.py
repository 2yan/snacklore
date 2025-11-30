#!/usr/bin/env python3
"""
Script to find national dishes of a country using Wikipedia via browser-use.
"""

import asyncio
import os
from browser_use import Agent

# Try to configure with OpenAI if available
llm = None
if os.getenv("OPENAI_API_KEY"):
    try:
        from browser_use.llm.openai.chat import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4")
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI LLM: {e}")
        llm = None


async def find_national_dishes(country: str) -> str:
    """
    Find the national dish(es) of a given country using Wikipedia.
    
    Args:
        country: Name of the country to search for
        
    Returns:
        String containing information about the national dish(es)
    """
    # Create an agent with instructions
    # Use OpenAI LLM if available, otherwise use default
    task = f"Find the national dish or dishes of {country} using Wikipedia. " \
           f"Navigate to Wikipedia and search for information about {country}'s national dish. " \
           f"Look for a page about national dishes or the country's cuisine. " \
           f"Extract the name(s) of the national dish(es) and provide a brief description if available. " \
           f"Be thorough and check multiple sources if needed to find accurate information."
    
    if llm:
        print(f"Using OpenAI LLM: {type(llm)}")
        agent = Agent(task=task, llm=llm)
    else:
        print("Warning: No OpenAI API key found, browser-use will use default LLM (requires BROWSER_USE_API_KEY)")
        # Try to create agent without LLM - this will fail if BROWSER_USE_API_KEY is not set
        agent = Agent(task=task)
    
    try:
        # Run the agent
        result = await agent.run()
        return result
    except Exception as e:
        return f"Error occurred while searching for national dishes: {str(e)}"


async def main():
    """Main function to run the script."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python find_national_dishes.py <country_name>")
        print("Example: python find_national_dishes.py Italy")
        sys.exit(1)
    
    country = " ".join(sys.argv[1:])
    print(f"Searching for national dishes of {country}...")
    
    result = await find_national_dishes(country)
    print("\n" + "="*80)
    print(f"National Dishes of {country}:")
    print("="*80)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

