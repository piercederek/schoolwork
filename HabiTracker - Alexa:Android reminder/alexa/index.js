var Alexa = require("alexa-sdk");
var appId = 'amzn1.ask.skill.4bf06049-c118-4aee-944f-026fc7dd1521'; //'amzn1.echo-sdk-ams.app.your-skill-id';
var AWS = require("aws-sdk");
AWS.config.update({endpoint: "https://dynamodb.us-east-1.amazonaws.com"});
var docClient = new AWS.DynamoDB.DocumentClient();
var table = "HabitTracker";

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.appId = appId;
    alexa.registerHandlers(newSessionHandlers, startSelectHandlers, newTaskModeHandlers, completeTaskModeHandlers, editTaskModeHandlers);
    alexa.execute();
};

var states = {
    SELECTMODE: '_SELECTMODE', // User is at top level, selecting what to do.
    NEWTASKMODE: '_NEWTASKMODE',  // Add a new habit.
    COMPLETEMODE: '_COMPLETEMODE', // Completing one of their tracked habits.
    EDITMODE: '_EDITMODE' // Making a change to an existing habit.
};

getTasks = function(session, params, callback) {
    docClient.get(params, function(err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:" + JSON.stringify(err, null, 2));
            callback(false);
        } else {
            console.log("GetItem succeeded:" + JSON.stringify(data["Item"], null, 2));
            callback(session, data.Item);
        }
    });
}

updateTasks = function(session, params, callback) {
    docClient.update(params, function(err, data) {
        if (err) {
            console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
            callback(false);
        } else {
            console.log("updated");
            callback(session);
        }
    });
} 

var newSessionHandlers = {
    'NewSession': function() {
        var params = {TableName: table, Key:{"userid":"Test"}};
        getTasks(this, params, function(session, task) {
            if (task) {
                var tasks = [];
                for(var i = 0; i < task["tasks"].length; i++) {
                    tasks.push(task["tasks"][i]);
                }
                session.attributes['stepByStep'] = false;
                session.attributes['tasks'] = tasks;
                session.handler.state = states.SELECTMODE;
                var toDo = 0;
                var currentTime = Math.round(Date.now()/1000);
                for (var i = 0; i < session.attributes["tasks"].length; i++) {
                    if ((currentTime - session.attributes["tasks"][i]["timeCompleted"])/3600 > 18 && session.attributes["tasks"][i]["frequency"] == "daily") {
                        toDo++;
                    } else if ((currentTime - session.attributes["tasks"][i]["timeCompleted"])/3600 > 162 && session.attributes["tasks"][i]["frequency"] == "weekly") {
                        toDo++;
                    } else if ((currentTime - session.attributes["tasks"][i]["timeCompleted"])/3600 > 714 && session.attributes["tasks"][i]["frequency"] == "monthly") {           
                        toDo++;
                    }
                }
                if (toDo == 0) {
                    session.emit(":ask", "Habit tracker here, you don't have anything to do today, is there anything I can help you with?")
                } else {
                    session.emit(":ask", "Habit tracker here, you have " + toDo.toString() + " things left to do today, to find out what they are say what do i have to do today?");
                }
            }
        });
    },
    "AMAZON.StopIntent": function() {
      this.emit(':tell', "Goodbye!");  
    },
    "AMAZON.CancelIntent": function() {
      this.emit(':tell', "Goodbye!");  
    },
    'SessionEndedRequest': function () {
        console.log('session ended!');
        this.emit(":tell", "Goodbye!");
    }
};

