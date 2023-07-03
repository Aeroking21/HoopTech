import StatsModel from "./StatsModel";
import { useState, useEffect } from "react";


function CalorieBurn(props) {
  const [formData, setFormData] = useState({
    weight: "",
    age: "",
    workoutName: "",
    gender: ""
  });

  const [workoutData, setWorkoutData] = useState({
    CalorieBurn: 0,
    Speed: 0,
    BPM: 0,
    Score: 0
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    handleStart();
    props.passData(true);

    let data = formData;
    data["time"] = new Date();

    const res = await fetch("http://teamtokyo.duckdns.org/startTransmission", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const dataStart = await res.json();
    console.log(dataStart);
  };

  const handleStopBtn = async (e) => {
    e.preventDefault();
    handleStop();

    props.passData(false);
    let data = formData;
    data["time"] = new Date();
    const res = await fetch('http://teamtokyo.duckdns.org/getTotalWorkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    data = await res.json();
    console.log("Form return:", data)
    setWorkoutData(data)
    setModalShow(true);
  };

  // Modal Functinality
  const [modalShow, setModalShow] = useState(false);

  // Stopwatch Functionality
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let intervalId;
    if (isRunning) {
      intervalId = setInterval(() => {
        setTime((prevTime) => prevTime + 1);
      }, 1000);
    }

    return () => clearInterval(intervalId);
  }, [isRunning]);

  function handleStart() {
    setIsRunning(true);
  }

  function handleReset() {
    setTime(0);
  }

  function handleStop() {
    setIsRunning(false);
  }

  return (
    //<div class="min-h-screen border-2 border-green-800 flex flex-col justify-center py-12 px-6 lg:px-8">
    <div class="flex flex-wrap relative align-center w-auto">

      <StatsModel
        show={modalShow}
        change={setModalShow}
        data={workoutData}
        onHide={() => setModalShow(false)}
      />


      <div class="relative isolate overflow-hidden py-24 w-auto px-10 rounded-3xl">
        {/* <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 2048 2048"
          className="absolute top-1/2 left-1/2 -z-10 h-[64rem] w-[64rem] -translate-y-1/2 [mask-image:radial-gradient(closest-side,white,transparent)] sm:left-full sm:-ml-80 lg:left-1/2 lg:ml-0 lg:translate-y-0 lg:-translate-x-1/2"
          aria-hidden="true"
        >
          <circle
            cx={256}
            cy={768}
            r={512}
            fill="url(#759c1415-0410-454c-8f7c-9a820de03641)"
            fillOpacity="0.7"
          />
          <defs>
            <radialGradient id="759c1415-0410-454c-8f7c-9a820de03641">
              <stop stopColor="#7775D6" />
              <stop offset={1} stopColor="#E935C1" />
            </radialGradient>
          </defs>
        </svg> */}
        <form class="mb-0 space-y-8 " onSubmit={handleSubmit}>
          <div>
            <label class="block text-xl text-black font-bold">
              Workout Name
            </label>
            <div class="mt-1">
              <input
                name="workoutName"
                type="text"
                required
                onChange={handleChange}
                class="rounded-3xl shadow-md text-xl"
              />
            </div>
          </div>
          <div>
            <label class="block text-xl text-black font-bold ">
              Weight (KG)
            </label>
            <div class="mt-1">
              <input
                name="weight"
                type="text"
                required
                onChange={handleChange}
                class="rounded-3xl shadow-md text-xl"
              />
            </div>
          </div>

          <div>
            <label class="block text-xl text-black font-bold">
              Age
            </label>
            <div class="mt-1">
              <input
                name="age"
                type="text"
                required
                onChange={handleChange}
                class="rounded-3xl shadow-md text-xl"
              />
            </div>
          </div>

          <div>
            <label class="block text-xl font-bold text-black">
              Gender
            </label>
            <div class="mt-1">
              <select
                name="gender"
                id="company-size"
                class="rounded-3xl shadow-md"
                onChange={handleChange}
              >
                <option value="">Please select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>

          <div className="flex justify-between ">
            <button
              type="submit"
              class="rounded-full font-bold bg-orange-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              Start
            </button>
            <button
              onClick={handleStopBtn}
              disabled={!isRunning}
              type="button"
              class="rounded-full font-bold bg-red-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              End
            </button>
          </div>

          <div class="relative text-xl font-bold">
            <p class="py-4 text-black "> Duration: {time} seconds</p>
            <button
              onClick={handleReset}
              disabled={isRunning}
              type="button"
              class="rounded-full font-bold bg-red-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>
  );

}

export default CalorieBurn;
