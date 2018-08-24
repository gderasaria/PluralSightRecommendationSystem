# Plural Sight Recommendation challenge 

The project is an attempt to compute user similarity between users that have taken assessments, courses or are interested in technologies and are looking to take courses or assessment. There was a need to come up with a metric that would try to capture similarity between users. Due to the different types of users involved there are three similarity scores, assessment scores, course scores and interests score.


## Getting Started

To run the application on a local environment clone the repo by downloading the zip file or running the following command in your terminal.
```
git clone https://github.com/gderasaria/PluralSightRecommendationSystem.git
```

### Prerequisites

The following packages would be needed to run the project 


pandas 
numpy 
pickle 
scipy  
sklearn  
operator
flask 
flask_restful 
flask_httpauth 
flask_jwt 
flask_bcrypt 
flask_json  
http.client
json
base64
ssl
glob


### Training

from the root directory type the following command in terminal

```
python models/train.py
```

### Testing

For testing run a seperate terminal for client and server.
The input can be changed from models/data/user.json.

Start up the server by following command 

```
python app.py
```

On the client side running the following command

```
python test.py
```


### Results

The results can be seen in models/data/results.json