var startSelectHandlers = Alexa.CreateStateHandler(states.SELECTMODE, {
    'NewSession': function () {
        this.emit('NewSession');
    },
    'LaunchRequest': function () {
        this.emit('NewSession');
    },
    'AMAZON.HelpIntent': function() {
        this.emit(':ask', "You can say what are my habits to get a list of everything, i want to check off a habit if you finished something, track a new habit to create a new habit, i want to change followed by a habit name to make a change, what are my stats for followed by a habit to get your stats, or stop tracking followed by a habit to remove it.");
    },
    "AMAZON.StopIntent": function() {
        this.emit(":tell", "Goodbye!");   
    },
    'SessionEndedRequest': function () {
        console.log("SESSIONENDEDREQUEST");
        this.emit(':tell', "Goodbye!");
    },
    'ReadAllIntent': function() {
        var habits = [];
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            habits.push(this.attributes["tasks"][i]["task"] + " " + this.attributes["tasks"][i]["frequency"]);
        }
        this.emit(':ask', "You want to " + habits.join(", "));
    },
    'DoTodayIntent': function() {
        var toDo = [];
        var currentTime = Math.round(Date.now()/1000);
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 > 18 && this.attributes["tasks"][i]["frequency"] == "daily") {
                toDo.push(this.attributes["tasks"][i]["task"]);
            } else if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 > 162 && this.attributes["tasks"][i]["frequency"] == "weekly") {
                toDo.push(this.attributes["tasks"][i]["task"]);
            } else if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 > 714 && this.attributes["tasks"][i]["frequency"] == "monthly") {           
                toDo.push(this.attributes["tasks"][i]["task"]);
            }
        }
        if (toDo.length == 0) {
            this.emit(":ask", "You don't have anything to do today, is there anything else I can do for you?")
        } else {
            this.emit(":ask", "Today you need to " + toDo.join(", "));
        }
    },
    'NewTaskIntent': function() {
        this.handler.state = states.NEWTASKMODE;
        this.emit(':ask', "What habit would you like to track?");
    },
    'DeleteTaskIntent': function() {
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if (this.attributes["tasks"][i]["task"] == this.event.request.intent.slots.taskName.value) {
                delete this.attributes["tasks"][i];
                var params = {TableName: table, Key:{"userid":"Test"}, UpdateExpression: "set tasks = :tasks", ExpressionAttributeValues: {":tasks":this.attributes["tasks"]}, ReturnValues:"UPDATED_NEW"};

                updateTasks(this, params, function(session) {
                    session.emit(":ask", "OK I won't remind you anymore");
                });
            }
        }
    },
    'AllDetailsTaskIntent': function() {
        this.handler.state = states.NEWTASKMODE;
        this.attributes['newTask'] = {"task":this.event.request.intent.slots.taskName.value};
        this.attributes['newTask']['frequency'] = this.event.request.intent.slots.frequency.value;
        this.attributes['newTask']['time'] = this.event.request.intent.slots.taskTime.value;
        this.attributes['newTask']['timeCompleted'] = 0;
        this.attributes['newTask']['bestStreak'] = 0;
        this.attributes['newTask']['currentStreak'] = 0;
        this.emit(":ask", "So you want to " + this.attributes["newTask"]["task"] + " " + this.attributes["newTask"]["frequency"] + " and you want to be reminded in the " + this.attributes["newTask"]["time"]);
    },
    'TaskCompletedIntent': function() {
        this.handler.state = states.COMPLETEMODE;
        this.emit(":ask", "Which habit did you finish?");
    },
    'EditStatsIntent': function() {
        this.handler.state = states.EDITMODE;
        this.attributes["editName"] = this.event.request.intent.slots.editName.value;
        this.emit(":ask", "Would you like to change the frequency, or time of day?");
    },
    'GetStatsIntent': function() {
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if (this.attributes["tasks"][i]["task"] == this.event.request.intent.slots.statsName.value) {
                this.emit(":ask", "You have completed " + this.event.request.intent.slots.statsName.value + " " + this.attributes["tasks"][i]["currentStreak"] + " times in a row, your all time record is " + this.attributes["tasks"][i]["bestStreak"] + " times in a row.");
            }
        }
    },
    'Unhandled': function() {
        console.log("UNHANDLED");
        this.emit(':ask', 'Sorry I didn\'t get that. You can say what are my habits to get a list of everything, i want to check off a habit if you finished something, track a new habit to create a new habit, i want to change followed by a habit name to make a change, what are my stats for followed by a habit to get your stats, or stop tracking followed by a habit to remove it.');
    }
});

