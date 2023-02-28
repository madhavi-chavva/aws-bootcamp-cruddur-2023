# Week 2 — Distributed Tracing

## HoneyComb
When creating a new dataset in the honeycomb it provides all the installation instructions.

Create a API key in the Honeycomb Account and integrate it with the gitpod.

```sh
export HONEYCOMB_API_KEY=""
export HONEYCOMB_SERVICE_NAME="Cruddur"
gp env HONEYCOMB_API_KEY=""
gp env HONEYCOMB_SERVICE_NAME="Cruddur"
```

Add the following Environment Vars to `backend-flask` in docker compose

```yml
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
```

Install the dependencies in the requirement.txt in the backend folder

```
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```

We'll install these dependencies: 

```sh
pip install -r requirements.txt
```
Add the following instructions in the app.py

```py
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
```

```py
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```
```py
# Initialize automatic instrumentation with Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```
Add the following code in the .gitpod.yml to open the ports automatically.
ports:
  - name: frontend
    port: 3000
    onOpen: open-browser
    visibility: public
  - name: backend
    port: 4567
    visibility: public
  - name: xray-daemon
    port: 2000
    visibility: public   

close the gitpod and open the workspace again then do the docker compose up
open the backend app
![docker view logs](https://user-images.githubusercontent.com/125069098/221917209-9b78bed2-66f7-4864-8f32-ccc9d6916d21.png)

![honeycomb trace](https://user-images.githubusercontent.com/125069098/221916823-61286733-574e-44f8-b76b-4ffaf24bcb83.png)

### Acquiring a Tracer 
To create spans, you need to get a Tracer.
When you create a Tracer, OpenTelemetry requires you to give it a name as a string. This string is the only required parameter.
When traces are sent to Honeycomb, the name of the Tracer is turned into the library.name field, which can be used to show all spans created from a particular tracer.

### Creating Spans 
Now we have a tracer configured, we can create spans to describe what is happening in your application.

Open the home_activities.py add the following instructions to trace the activities.

```py
from opentelemetry import trace

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run():
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      
      
      span.set_attribute("app.result_length", len(results))
```

The reference document [honeycomb opentelemetry](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/)

![honeycomb queryrun](https://user-images.githubusercontent.com/125069098/221920511-70adeaeb-6e2d-438b-9439-faef5bae8758.png)

## X-ray

Install the dependencies in the requirement.txt in the backend folder

```py
aws-xray-sdk
```

We'll install these dependencies in the backend-folder:

```sh
pip install -r requirements.txt
```
Add to `app.py`

```py
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)

app = Flask(__name__)

# x-ray ---------------
XRayMiddleware(app, xray_recorder)
```

### Setup AWS X-Ray Resources

Add `aws/json/xray.json`

```json
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "Cruddur",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```
### Create -group in the xray and sampling rule
```sh
FLASK_ADDRESS="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"$FLASK_ADDRESS\") {fault OR error}"
```
![awscli xray group](https://user-images.githubusercontent.com/125069098/221940969-c9bbdeae-a024-4438-b1d6-f544e7b4b722.png)

![xray group](https://user-images.githubusercontent.com/125069098/221940669-04d3fa33-7d68-45ed-9a7a-3fc538588e22.png)

```sh
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```
![awscli samplingrule](https://user-images.githubusercontent.com/125069098/221941292-0d8fa0a0-3b58-4ae0-8dcd-00c93e4f92a5.png)

![xray sampling-rule](https://user-images.githubusercontent.com/125069098/221940605-a326a57c-9310-47bd-b044-b103d4216798.png)

[Install X-ray Daemon](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html)

[Github aws-xray-daemon](https://github.com/aws/aws-xray-daemon)
[X-Ray Docker Compose example](https://github.com/marjamis/xray/blob/master/docker-compose.yml)


```sh
 wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.deb
 sudo dpkg -i **.deb
 ```

### Add Deamon Service to Docker Compose

```yml
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```
-b is for binding the port 0 is for ignore user data and metadata on an virtual machine

We need to add these two env vars to our backend-flask in our `docker-compose.yml` file

```yml
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```
![aws trace](https://user-images.githubusercontent.com/125069098/221948724-c5c124f5-9536-4e16-93a5-81f607aa8c58.png)






