# Introduction to Microservices


```
TODO add quote
```

```
TODO add quote
```


## Table of Contents

1. Overview
2. Tools
3. Architecture
4. Back-End
5. Microservices
6. Templates
    - Model 1
    - Model 2
7. Testing
8. Final Thoughts
9. Exercise

## 1. Overview


In this part of the workshop, we're going to learn about how to get started creating microservices, for more traditional software development use cases and for machine learning microservices.

**What are microservices?**
Microservices are an architectural approach to building applications as a collection of small, modular, independently deployable services.

**What are machine learning microservices?**
Machine learning microservices apply this approach to ML systems by decomposing them into smaller services that each focus on a specific capability or model. Some examples of machine learning microservices:

- Model Training Service - Handles training ML models on new data.
- Model Serving Service - Deploys trained models and provides predictions/inferences.
- Data Processing Pipeline - Microservices for data ingestion, cleaning, preprocessing.
- Model Monitoring Service - Tracks model performance and drift.
- Experiment Tracking Service - Logs model experiments and results.
- The benefits of using microservices for machine learning include:
- Independent scaling - Can allocate more resources to demanding services.
- Fault isolation - If one service fails, others are not affected.
- Flexible deployment - Can rapidly deploy updates to individual services.
- Polyglot support - Mix languages/frameworks within services.
- Organizational alignment - Teams can own discrete services.
- The main challenges are the added complexity of distributed systems and the need for coordination between services. Clear communication protocols and well-defined APIs are essential.

Looking at machine learning microservices for inference, monitoring, and explainability:

For inference, a model serving microservice deploys trained models and handles prediction requests. Like a short order cook, it receives orders and rapidly serves up predictions. Architectures like Kubernetes can scale this service to handle spikes in traffic.

Monitoring microservices track model performance over time. They're like fitness trackers for your ML models, logging metrics like accuracy, latency, and drift. This helps identify when models need retraining or updating.

Explainability microservices analyze model behavior and describe the reasons behind predictions. These are like interpreters, translating model internal state into human-understandable explanations. Say for credit approval, they could identify the main factors driving a given prediction.

Pulling this together into an ML application is like assembling a symphony. The components (inference, monitoring, explainability) each focus on their part, coordinating via well-defined interfaces. Get the orchestration right, and you end up with a harmonious ML system greater than the sum of its microservices.

Let me know if you need any clarification or have additional examples to discuss!

Overall, microservices enable faster iteration and more robust and resilient ML systems, but require more up-front design and infrastructure coordination.


## 2. Tools
   
   
For this section, we will be using the following tools.
- FastAPI: FastAPI is like having a team of skilled architects and builders for constructing a house quickly and efficiently. It provides clear blueprints (API endpoints) and customization options, ensuring rapid development of robust and personalized APIs.
- HTML
- Tailwind CSS: 
- Gradio: Certainly! Imagine you have a tasty sandwich that you want to share with others. However, everyone has different preferences and dietary restrictions. Gradio is like a versatile food truck that serves your sandwich in various ways to accommodate different tastes. It takes your delicious sandwich (your Python code) and provides a user-friendly interface for people to interact with it. Just like a food truck offers different condiments, bread options, and sides, Gradio allows you to customize your interface by adding input fields, sliders, buttons, and more. It makes it easy for others to consume your code and interact with it in a way that suits their needs.
- Pytest
- Jinja2
 
## 3. Architecture
   
Every application or system needs an architecture, and even thought these are not often built into a diagram, it is good practice to visualize how we want to system to function and/or look before we get to coding. Let's start there.

We will need:
- a back-end
- a front-end
- 2 machine learning applications
- tests
- A DataBase (optional for this tutorial)

## 4. The Backend

Here's an attempt to describe the front-end and back-end of a microservices application using analogies:

The front-end is like a traveler exploring a foreign city, navigating between sites and activities. It acts as the user interface, calling different services to assemble experiences. The React/Angular UI is the traveler's map, guiding them between locations. Redux/Flux stores are travel journals, recording visits to services. APIs are transit systems, with protocols like GraphQL as subway maps. User auth is visa security, granting access privileges.

The back-end is like a bustling marketplace, full of vendors running independent shops. Services are merchant stalls, focused on specific capabilities. Data pipelines act as supply chains, moving inventory between stalls. Monitoring services are the market inspector, checking goods and stall conditions. APIs are the signboards and directions that connect the marketplace. Scaling changes the number of vendor stalls. New capabilities are added by launching new pop-up shops.

To travel the market (use the app), the front-end explorer (UI) relies on the directions (APIs) to visit the right merchants (services). Back-end organization and protocols enable smooth exploration. Microservices create a thriving software bazaar!

Let's begin with an example server that has one kind of API. Everytime we call our API we'll get a joke back.

```py
# examples/jokes.py
from fastapi import FastAPI
import pyjokes

app = FastAPI()

@app.get("/joke")
def get_joke():
    joke = pyjokes.get_joke()
    return {"joke": joke}
```

To run it we can use plain python. If we were using this in a production environment, we would want to use uvicorn or gunicorn to control the way our app operates in an server from, say, AWS or GCP. So..

```sh
# use
python jokes.py

# or
uvicorn main:app --reload
```

Once our server is up and running, we can send a GET requests to it using the requests library as below.

```py
import requests

response = requests.get("http://localhost:8000/joke")
print(response.status, "\n", response.json())
```
```
<Response [200]>

"A programmer walks into a bar and orders 1.38 root beers. The bartender informs her it's a root beer float. She says 'Make it a double!'"
```

Please keep your expectations low and your dad jokes tolerance high with these examples. The `pyjokes` library can be a hit and miss with the quality of the jokes.🫣

### Exercise

Download a package a create a new API that, when called, returns something back. you can get as creative as you'd like to with the result. 😎


Now that we know a bit about how we can create APIs, let build our first application.

```py
# main.py
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    pass

@app.get("/service1")
async def read_page1(request: Request):
    pass

@app.get("/service2")
async def read_page2(request: Request):
    pass
```

Let's unpack our file above.

In the snippet above, we created an application with 3 components:
1. A home route
2. A page with some service
3. Another page with another service

These 3 pieces will come up as `your_kul_website.com`, `your_kul_website.com/service1`, and `your_kul_website.com/service2`.

Each of these services will have some sort of front-end template, and the functionality within each could be composed of multiple services as well (as we will see shortly).

As data professionals or machine learning engineers, chances are we might not have much experience with fron-end development work, bht that can't and shouldn't stop us from putting some makeup on our apps. to help us with this, we have Jinja2, which are templates that help structure and format the content in a Python web application.

Let's build a template for the home page of our application. This page should contain 2 buttons, one for each service, and a nice look and feel.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Building Machine Learning Microservices</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css" rel="stylesheet">
    <style>
        /* Add your custom styles here if needed */
    </style>
</head>

<body class="bg-gray-200 flex flex-col items-center justify-center h-screen">
    <div class="text-center">
        <h1 class="text-4xl font-bold mb-4">Building Machine Learning Microservices</h1>
        <p class="text-lg mb-8">Description of a generic machine learning application goes here.</p>
        <!-- Add your cool animation here -->
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
            Microservice 1
        </button>
        <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Microservice 2
        </button>
    </div>
</body>

</html>
```



```py
# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the 'templates' folder to serve HTML files
templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/service1")
async def read_page1(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request})

@app.get("/service2")
async def read_page2(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})
```