var newTaskModeHandlers = Alexa.CreateStateHandler(states.NEWTASKMODE, {
    'NewSession': function() {
        this.emit('NewSession');
    },
    'LaunchRequest': function() {
        this.emit('NewSession');
    },
    'TaskNameIntent': function() {
        this.attributes['newTask'] = {"task":this.event.request.intent.slots.taskName.value};
        this.attributes['stepByStep'] = true;
        this.emit(":ask", "How often would you like to do this? Daily, weekly, or monthly?");
    },
    'TaskFrequencyIntent': function() {
        this.attributes['newTask']['frequency'] = this.event.request.intent.slots.frequency.value;
        this.emit(":ask", "Would you like to be reminded in the morning, afternoon, or evening?");
    },
    'TaskTimeIntent': function() {
        this.attributes['newTask']['time'] = this.event.request.intent.slots.taskTime.value;
        this.emit(":ask", "So you want to " + this.attributes["newTask"]["task"] + " " + this.attributes["newTask"]["frequency"] + " and you want to be reminded in the " + this.attributes["newTask"]["time"]);
    },
    'AllDetailsTaskIntent': function() {
        this.handler.state = states.NEWTASKMODE;
        this.attributes['newTask'] = {"task":this.event.request.intent.slots.taskName.value};
        this.attributes['newTask']['frequency'] = this.event.request.intent.slots.frequency.value;
        this.attributes['newTask']['time'] = this.event.request.intent.slots.taskTime.value;
        this.attributes['newTask']['timeCompleted'] = 0;
        this.attributes['newTask']['bestStreak'] = 0;
        this.attributes['newTask']['currentStreak'] = 0;
        this.emit(":ask", "So you want to " + this.attributes["newTask"]["task"] + " " + this.attributes["newTask"]["frequency"] + " and you want to be reminded in the " + this.attributes["newTask"]["time"]);
    },
    'AMAZON.YesIntent': function() {
        this.attributes['newTask']['timeCompleted'] = 0;
        this.attributes['newTask']['bestStreak'] = 0;
        this.attributes['newTask']['currentStreak'] = 0;
        this.attributes["tasks"].push(this.attributes['newTask']);
        var params = {TableName: table, Key:{"userid":"Test"}, UpdateExpression: "set tasks = :tasks", ExpressionAttributeValues: {":tasks":this.attributes["tasks"]}, ReturnValues:"UPDATED_NEW"};

        this.handler.state = states.SELECTMODE;
        updateTasks(this, params, function(session) {
            if (session.attributes['stepByStep'] == false) {
                session.emit(":ask", "OK I will remind you, is there anything else you want to do?");
            } else {
                session.emit(":ask", "OK I will remind you, next time you can use one phrase in the form i want to " + session.attributes["newTask"]["task"] + " " + session.attributes["newTask"]["frequency"] + " remind me in the " + session.attributes["newTask"]["time"]);
            }
        });
    },
    'AMAZON.NoIntent': function() {
        this.emit(":ask", "Ok if you want to change the name say i want to followed by what the name you want. If you want to change the frequency say either daily, weekly, or monthly. If you want to change the time of day say morning, afternoon, or evening.");
    },
    'AMAZON.HelpIntent': function() {
        this.emit(':ask', 'You need to specify a name, a frequency of daily, weekly, or monthly, and a time of day that you would like to be reminded either morning, afternoon, or evening');
    },
    'ReadAllIntent': function() {
        var habits = [];
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            habits.push(this.attributes["tasks"][i]["task"] + " " + this.attributes["tasks"][i]["frequency"]);
        }
        this.emit(':ask', "You want to " + habits.join(", "));
    },
    "AMAZON.CancelIntent": function() {
        this.handler.state = states.SELECTMODE;
        console.log("CANCELINTENT");
    },
    'SessionEndedRequest': function () {
        this.handler.state = states.SELECTMODE;
        this.emit(":tell", "Goodbye");
    },
    'Unhandled': function() {
        console.log("UNHANDLED");
        this.emit(':ask', 'Sorry I didn\'t get that. If you were trying to name the habit say i want to followed by the name. If you were specifying a frequency say daily, weekly, or monthly. If you were specifying a time of day say morning, afternoon, or evening.');
    }
});

