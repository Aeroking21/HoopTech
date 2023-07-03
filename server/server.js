const express = require('express');
const fs = require('fs');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const mqtt = require('mqtt');


const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))


const clientOptions = {
  username: "TeamTokyo",
  password: "TeamTokyo",
  rejectUnauthorized: false,
  key: fs.readFileSync('client.key'),
  cert: fs.readFileSync('client.crt'),
  ca: [ fs.readFileSync('ca.crt') ]
}


let Stats_Selection = {
  bpm: 0,
  score: 0,
  speed: 0
};

let tWorkout = {
  "BP": 0,
  "Speed": 0,
  "Score": 0,
  "Calories": 0,
};

let sample_data = {
  weight: "",
  age: "",
  workoutName: "",
  gender: "",
  time: new Date()
};

//Mongo Schema
// Avg speed, Avg bpm, workout storage(Total Calorie count)

const StatsSchema = new mongoose.Schema({
  Speed: Number,
  BPM: Number,
  Score: Number

});

const WorkoutSchema = new mongoose.Schema({
  WorkoutName: String,
  AvgBPM: Number,
  AvgSpeed: Number,
  Calories: Number,
  Score: Number

});

const Stats = mongoose.model("stats", StatsSchema);
const WorkoutHistory = mongoose.model("Workout", WorkoutSchema);

let connection = "mongodb+srv://TeamTokyo:TeamTokyo@basketball.dzriwuc.mongodb.net/?retryWrites=true&w=majority"
mongoose.set("strictQuery", false);

mongoose.connect(connection, { useNewUrlParser: true, UseUnifiedTopology: true })
  .then(app.listen(port, () => {
    console.log(`Express API listening on port ${port}`);;


    Stats.deleteMany({})
      .then(console.log("Deleted Stats Collection"))
      .catch((err) => console.log(err))
      ;

    WorkoutHistory.deleteMany({})
      .then(console.log("Deleted WorkOut Collection"))
      .catch((err) => console.log(err))
      ;

  }))

  .catch((err) => console.log(err))
  ;


const client = mqtt.connect("mqtts://18.133.234.200", clientOptions);

client.on('connect', function () {
  console.log('Connected to broker');

  // Subscribe to a topic
  client.subscribe('bpm');
});



// Handle incoming messages
client.on('message', function (topic, message) {
  if (topic === "bpm") {
    Stats_Selection = JSON.parse(message);
    // Push to database

    const StatsObj = new Stats({
      // Try use 2 dp here
      Speed: Stats_Selection["speed"],
      BPM: Stats_Selection["bpm"],
      Score: Stats_Selection["score"]

    });

    StatsObj.save()
      .then(function (result) {
        console.log("Updated in database")
      })
      .catch((err) => console.log(err))
      ;

    console.log('Received message and updated in DB:', Stats_Selection);
  }

  //console.log('Received message:', message.toString(), 'on topic:', topic);

});

app.get('/', function (req, res) {
  res.send("😃😃😃😃😃😃😃 Welcome ");
  console.log("/")
});

app.post('/startTransmission', function (req, res) {
  sample_data = req.body
  client.publish('StartTransmission', "true");
  res.json({ "Output": "Started Data Process" });
  console.log("/startTransmission")

});

app.post('/getHistory', function (req, res) {
  console.log("Req is", req.body)

  WorkoutHistory.findOne({ "WorkoutName": sample_data["workoutName"] })
    .then(function (result) {
      console.log("/getHistory")
      console.log(result)



      let average_bpm = result["AvgBPM"];
      let average_speed = result["AvgSpeed"];
      let TotalCalories = result["Calories"];
      let score = result["Score"];

      res.json({ "CalorieBurn": TotalCalories, "Speed": average_speed, "BPM": average_bpm, "Score": score });

    })

    .catch((err) => console.log(err))
    ;


});


