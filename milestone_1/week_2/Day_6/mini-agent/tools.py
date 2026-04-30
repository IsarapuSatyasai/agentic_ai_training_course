# tools.py
import datetime
import math
import random

def get_current_time():
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression):
    """Evaluates a mathematical expression string. e.g., '50 * 2 + 10'"""
    try:
        # Using eval safely by limiting globals (Basic logic)
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"

def get_weather(city):
    """Simulates fetching weather data for a specific city."""
    # In a real scenario, you'd use a weather API here
    weathers = ["Sunny", "Cloudy", "Rainy", "Snowing", "Windy"]
    temp = random.randint(15, 35)
    return f"The weather in {city} is {random.choice(weathers)} with a temperature of {temp}°C."

def convert_currency(amount, from_currency, to_currency):
    """Simulates currency conversion. Args: amount, from_code, to_code."""
    # Mock rates
    rates = {"USD_to_EUR": 0.92, "USD_to_GBP": 0.79, "USD_to_INR": 83.0}
    key = f"{from_currency.upper()}_to_{to_currency.upper()}"
    
    if key in rates:
        converted = float(amount) * rates[key]
        return f"{amount} {from_currency} is approximately {converted:.2f} {to_currency}."
    else:
        return "Error: Exchange rate not available for this pair."

def generate_password(length=12):
    """Generates a random secure password string."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    password = "".join(random.choice(chars) for _ in range(int(length)))
    return f"Generated Password: {password}"

# Update this dictionary so the Agent can see the new tools.
available_tools = {
    "get_current_time": get_current_time,
    "calculator": calculator,
    "get_weather": get_weather,
    "convert_currency": convert_currency,
    "generate_password": generate_password
}