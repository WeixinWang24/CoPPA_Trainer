# CoPPA Trainer

## Description
The "Trainer" part of the CoPPA project requests data for training and prediction from the "Connector". With help of a random forest classifier and a XGBoost classifier, it is able to predict the most probable next flow nodes, the duration and the risk for an occuring incident and provides the corresponding probabilities. It exports these results via a FastAPI endpoint, which is accessed by the "Predictor". 

## Installation
## Installation on Windows
### Run in Docker Container
- install docker engine (e.g. https://www.docker.com/products/docker-desktop/)
- create a file called **"docker-compose.yml"** with the following content
```yaml
version: '3.4'

services:
  coppaconnector:
    image: gitlab.uni-koblenz.de:4567/process-science/internship/coppa-sose-23/coppa-connector:latest
    container_name: coppaconnector
    restart: unless-stopped    
    depends_on:
      - db
    environment:
    #Set Camunda -> IP, PORT, USERNAME and PASSWORD
      - IP=141.26.157.132
      - PORT=8081
      - USERNAME=demo
      - PASSWORD=demo
    ports:
    - 8080:8080
  db:
    image: postgres
    restart: unless-stopped
    container_name: connector-db    
    environment:
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_USER: postgres    
    ports:
      - 5432:5432

  coppatrainer:
    image: gitlab.uni-koblenz.de:4567/process-science/internship/coppa-sose-23/coppa-trainer:latest
    container_name: coppatrainer    
    restart: unless-stopped    
    ports:
      - 8000:8000
    depends_on:
      - coppaconnector

  coppapredictor:
    image: gitlab.uni-koblenz.de:4567/process-science/internship/coppa-sose-23/coppa-predictor:latest
    container_name: coppapredictor    
    restart: unless-stopped    
    ports:
      - 8090:8090
    depends_on:
      - coppatrainer
```
- run the command ```docker-compose up -d``` in the Terminal (Terminal must be started in same Path where the docker-compose file is located)
- Container should be running in docker now

### Run in IDE
First, make sure you will be running the following commands from within the correct directory. To do so, open a terminal from the directory 'Trainer', which is a subdirectory of this project. Alternatively, open a terminal from the project directory and enter the following command:
```
cd Trainer
```

A virtual environment has to be installed and activated. To do so, use the following commands:
```
python -m venv myenv
myenv\Scripts\activate
```

After that, some libraries have to be installed. This is done via this command:
```
pip install -r requirements.txt
```

## Usage
The Trainer API can be offered by running the command ``python -m uvicorn api:app --reload`` and depends on the API offered by the "Connector", so make sure the "Connector" is also started. The API exports JSONs containing predictions for each active flow node of the requested process instance at an endpoint reachable under ``localhost:8000/prediction_export/{processInstanceKey}``. 

Exported JSONs are of the following format:
```json
{
    "key": 2251799820439069.0,
    "resultsRFC": [
        {
            "flowNodeId": "Activity_1xm9fc6",
            "nextFlowNode": "['' 'Activity_02v768m' 'Activity_0c3ibic' 'Activity_0mthdzh'\n 'Activity_0nkjpg1' 'Activity_0qonx8u' 'Activity_147yyfz'\n 'Activity_1ke82fi' 'Activity_1xm9fc6' 'Activity_1xu4ws9' 'Event_0h41kdq'\n 'Event_12geraz' 'Event_19t668s' 'Event_1b1br5q']",
            "probabilityForNextFlowNode": "[0.         0.         0.         0.         0.         0.\n 0.00357143 0.         0.         0.         0.00207143 0.02063095\n 0.965      0.00872619]",
            "incident": "False",
            "probabilityForIncident": "1.0",
            "duration": "20535",
            "probabilityForDuration": "0.46099999999999985"
        },
        {
            "flowNodeId": "Activity_0c3ibic",
            "nextFlowNode": "['' 'Activity_02v768m' 'Activity_0c3ibic' 'Activity_0mthdzh'\n 'Activity_0nkjpg1' 'Activity_0qonx8u' 'Activity_147yyfz'\n 'Activity_1ke82fi' 'Activity_1xm9fc6' 'Activity_1xu4ws9' 'Event_0h41kdq'\n 'Event_12geraz' 'Event_19t668s' 'Event_1b1br5q']",
            "probabilityForNextFlowNode": "[0.335 0.    0.    0.    0.    0.    0.    0.    0.    0.665 0.    0.\n 0.    0.   ]",
            "incident": "False",
            "probabilityForIncident": "1.0",
            "duration": "38322",
            "probabilityForDuration": "0.65"
        }
    ],
    "resultsXGB": [
        {
            "flowNodeId": "Activity_1xm9fc6",
            "nextFlowNode": "['' 'Activity_02v768m' 'Activity_0c3ibic' 'Activity_0mthdzh'\n 'Activity_0nkjpg1' 'Activity_0qonx8u' 'Activity_147yyfz'\n 'Activity_1ke82fi' 'Activity_1xm9fc6' 'Activity_1xu4ws9' 'Event_0h41kdq'\n 'Event_12geraz' 'Event_19t668s' 'Event_1b1br5q']",
            "probabilityForNextFlowNode": "[0.00823662 0.00249426 0.00200074 0.00107785 0.0012827  0.00474899\n 0.01166014 0.00233128 0.00364042 0.00124066 0.01005206 0.04484832\n 0.88585824 0.02052777]",
            "incident": "False",
            "probabilityForIncident": "0.9916369",
            "duration": "11220",
            "probabilityForDuration": "0.0070555075"
        },
        {
            "flowNodeId": "Activity_0c3ibic",
            "nextFlowNode": "['' 'Activity_02v768m' 'Activity_0c3ibic' 'Activity_0mthdzh'\n 'Activity_0nkjpg1' 'Activity_0qonx8u' 'Activity_147yyfz'\n 'Activity_1ke82fi' 'Activity_1xm9fc6' 'Activity_1xu4ws9' 'Event_0h41kdq'\n 'Event_12geraz' 'Event_19t668s' 'Event_1b1br5q']",
            "probabilityForNextFlowNode": "[3.6086727e-02 1.3162993e-03 1.0558555e-03 5.6881615e-04 6.7692046e-04\n 3.4210309e-03 4.9073454e-03 1.2302904e-03 1.9211640e-03 8.9144301e-01\n 4.4484115e-03 2.5879119e-02 3.8870568e-03 2.3157943e-02]",
            "incident": "False",
            "probabilityForIncident": "0.9916369",
            "duration": "11220",
            "probabilityForDuration": "0.0070555266"
        }
    ]
}
```
_Note: The order of the probabilities of the list "probaibilitiyForNextFlowNode" corresponds to the order of the flow node IDs of the list "nextFlowNode"._

## Authors
- Florian Nebenführ (@fnebenfuehr)
- Julia Märdian (@maerdian01)
- Valerie Simon (@vsimon)
- Jonas Breitzter (@jbreitzter)
- Nico Weiand (@nweiand)
- Carolin Dillenburg (@cdillenburg)

## Project status
Trainer finished