app.post('/getTotalWorkout', function (req, res) {
  // Change this to actual data 
  // Find Avg speed, Avg bpm, calorie count
  // Then add to Workout history along with workout id
  // Then delete Stats collection

  Stats.aggregate([{ $group: { _id: null, bpm_average: { $avg: "$BPM" }, speed_average: { $avg: "$Speed" } } }], { allowDiskUse: true })
    .then(function (result) {

      let average_bpm = result[0]["bpm_average"];
      let average_speed = result[0]["speed_average"];
      let elapsed_time = (new Date() - new Date(sample_data["time"]));
      elapsed_time = seconds = Math.floor(elapsed_time / 1000);

      //console.log("Elasped time total workout", elapsed_time)

      let TotalCalories = calculateCalorieBurn(elapsed_time, average_bpm, sample_data["weight"], sample_data["age"], sample_data["gender"]);

      console.log(elapsed_time, average_bpm, sample_data["weight"], sample_data["age"], sample_data["gender"]);

      console.log("Total calories is", TotalCalories)
      let id = sample_data["workoutName"];

      let baskets_score; // needs to be from DB

      Stats.findOne().sort({ _id: -1 })
        .then(function (result) {
          baskets_score = result["Score"];
          console.log("Score is", baskets_score)

          const WorkoutObj = new WorkoutHistory({
            WorkoutName: id,
            AvgBPM: average_bpm,
            AvgSpeed: average_speed,
            Calories: TotalCalories,
            Score: baskets_score
          });

          WorkoutObj.save()
            .then(function (result) {
              console.log("Updated in database", result)
              res.json({ "CalorieBurn": TotalCalories, "Speed": average_speed, "BPM": average_bpm, "Score": baskets_score });
              console.log(req.body);
              client.publish('StartTransmission', "false");

              // Stats.deleteMany({})
              //   then(console.log("Deleted Stats Collection"))
              //   .catch((err) => console.log(err))
              // ;

            })
            .catch((err) => console.log(err))
            ;

          Stats.deleteMany({})
            .then(console.log("Deleted Stats Collection"))
            .catch((err) => console.log(err))
          ;

          client.publish('StartTransmission', "false");


        })
    })

    .catch ((err) => console.log(err))
  ;


});

app.get('/getWorkout', function (req, res) {
  console.log("/getWorkout")
  let elapsed_time = (new Date() - new Date(sample_data["time"]));
  //console.log("Elasped time get workout", elapsed_time)
  elapsed_time = seconds = Math.floor(elapsed_time / 1000);

  Stats.aggregate([{ $group: { _id: null, bpm_average: { $avg: "$BPM" }, speed_average: { $avg: "$Speed" } } }], { allowDiskUse: true })
    .then(function (result) {
      let average_bpm = result[0]["bpm_average"];
      console.log("Average BPM return is ", average_bpm)
      let average_speed = result[0]["speed_average"];


      let TotalCalories = calculateCalorieBurn(elapsed_time, average_bpm, sample_data["weight"], sample_data["age"], sample_data["gender"]);

      console.log("Average Calories return is ", TotalCalories)
      let score = 0; // needs to be from DB

      Stats.findOne().sort({ _id: -1 })
        .then(function (result) {
          score = result["Score"];

          let output = { "BP": average_bpm, "Speed": average_speed, "Score": score, "Calories": TotalCalories };
          tWorkout = output
          //console.log(Stats_Selection["bpm"], Stats_Selection['score'])
          //res.json({"BP" : Stats_Selection["bpm"], "Score": Stats_Selection['score'] });
          res.json(output);

        })
        .catch((err) => console.log(err))
        ;

    })
    .catch((err) => console.log(err))
    ;

});

app.get('/getWorkoutChart', function (req, res) {
  console.log("/getWorkout2")

  res.json(tWorkout);
});


// MongoDB Helper Functions

function calculateCalorieBurn(duration, heart_rate, weight, age, gender) {
  duration = duration / 60;
  let answer;

  console.log("CalorieFunc inputs:", duration, heart_rate, weight, age, gender)
  //console.log("CalorieFunc types:", typeof(duration), typeof(heart_rate), typeof(weight), typeof(age), typeof(gender));

  if (gender == "Male") {
    answer = (duration * (0.630 * heart_rate + 0.198 * weight + 0.2017 * age - 55.09)) / 4.184
  }
  else {
    answer = (duration * (0.477 * heart_rate - 0.126 * weight + 0.074 * age - 20.422)) / 4.184
  }

  console.log("CalorieFunc:", answer)
  return Math.abs(answer);
}

// function getScore() {
//   Stats.findOne().sort({ _id: -1 })
//     .then(function (result) {
//       console.log(result)
//       return result;
//     })
//     .catch((err) => console.log(err))
//   ;
// }

// function AVG_BPM() {
//   Stats.aggregate([{ $group: { _id: null, bpm_average: { $avg: "$BPM" }, speed_average: { $avg: "$Speed"}} }])
//     .then(function (result) {
//       return result;
//     })
//     .catch((err) => console.log(err))
//   ;
// }

// function AVG_Speed() {
//   Stats.aggregate([{ $group: { _id: null, average: { $avg: "$speed" } } }])
//     .then(function (result) {
//       return result[0].average;
//     })
//     .catch((err) => console.log(err))
//   ;
// }

// app.listen(port, function () {
//   console.log(`Express API listening on port ${port}`);
// });
