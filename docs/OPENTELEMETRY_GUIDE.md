# The Beginner's Guide to OpenTelemetry & Jaeger in Synora Studio

If you're new to observability, terms like "OpenTelemetry", "Spans", and "Distributed Tracing" can sound extremely intimidating. This guide is written specifically for beginners to explain exactly what is going on, why it's useful, and how you can actually look at your data using a beautiful visual dashboard called **Jaeger**.

---

## 1. What is OpenTelemetry?

Imagine you are shipping a package. You want to know exactly when it leaves the warehouse, when it arrives at the sorting facility, and when it is delivered to the customer.

In Synora Studio, when a user types a message in the **SaaS Web Portal** and hits send, that "package" (the HTTP request) has a long journey:

1. It enters the SaaS Portal.
2. The SaaS Portal forwards it over the network to the **API Server**.
3. The API Server queries the database.
4. The API Server talks to OpenAI (or a local LLM).
5. The response travels all the way back.

**OpenTelemetry (OTel)** is the tracking system for this package. It records timestamps at every single stop.

### Key Vocabulary:

* **Trace:** The entire journey of the package from start to finish.
* **Span:** A single stop along the journey. (e.g., The time spent specifically inside the API server is one "Span". The time spent talking to OpenAI is another "Span").
* **Context Propagation:** The way the "tracking number" is passed along. When the SaaS portal talks to the API server, it hands over the tracking number so the API Server can attach its own spans to the same Trace.

---

## 2. What is Jaeger?

Right now, OpenTelemetry is configured to print these tracking logs directly to your console (the black terminal window). This is great for debugging, but impossible to read for humans.

**Jaeger** is a free, open-source user interface that takes all those messy console logs and turns them into beautiful, colorful, easy-to-read waterfall graphs. It allows you to visually see exactly which part of your code is making the application slow.

---

## 3. Step-by-Step: Setting Up Jaeger

To see the UI, you need to run the Jaeger server on your machine. The easiest way is using Docker.

### Step 1: Install Docker

If you don't have Docker, download and install **Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop).

### Step 2: Run Jaeger

Open your terminal (Command Prompt or PowerShell) and run this exact command:

```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

*Wait a few seconds for it to download and start.*

### Step 3: Open the Jaeger Dashboard

Open your web browser and navigate to:
**[http://localhost:16686](http://localhost:16686)**

You are now looking at the Jaeger UI! But wait—it's empty. That's because Synora Studio is still printing traces to the console instead of sending them to Jaeger. Let's fix that.

---

## 4. Connecting Synora Studio to Jaeger

To tell Synora Studio to send data to Jaeger over the network, we need to install an "Exporter" and update two files.

### Step 1: Install the Exporter Library

In your terminal, inside the Synora Studio folder, run:

```bash
pip install opentelemetry-exporter-otlp
```

*(This library handles sending the data over the network via gRPC).*

### Step 2: Update the API Server

Open the file: `synora_server/logic/telemetry/telemetry_manager.py`

**Change the import line at the top:**

```python
# Change this:
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# To this:
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
```

**Change the processor logic (around line 59):**

```python
# Change this:
processor = BatchSpanProcessor(ConsoleSpanExporter())

# To this:
processor = BatchSpanProcessor(OTLPSpanExporter())
```

### Step 3: Update the SaaS Web Portal

Open the file: `synora_saas/core/app.py`

Do the exact same thing as above. Update the imports to include `OTLPSpanExporter` and change `BatchSpanProcessor(ConsoleSpanExporter())` to `BatchSpanProcessor(OTLPSpanExporter())`.

---

## 5. View Your Data!

1. Restart your API Server (`python server.py`).
2. Restart your SaaS Portal (`python web.py`).
3. Open the SaaS Portal in your browser and click around, send a message, or log in.
   *Note: We have "Sampling" set to 5%. This means you might need to click around 20 times before a trace is randomly selected and generated!*
4. Go back to your Jaeger Dashboard (`http://localhost:16686`).
5. Under "Service", select `synora_saas` or `synora_server` and click **Find Traces**.

You will now see beautiful waterfall graphs showing exactly how many milliseconds it took to travel between your frontend and your backend!
