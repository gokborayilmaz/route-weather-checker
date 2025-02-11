# 🚀 Everyday New Agent Series - Day 15/21: Route Weather Checker 🌦️🛣️

## 📌 Overview

**Route Weather Checker** is an AI-powered agent that helps travelers plan their journeys by checking the weather conditions in all cities along their travel route.

🔹 **BrowserUse** is used to search and extract weather data for each city.\
🔹 Users enter a starting city and a destination city, and the agent fetches real-time weather conditions along the route.

## 🛠 Features

✅ Fetches **all cities along the travel route**\
✅ Retrieves **real-time weather conditions** for each city\
✅ Provides **temperature & weather status** per city\
✅ Simple **UI to enter cities and view results**

## 📌 Installation

### Prerequisites

- Python 3.9+
- API key for OpenAI (Azure or OpenAI-supported models)

### Install dependencies

```sh
pip install -r requirements.txt
```

## 🚀 Running the Application

Start the FastAPI server:

```sh
uvicorn upsonicai:app --reload
```

Open the UI in your browser:

```
http://127.0.0.1:8000/
```

Enter your **starting and destination cities** and get a full breakdown of **weather conditions along the route**.

## 🖥️ API Endpoint

To get route weather data programmatically, use:

```
http://127.0.0.1:8000/get_route_weather?start_city=New York&end_city=Los Angeles
```

## 📦 Requirements

```
fastapi
uvicorn
dotenv
upsonic
```

