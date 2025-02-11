from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv
from upsonic import Agent, Task, ObjectResponse
from upsonic.client.tools import BrowserUse

# Load environment variables
load_dotenv()

app = FastAPI(title="Route Weather Checker")

# Initialize the AI agent
weather_agent = Agent("Travel Weather Assistant", model="azure/gpt-4o", reflection=True)

# Define response format for weather analysis
class CityWeather(ObjectResponse):
    city: str
    temperature: str
    condition: str

class RouteWeather(ObjectResponse):
    weather_reports: list[CityWeather]

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Route Weather Checker</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex justify-center items-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-lg w-[40rem]">
            <h1 class="text-2xl font-bold text-center mb-4">🌦️ Route Weather Checker</h1>
            <input id="start_city" type="text" placeholder="Enter starting city" class="w-full p-2 border rounded mb-4">
            <input id="end_city" type="text" placeholder="Enter destination city" class="w-full p-2 border rounded mb-4">
            <button onclick="checkWeather()" class="bg-blue-500 text-white px-4 py-2 rounded w-full">Check Route Weather</button>
            <div id="result" class="mt-4 text-sm text-gray-800 bg-gray-50 p-4 rounded overflow-y-auto h-64"></div>
        </div>
        <script>
            async function checkWeather() {
                const start_city = document.getElementById("start_city").value;
                const end_city = document.getElementById("end_city").value;
                if (!start_city || !end_city) {
                    alert("Please enter both cities.");
                    return;
                }
                const response = await fetch(`http://127.0.0.1:8000/get_route_weather?start_city=${encodeURIComponent(start_city)}&end_city=${encodeURIComponent(end_city)}`);
                const data = await response.json();
                document.getElementById("result").innerText = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """

@app.get("/get_route_weather", response_class=JSONResponse)
async def get_route_weather(start_city: str = Query(...), end_city: str = Query(...)):
    """Fetch route cities and get their weather data."""
    try:
        # Task to get cities along the route
        route_task = Task(
            f"Find all cities between {start_city} and {end_city} along the best driving route.",
            tools=[BrowserUse],
            response_format=RouteWeather
        )
        weather_agent.do(route_task)
        route_cities = [start_city] + [city.city for city in route_task.response.weather_reports] + [end_city]

        weather_results = []
        for city in route_cities:
            weather_task = Task(
                f"Search 'Weather in {city}' on Google and extract temperature and conditions.",
                tools=[BrowserUse],
                response_format=CityWeather
            )
            weather_agent.do(weather_task)
            if weather_task.response:
                weather_results.append(weather_task.response)

        return {"weather_reports": weather_results}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
