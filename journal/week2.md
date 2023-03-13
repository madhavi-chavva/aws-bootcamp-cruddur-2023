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

![xray home activities](https://user-images.githubusercontent.com/125069098/223182301-c8662e8e-a737-4a3f-98a3-4421b397eff3.png)

![xray mock data](https://user-images.githubusercontent.com/125069098/223181479-4700d293-5051-40d4-bf7d-f1192ce02394.png)




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

### Check service data for last 10 minutes

```sh
EPOCH=$(date +%s)
aws xray get-service-graph --start-time $(($EPOCH-600)) --end-time $EPOCH
```

## CloudWatch Logs

Referred the link [python watchtower](https://pypi.org/project/watchtower/)
Add to the `requirements.txt`

```
watchtower
```

```sh
pip install -r requirements.txt
```


In `app.py`

```
import watchtower
import logging
from time import strftime
```

```py
# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("some message")
```

```py
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```
```py
@app.route("/api/activities/home", methods=['GET'])
def data_home():
  data = HomeActivities.run(Logger=LOGGER)
  return data, 200
```
Edit the home_activities.py

```py
class HomeActivities:
  def run(Logger):
    Logger.info("HomeActivities")
```

We'll log something in an API endpoint
```py
LOGGER.info('Hello Cloudwatch! from  /api/activities/home')
```

Set the env var in your backend-flask for `docker-compose.yml`

```yml
      AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

> passing AWS_REGION doesn't seems to get picked up by boto3 so pass default region instead

![cloudwatchlog](https://user-images.githubusercontent.com/125069098/222278787-34a31a0f-960a-452f-88b9-d57a21d90562.png)

![cloudwatch logs](https://user-images.githubusercontent.com/125069098/222221744-14185a3c-3769-43a5-87a5-196dbcfbcfad.png)

## Rollbar

https://rollbar.com/

Create a new project in Rollbar called `Cruddur`

Add to `requirements.txt`


```
blinker
rollbar
```

Install deps

```sh
pip install -r requirements.txt
```

We need to set our access token

```sh
export ROLLBAR_ACCESS_TOKEN=""
gp env ROLLBAR_ACCESS_TOKEN=""
```

Add to backend-flask for `docker-compose.yml`

```yml
ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
```

Import for Rollbar

```py
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
```

```py
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
```

We'll add an endpoint just for testing rollbar to `app.py`

```py
@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"
```


[Rollbar Flask Example](https://github.com/rollbar/rollbar-flask-example/blob/master/hello.py)

![rollbar](https://user-images.githubusercontent.com/125069098/222280298-db2b67f2-3282-4b14-ad95-6298a9c3929f.png)
![rollvar screenshot](https://user-images.githubusercontent.com/125069098/222280802-f7a83afa-79fd-41d7-af6d-eb14e54b2f07.png)
![rollbar screenshot2](https://user-images.githubusercontent.com/125069098/222281896-a471b1e1-2a9c-48d8-acc4-6c9ebf6b8ab8.png)
![rollbar typeerror](https://user-images.githubusercontent.com/125069098/222282076-b743daa7-8998-4975-8f40-f78a93703f2b.png)

## Xray subsegment of user_activities
Modify the code in the user_activities
```py
subsegment = xray_recorder.begin_subsegment('mock-data')
      # xray ---
      dict = {
        "now": now.isoformat(),
        "results-size": len(model['data'])
      }
      subsegment.put_metadata('key', dict, 'namespace')
      xray_recorder.end_subsegment()
    finally:  
    #  # Close the segment
      xray_recorder.end_subsegment()
 ```     
      
![image](https://user-images.githubusercontent.com/125069098/224727900-f9efdce5-c54b-40e1-9e62-c2c737f9da6b.png)










