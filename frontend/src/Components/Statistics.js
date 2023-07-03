import { useState, useEffect } from 'react';

function Statistics(props) {
  const [bp, setBPM] = useState(0);
  const [score, setScore] = useState(0);
  const [speed, setSpeed] = useState(0);
  const [calories, setCalories] = useState(0);

  useEffect(() => {

    const intervalId = setInterval(async () => {
      if (props.state) {
        const response = await fetch("http://teamtokyo.duckdns.org/getWorkout");

        let json = await response.json();
        console.log("JSON:", json)
        setScore(json["Score"])
        setBPM(json["BP"]);
        setSpeed(json["Speed"]);
        setCalories(json["Calories"]);
      }
    }, 1000);

    return () => {
      setBPM(0);
      setScore(0);
      setCalories(0);
      clearInterval(intervalId);
      //clearInterval(intervalId2);
    };
  }, [props.state]);

  // return (
  //   <div className="relative overflow-hidden bg-white place-self-end ">

  //     <div className="text-center flex-auto">
  //       <h2 className="text-3xl font-bold tracking-wide text-black text-center">
  //         Score
  //         <p className="font-mono text-8xl">
  //           {score}
  //         </p>
  //       </h2>
  //     </div>

      

  //     <div className="text-center flex-auto">

  //       <div className="text-8xl font-bold tracking-tight text-black text-center">
  //         BPM: {bp}
  //       </div>

  //       <div className="grid-cols-2 grid text-3xl font-bold tracking-tight text-black py-4">
  //         <div>Calories Burnt 
         
  //         </div>
  //         <div className='py-3'>
  //         Speed
  //         <p className="font-mono text-8xl pt-6"> {score}
  //         </p>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // );

  return (
    <div className="items-center w-full min-h-screen col-span-2">


      <h2 className="text-xl font-bold h-100 text-white flex flex-col-4 justify-around">

      <div className="text-center flex-auto">
        <div className="text-1xl font-bold tracking-tight text-black text-center">
          BPM: {bp}
        </div>

        <div className="grid-cols-3 grid text-3xl font-bold tracking-tight text-black py-16">
        
          <div className="text-transparent bg-clip-text bg-gradient-to-br from-black to-amber-500">Calories Burnt <br /> 
          <p className="font-mono text-8xl"> {calories.toFixed(1)}
          </p>
          </div>

          <div className="text-transparent bg-clip-text bg-gradient-to-br from-black to-red-500">Score <br /> 
          <p className="font-mono text-8xl"> {score}
          </p>
          </div>

          <div className="text-transparent bg-clip-text bg-gradient-to-br from-black to-orange-500">
          Max Acceleration
          <p className="font-mono text-8xl"> {speed.toFixed(2)}
          </p>
          </div>
        </div>
      </div>
        {/* <span> BPM: {bp} </span>

        <span> Score : {score}</span>

        <span> Calories Burnt : {calories}</span>

        <span> Max Acceleration : {speed}</span> */}

      </h2>

    </div>
  );
}

export default Statistics;