var completeTaskModeHandlers = Alexa.CreateStateHandler(states.COMPLETEMODE, {
    'NewSession': function() {
        this.emit('NewSession');
    },
    'LaunchRequest': function() {
        this.emit('NewSession');
    },
    'CompletedSpecificIntent': function() {
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if (this.attributes["tasks"][i]["task"] == this.event.request.intent.slots.completeTask.value) {
                var currentTime = Math.round(Date.now()/1000);
                if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 < 24 && this.attributes["tasks"][i]["frequency"] == "daily") {
                    this.attributes['tasks'][i]['currentStreak'] += 1;
                    if (this.attributes['tasks'][i]['currentStreak'] > this.attributes['tasks'][i]['bestStreak']) {
                        this.attributes['tasks'][i]['bestStreak'] = this.attributes['tasks'][i]['currentStreak'];
                    }
                } else if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 < 168 && this.attributes["tasks"][i]["frequency"] == "weekly") {
                    this.attributes['tasks'][i]['currentStreak'] += 1;
                    if (this.attributes['tasks'][i]['currentStreak'] > this.attributes['tasks'][i]['bestStreak']) {
                        this.attributes['tasks'][i]['bestStreak'] = this.attributes['tasks'][i]['currentStreak'];
                    }
                } else if ((currentTime - this.attributes["tasks"][i]["timeCompleted"])/3600 < 720 && this.attributes["tasks"][i]["frequency"] == "monthly") {           
                    this.attributes['tasks'][i]['currentStreak'] += 1;
                    if (this.attributes['tasks'][i]['currentStreak'] > this.attributes['tasks'][i]['bestStreak']) {
                        this.attributes['tasks'][i]['bestStreak'] = this.attributes['tasks'][i]['currentStreak'];
                    }
                } else {
                    this.attributes["tasks"][i]["currentStreak"] = 1;
                    if (this.attributes['tasks'][i]['currentStreak'] > this.attributes['tasks'][i]['bestStreak']) {
                        this.attributes['tasks'][i]['bestStreak'] = this.attributes['tasks'][i]['currentStreak'];
                    }
                }
                this.attributes["tasks"][i]["timeCompleted"] = currentTime;
                var params = {TableName: table, Key:{"userid":"Test"}, UpdateExpression: "set tasks = :tasks", ExpressionAttributeValues: {":tasks":this.attributes["tasks"]}, ReturnValues:"UPDATED_NEW"};
                this.handler.state = states.SELECTMODE;
                updateTasks(this, params, function(session) {
                    if (session == false) {
                        session.emit(":ask", "I'm sorry I couldn't find that.");
                    } else {
                        session.emit(":ask", "Great job, keep up the good work. Is there anything else I can do for you?");     
                    }
                });
                return;

            }
        };
        this.emit(":ask", "I am sorry I couldn't find your specified habit, could you try again");
    },
    'AMAZON.HelpIntent': function() {
        this.emit(':ask', 'You need to specify which habit you finished by saying i finished followed by the task name, you can say what are my habits to get the full list if you do not recall the name.');
    },
    'ReadAllIntent': function() {
        var habits = [];
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            habits.push(this.attributes["tasks"][i]["task"] + " " + this.attributes["tasks"][i]["frequency"]);
        }
        this.emit(':ask', "You want to " + habits.join(", "));
    },
    "AMAZON.CancelIntent": function() {
        this.handler.state = states.SELECTMODE;
        console.log("CANCELINTENT");
    },
    'SessionEndedRequest': function () {
        this.handler.state = states.SELECTMODE;
        this.emit(":tell", "Goodbye");
    },
    'Unhandled': function() {
        console.log("UNHANDLED");
        this.emit(':ask', 'Sorry, I didn\'t get that. You need to specify which habit you finished by saying i finished followed by the task name, you can say what are my habits to get the full list if you do not recall the name.');
    }
});

