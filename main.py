import os
import urllib.request
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import json
import requests
from PIL import ImageTk, Image

BASE_URL = "http://api.weatherapi.com/v1/current.json?"
API_KEY = "<TOKEN>"


def show_data(city, country, temperature, wind_speed, humidity, pressure):
    country_label.configure(text=f"Country: {country}")
    temperature_label.configure(text=f"Temperature in {city}: {temperature}°")
    wind_speed_label.configure(text=f"Wind speed in {city}: {wind_speed}km/h")
    humidity_label.configure(text=f"Humidity in {city}: {humidity}φ")
    pressure_label.configure(text=f"Pressure in {city}: {pressure}Pa")


def get_weather(event):
    city = entry.get()
    url = BASE_URL+"key="+API_KEY+"&q="+city
    try:
        response = requests.get(url)
        if response.status_code == 200:
            root.grid_rowconfigure(0, weight=0)
            root.grid_columnconfigure(0, weight=0)
            all_data.configure(corner_radius=50)
            all_data.place(relx=0.5, rely=0.5, anchor="center")
            enter_city_label.grid(row=0, column=0, padx=50)
            entry.grid(row=1, column=0, padx=50)
            button.grid(row=2, column=0, padx=50)
            data_frame.grid(row=0, column=1, rowspan=3, pady=10)
            country_label.grid(row=0, column=0)
            temperature_label.grid(row=1, column=0)
            wind_speed_label.grid(row=2, column=0)
            humidity_label.grid(row=3, column=0)
            pressure_label.grid(row=4, column=0)
            data = json.loads(response.content)
            country = data['location']['country']
            data = data['current']
            show_data(city, country, data['temp_c'], data['gust_kph'], data['humidity'], data['pressure_mb'])
            url = "https:"+data['condition']['icon']
            filename = url.split('/')[-1]
            urllib.request.urlretrieve(url, filename)
            image = Image.open(filename)
            image = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(all_data, text="", image=image)
            image_label.grid(row=0, column=2, rowspan=3, padx=20)
            os.remove(filename)
        else:
            CTkMessagebox(title="Error", message="I can't find such a city", icon='cancel')
    except requests.exceptions.ConnectionError:
        CTkMessagebox(title="Error", message="Connection error", icon='cancel')


root = ctk.CTk()
window_height = 400
window_width = 850
root.geometry(f"{window_width}x{window_height}")
root.title("Weather")

# elements
all_data = ctk.CTkFrame(root, corner_radius=0)
enter_city_label = ctk.CTkLabel(all_data, text="Enter city:", font=('Consolas', 25))
entry = ctk.CTkEntry(all_data, width=200, height=30, font=('Consolas', 25), justify='center')
button = ctk.CTkButton(all_data, text="show temperature", command=get_weather, font=('Consolas', 20), width=200,
                       height=40)
data_frame = ctk.CTkFrame(all_data, width=500, height=200, corner_radius=20)
country_label = ctk.CTkLabel(data_frame, text="Country: ", font=('Consolas', 20))
temperature_label = ctk.CTkLabel(data_frame, text="Temperature: ", font=('Consolas', 20))
wind_speed_label = ctk.CTkLabel(data_frame, text="Wind speed: ", font=('Consolas', 20))
humidity_label = ctk.CTkLabel(data_frame, text="Humidity: ", font=('Consolas', 20))
pressure_label = ctk.CTkLabel(data_frame, text="Pressure: ", font=('Consolas', 20))
# grid
enter_city_label.place(relx=0.5, rely=0.4, anchor="center")
entry.place(relx=0.5, rely=0.5, anchor="center")
button.place(relx=0.5, rely=0.6, anchor="center")
all_data.grid(row=0, column=0, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.bind('<Return>', get_weather)

root.mainloop()
