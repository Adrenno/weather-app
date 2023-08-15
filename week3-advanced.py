import tkinter as tk
from tkinter import messagebox
import datetime
import requests
from PIL import Image, ImageTk
import io
import urllib.request

def kelvin_to_celcius_fahrenheit(kelvin):
    celcius=kelvin-273.15
    fahrenheit=celcius*(9/5)+32
    return celcius, fahrenheit

def set_city_image(city):
    access_key="1ZnN9_ItI6ZztheIkNqLbeUdnqbROAKN6cJvXzFSZkE"
    base_URL=f'https://api.unsplash.com/photos/random?query={city}&client_id={access_key}'

    try:
        response=requests.get(base_URL)
        data=response.json()

        if 'urls' in data:
            image_url=data['urls']['regular']
            image_response=requests.get(image_url)

            if image_response.status_code==200:
                image_data=io.BytesIO(image_response.content)
                city_image=Image.open(image_data)
                resized_bg=city_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
                bg=ImageTk.PhotoImage(resized_bg)
                background_label.configure(image=bg)
                background_label.image=bg

    except requests.exceptions.RequestException:
        pass

def get_weather():
    city=city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city")
        return
    
    base_URL="http://api.openweathermap.org/data/2.5/weather?"
    API_KEY="7bf104e9ba149daaae634c0d24478502"
    url=base_URL+"appid="+API_KEY+"&q="+city

    try:
        response=requests.get(url).json()
    
        temp_kelvin=response['main']['temp']
        temp_celcius, temp_fahrenheit=kelvin_to_celcius_fahrenheit(temp_kelvin)

        feels_like_kelvin=response['main']['feels_like']
        feels_like_celcius, feels_like_fahrenheit=kelvin_to_celcius_fahrenheit(feels_like_kelvin)

        weather=response['weather'][0]['main']
        weather_description=response['weather'][0]['description']

        humidity=response['main']['humidity']

        sunrise_time=datetime.datetime.utcfromtimestamp(response['sys']['sunrise']+response['timezone'])
        sunset_time=datetime.datetime.utcfromtimestamp(response['sys']['sunset']+response['timezone'])

        wind_speed=response['wind']['speed']

        date_time=datetime.datetime.utcfromtimestamp(response['dt']+response['timezone'])

        try:
            rain=response['rain']['1h']
        except KeyError:
            rain=0

        #Get weather icon url
        icon_URL=f"http://openweathermap.org/img/w/{response['weather'][0]['icon']}.png"
        icon_response=urllib.request.urlopen(icon_URL)
        icon_data=icon_response.read()

        #Display weather icon
        icon_image=Image.open(io.BytesIO(icon_data))
        resized_icon=icon_image.resize((100, 100))
        weather_icon=ImageTk.PhotoImage(resized_icon)
        weather_icon_label.config(image=weather_icon)
        weather_icon_label.image=weather_icon
        #Show weather info widgets
        result_label.grid()
        weather_icon_label.grid()

        result_label.config(text=f"Current weather in {response['name']}\n"
                                 f"{date_time} local time\n"
                                 f"Temperature: {temp_celcius:.2f}°C / {temp_fahrenheit:.2f}°F\n"
                                 f"Feels like: {feels_like_celcius:.2f}°C / {feels_like_fahrenheit:.2f}°F\n"
                                 f"Weather: {weather}\n"
                                 f"Description: {weather_description}\n"
                                 f"Humidity: {humidity}%\n"
                                 f"Sunrise time: {sunrise_time} local time\n"
                                 f"Sunset time: {sunset_time} local time\n"
                                 f"Wind speed: {wind_speed} m/s\n"
                                 f"Rain rate per hour: {rain}"
                                 )
        
        set_city_image(city)

        result_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        weather_icon_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        get_forecast()

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Connection Error: Please check your internet connection.")
    except KeyError:
        messagebox.showerror("Error", "City not found. Please enter a valid city name.")


