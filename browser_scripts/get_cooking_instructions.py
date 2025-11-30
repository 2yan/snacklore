#!/usr/bin/env python3
"""
Script to get detailed cooking instructions for a dish using online search via browser-use.
"""

import asyncio
import os
from browser_use import Agent


async def get_cooking_instructions(dish: str, country: str) -> str:
    """
    Get detailed cooking instructions for a dish from a specific country.
    
    Args:
        dish: Name of the dish
        country: Country of origin for the dish
        
    Returns:
        String containing detailed cooking instructions
    """
    # Create an agent with detailed instructions
    # The Agent will handle browser configuration automatically
    agent = Agent(
        task=f"Find detailed cooking instructions for {dish} from {country}. "
             f"Search online for a recipe for {dish} from {country}. "
             f"Look for reputable cooking websites, recipe sites, or food blogs. "
             f"Extract the complete recipe including: "
             f"1. List of ingredients with quantities "
             f"2. Step-by-step cooking instructions "
             f"3. Cooking time and temperature if available "
             f"4. Serving suggestions if available. "
             f"Provide all the information in a clear, organized format. "
             f"Make sure to get the full recipe with all details."
    )
    
    try:
        # Run the agent
        result = await agent.run()
        return result
    except Exception as e:
        return f"Error occurred while searching for cooking instructions: {str(e)}"


async def main():
    """Main function to run the script."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python get_cooking_instructions.py <dish_name> <country>")
        print("Example: python get_cooking_instructions.py 'Pasta Carbonara' Italy")
        sys.exit(1)
    
    dish = sys.argv[1]
    country = " ".join(sys.argv[2:])
    
    print(f"Searching for cooking instructions for {dish} from {country}...")
    
    result = await get_cooking_instructions(dish, country)
    print("\n" + "="*80)
    print(f"Cooking Instructions for {dish} from {country}:")
    print("="*80)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