var editTaskModeHandlers = Alexa.CreateStateHandler(states.EDITMODE, {
    'NewSession': function() {
        this.emit('NewSession');
    },
    'LaunchRequest': function() {
        this.emit('NewSession');
    },
    'EditWhatIntent': function() {
        this.attributes["editType"] = this.event.request.intent.slots.editType.value;
        if (this.event.request.intent.slots.editType.value == "frequency") {
            this.emit(":ask", "Would you like to set it to daily, weekly, or monthly?");
        } else if (this.event.request.intent.slots.editType.value == "time of day") {
            this.emit(":ask", "Would you like to set it to morning, afternoon, or evening?");
        } else {
            this.emit(":ask", "I am sorry I did not catch that, do you want to change the name, frequency, or time of day?");
        }
    },
    'TaskTimeIntent': function() {
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if (this.attributes["tasks"][i]["task"] == this.attributes["editName"]) {
                this.attributes["tasks"][i]["time"] = this.event.request.intent.slots.taskTime.value;
                var params = {TableName: table, Key:{"userid":"Test"}, UpdateExpression: "set tasks = :tasks", ExpressionAttributeValues: {":tasks":this.attributes["tasks"]}, ReturnValues:"UPDATED_NEW"};
                this.handler.state = states.SELECTMODE;
                updateTasks(this, params, function(session) {
                    session.emit(":ask", "OK I have made the change.");
                });
                return;
            }
        }
        this.emit(":ask", "I am sorry I did not understand, could you restate?");
    },
    'TaskFrequencyIntent': function() {
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            if (this.attributes["tasks"][i]["task"] == this.attributes["editName"]) {
                this.attributes["tasks"][i]["frequency"] = this.event.request.intent.slots.frequency.value;
                var params = {TableName: table, Key:{"userid":"Test"}, UpdateExpression: "set tasks = :tasks", ExpressionAttributeValues: {":tasks":this.attributes["tasks"]}, ReturnValues:"UPDATED_NEW"};
                this.handler.state = states.SELECTMODE;
                updateTasks(this, params, function(session) {
                    session.emit(":ask", "OK I have made the change.");
                });
                return;
            }
        }
        this.emit(":ask", "I am sorry I did not understand, could you restate?");
    },
    'AMAZON.HelpIntent': function() {
        this.emit(":ask", "You can specify whether you were changing the name, frequency, or time of day. If you are specifying a frequency say daily, weekly, or monthly. If you are specifying a time of day say morning, afternoon, or evening.")
    },
    'ReadAllIntent': function() {
        var habits = [];
        for (var i = 0; i < this.attributes["tasks"].length; i++) {
            habits.push(this.attributes["tasks"][i]["task"] + " " + this.attributes["tasks"][i]["frequency"]);
        }
        this.emit(':ask', "You want to " + habits.join(", "));
    },
    'SessionEndedRequest': function () {
        this.emit(":tell", "Goodbye");
    },
    'Unhandled': function() {
        console.log("UNHANDLED");
        this.emit(':ask', 'Sorry, I didn\'t get that. You can specify whether you were changing the name, frequency, or time of day. If you are specifying a frequency say daily, weekly, or monthly. If you are specifying a time of day say morning, afternoon, or evening.');
    }
});