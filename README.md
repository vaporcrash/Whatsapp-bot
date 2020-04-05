# Whatsapp-bot

We'll have 2 different workflows
1. Question management by Admin user
2. Multiplayer Quiz using whatsapp bot


#### Question management
* Admin will need to create Questions/Answer pairs and have ability to perform CRUD actions on them.
* Questions can be grouped in Quizzes that will be sent out together to players
* Admin will have the capability to trigger a quiz , ie. set a timer for when the quiz should start 


#### Multiplayer Quiz
The Quiz can be broken into multiple steps : 
* Player signup : Players will send a message via whatsapp to sign up before the deadline
* Quiz game : Bot will send the questions from the chosen quiz to the registered players and responses will be stored at the server side
* Leaderboard : After half an hour time limit is over, server will analyze all answers from all users for quiz and send a leaderboard to admin


## Techincal Stack

* **Flask** :server to handle all requests from admin & users
* **Twillio** :for whatsapp integration
* **MongoDB** : for data storage


## Tables 
###### Quizzes

| quiz_id | quiz_name | duration | questions |
| ------- |:---------:| --------:| --------: |

##### Questions 

| question_id | questions_type | question | answer | difficulty | category | created_by | timestamp |
| ------- |:---------:| --------:| --------: | --------: | --------: | --------: |--------: |


##### Session

| sessions_id | start_time | end_time | quiz_id | members | 
| ------- |:---------:| --------:| --------: | --------: | 


## Future Tasks
1. Cumulative leaderboard
2. Random quiz generators
3. Similar but not equal answers. 
