import requests
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
import os
from dotenv import load_dotenv
from datetime import datetime,timezone,timedelta

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('WEATHER_API_KEY')

def oper():
    # Destroy old labels
    for widget in f.winfo_children():
        widget.destroy()

    try:
        # Fetch weather data
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={e1.get()}&appid={api_key}')
        response.raise_for_status()
        data = response.json()

        # Extract relevant information
        temperature = str(data["main"]["temp"])
        feels_like = str(data["main"]["feels_like"])
        humidity = str(data["main"]["humidity"])
        weather_description = data["weather"][0]['description'].capitalize()
        

         # Convert to local time using timezone-aware objects
        timezone_offset = data["timezone"]
        utc_time = datetime.fromtimestamp(data["dt"], timezone.utc)
        local_time = utc_time + timedelta(seconds=timezone_offset)
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')


        # Update UI with weather data
        tk.Label(f, text=weather_description, font="Helvetica 20 bold", bg="#2E3B4E", fg="white").pack(pady=10)
        tk.Label(f, text=f"Temperature: {temperature}°C", font="Helvetica 24 bold", bg="#2E3B4E", fg="white").pack(pady=10)
        tk.Label(f, text=f"Feels Like: {feels_like}°C", font="Helvetica 24 bold", bg="#2E3B4E", fg="white").pack(pady=10)
        tk.Label(f, text=f"Humidity: {humidity}%", font="Helvetica 24 bold", bg="#2E3B4E", fg="white").pack(pady=10)
        tk.Label(f, text=f"Time: {local_time_str}", font="Helvetica 24 bold", bg="#2E3B4E", fg="white").pack(pady=10)

    except requests.RequestException as e:
        tk.Label(f, text="Error: " + str(e), font="Helvetica 20 bold", bg="#2E3B4E", fg="white").pack(pady=5)

def capitalize_text(event):
    text = e1.get()
    e1.delete(0, tk.END)
    e1.insert(0, text.capitalize())

root = tk.Tk()
root.title("Weather App")
root.geometry("800x600")
root.config(bg="#2E3B4E")

# Header with padding at the top
tk.Label(root, text="Weather App", bg="#2E3B4E", fg="#F7F9F9", font="Helvetica 24 bold").pack(pady=(80, 20))

# Container for entry and button
container = tk.Frame(root, bg="#2E3B4E")
container.pack(pady=20)

# Location Entry - Center aligned within the container
tk.Label(container, text="Enter Location:", bg="#2E3B4E", fg="#F7F9F9", font="Helvetica 16").pack(pady=5)

e1 = tk.Entry(container, fg="#333", bg="#F7F9F9", font="Helvetica 16", width=20, justify='center')
e1.pack(pady=5)
e1.insert(0, "")  # Insert empty text to ensure the entry field is initially empty

# Bind the entry widget to capitalize text as the user types
e1.bind('<KeyRelease>', capitalize_text)

# Fetch Button - Center aligned within the container
fetch_button = tk.Button(container, text="Fetch Weather", command=oper, bg="#4CAF50", fg="white", font="Helvetica 16", relief="flat", padx=10, pady=5)
fetch_button.pack(pady=10)

# Frame for weather details
f = tk.Frame(root, bg="#2E3B4E")
f.pack(padx=20, pady=20, fill="both", expand=True)
root.maxsize()

root.mainloop()