def get_forecast():
    city=city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city")
        return
    
    base_URL="http://api.openweathermap.org/data/2.5/forecast?"
    API_KEY="7bf104e9ba149daaae634c0d24478502"
    url=base_URL+"appid="+API_KEY+"&q="+city

    try:
        response=requests.get(url).json()

        forecast_label1.grid()
        forecast_label2.grid()
        forecast_label3.grid()
        forecast_label4.grid()

        weather_icon_label1.grid()
        weather_icon_label2.grid()
        weather_icon_label3.grid()
        weather_icon_label4.grid()

        forecast_labels=[forecast_label1, forecast_label2, forecast_label3, forecast_label4]
        weather_icon_labels=[weather_icon_label1, weather_icon_label2, weather_icon_label3, weather_icon_label4]

        for i in range(8, min(33, len(response['list'])), 8):
            temp_kelvin=response['list'][i]['main']['temp']
            temp_celcius, temp_fahrenheit=kelvin_to_celcius_fahrenheit(temp_kelvin)
            weather=response['list'][i]['weather'][0]['description']
            date_time=datetime.datetime.strptime(response['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S')
            forecast_labels[int((i-8)/8-1)].config(text=f"Temperature: {temp_celcius:.2f}°C / {temp_fahrenheit:.2f}°F\n"
                                                   f"Weather: {weather}\n"
                                                   f"{date_time}")
            
            icon_URL=f"http://openweathermap.org/img/w/{response['list'][i]['weather'][0]['icon']}.png"
            icon_response=urllib.request.urlopen(icon_URL)
            icon_data=icon_response.read()

            icon_image=Image.open(io.BytesIO(icon_data))
            resized_icon=icon_image.resize((70, 70))
            weather_icon=ImageTk.PhotoImage(resized_icon)
            weather_icon_labels[int((i-8)/8-1)].config(image=weather_icon)
            weather_icon_labels[int((i-8)/8-1)].image=weather_icon

        weather_icon_label4.grid(row=3, column=0, padx=10, pady=10)
        weather_icon_label1.grid(row=3, column=1, padx=10, pady=10)
        weather_icon_label2.grid(row=3, column=2, padx=10, pady=10)
        weather_icon_label3.grid(row=3, column=3, padx=10, pady=10)

        forecast_label4.grid(row=4, column=0, padx=10, pady=10)
        forecast_label1.grid(row=4, column=1, padx=10, pady=10)
        forecast_label2.grid(row=4, column=2, padx=10, pady=10)
        forecast_label3.grid(row=4, column=3, padx=10, pady=10)  
           

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Connection Error: Please check your internet connection.")
    except KeyError:
        messagebox.showerror("Error", "City not found. Please enter a valid city name.")


label_font=("Quicksand", 14)
bold_label_font=("Quicksand", 14, "bold")
label_text_color="#333"
label_bg_color="#f0f0f0"
result_label_bg_color="#f5f5f5"
button_bg_color="#4CAF50"
button_fg_color="white"
button_active_bg_color="#45a049"
entry_font=("Quicksand", 16)

#Main
root=tk.Tk()
root.title("Weather App")


background=Image.open("background.jpg")

#screen width and height
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

# Resize the background image to the new dimensions
background=background.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg=ImageTk.PhotoImage(background)

background_label=tk.Label(root, image=bg)
background_label.place(relx=0.5, rely=0.5, anchor="center") 

#Widgets
city_label=tk.Label(root, text="Enter a city: " )
city_entry=tk.Entry(root, font=entry_font)
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather )
result_label = tk.Label(root, text="", justify=tk.LEFT )
weather_icon_label=tk.Label(root)
result_label.grid_remove()
weather_icon_label.grid_remove()
forecast_label1=tk.Label(root, text="", justify=tk.LEFT )
forecast_label1.grid_remove()
forecast_label2=tk.Label(root, text="", justify=tk.LEFT )
forecast_label2.grid_remove()
forecast_label3=tk.Label(root, text="", justify=tk.LEFT )
forecast_label3.grid_remove()
forecast_label4=tk.Label(root, text="", justify=tk.LEFT )
forecast_label4.grid_remove()
weather_icon_label1=tk.Label(root)
weather_icon_label1.grid_remove()
weather_icon_label2=tk.Label(root)
weather_icon_label2.grid_remove()
weather_icon_label3=tk.Label(root)
weather_icon_label3.grid_remove()
weather_icon_label4=tk.Label(root)
weather_icon_label4.grid_remove()

#label colors
city_label.config(fg=label_text_color, bg=label_bg_color, font=bold_label_font, borderwidth=1, relief="solid", padx=10, pady=10)
result_label.config(fg=label_text_color, bg=result_label_bg_color, font=label_font, borderwidth=1, relief="solid", padx=10, pady=10)
get_weather_button.config(bg=button_bg_color, fg=button_fg_color, activebackground=button_active_bg_color, font=label_font)

forecast_labels = [forecast_label1, forecast_label2, forecast_label3, forecast_label4]
for label in forecast_labels:
    label.config(bg=label_bg_color, fg=label_text_color, font=label_font, borderwidth=1, relief="solid", padx=10, pady=10)

#Layout
city_label.grid(row=0, column=0, padx=20, pady=20)
city_entry.grid(row=0, column=1, padx=10, pady=20)
get_weather_button.grid(row=0, column=2, padx=20, pady=20)

#Forecast borders
forecast_label1.config(borderwidth=1, relief="solid")
forecast_label2.config(borderwidth=1, relief="solid")
forecast_label3.config(borderwidth=1, relief="solid")
forecast_label4.config(borderwidth=1, relief="solid")


root.mainloop()
