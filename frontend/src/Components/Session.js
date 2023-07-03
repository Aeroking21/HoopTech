import { useNavigate, useLocation } from "react-router-dom";
import { useState, } from "react";
import HistoryModal from "./HistoryModal";



function Session() {
  const navigate = useNavigate();

  const { state } = useLocation();

  const { id } = state;

  const name = () => {
    return localStorage.getItem(id).split(",")[1];
  };

  // Modal Functinality
  const [modalShow, setModalShow] = useState(false);
  const [formData, setFormData] = useState({
    workoutName: "",
  });

  const [workoutData, setWorkoutData] = useState({
    CalorieBurn: 0,
    Speed: 0,
    BPM: 0,
    Score: 0
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    //props.passData(true);

    let data = formData;

    const res = await fetch("http://teamtokyo.duckdns.org/getHistory", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const dataStart = await res.json();
    console.log("Data sent to workout is:", JSON.stringify(data));
    console.log("Data sent to workout is:", dataStart);

    setWorkoutData(dataStart);
    setModalShow(true);
  };


  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };


  return (
    <div className="bg-gradient-to-b from-white to-red-300 flex flex-row justify-center min-h-screen">

      <HistoryModal
        show={modalShow}
        change={setModalShow}
        data={workoutData}
        onHide={() => setModalShow(false)}
      />
      
      <div className="relative isolate overflow-hidden flex items-center">
        


        <div className="flex-row text-center justify-start">

          <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-black to-red-500">
            Hello, {name()}!
          </h2>
          <br />
          <button
            onClick={() => navigate("/main")}
            class="rounded-full font-bold bg-red-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            Let's Workout!
          </button>
          <br />
          <br />
          <form className=" border-3 border-red-500 space-y-8 " onSubmit={handleSubmit}>
            <div>
              <label class="p-4 block text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-black to-red-600">
                Workout Search
              </label>
              <div class="">
                <input
                  name="workoutName"
                  type="text"
                  required
                  onChange={handleChange}
                  class="rounded-3xl shadow-md text-md"
                />
              </div>
            </div>
            

            <div className="flex justify-evenly">
              <button
                type="submit"
                class="rounded-full font-bold bg-orange-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Search
              </button>
            </div>
          </form>

        </div>
      </div>
    </div>
  );
}

export default Session;
