import { useState, useEffect } from 'react';
import 'chartjs-adapter-date-fns';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  TimeScale,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';


ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


function Chart(props) {

  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "BPM",
        data: [],
        backgroundColor: "Red",
        borderColor: "Red",
        borderWidth: 0.1,
        pointRadius: 3,
        pointHitRadius: 10
      },
    ],
  });


  useEffect(() => {


    const intervalId2 = setInterval( async () => {
      if(props.state){
        const response = await fetch("http://teamtokyo.duckdns.org/getWorkoutChart");
        let json = await response.json();

        const newData = { ...chartData };
        newData.labels.push(new Date().toLocaleTimeString());
        newData.datasets[0].data.push(json['BP']);
        console.log(newData.datasets[0])
        setChartData(newData);
      }
    }, 1000);

    return () => {;
      clearInterval(intervalId2);
    };
  }, [props.state]);

  const options = {
    plugins: {
      customCanvasBackgroundColor: {
        color: 'White',
      }
    },
    scale: {
      x: {
        type: "time",
        time: {
          unit: "second",
        },
      },
    },
    tension: {
      duration: 100,
      easing: "linear",
      from: 1,
      to: 0,
      loop: true,
    },
  };

  return (
    <div className="flex flex-wrap grid-span-2 p-10 justify-start w-full">
      <Line data={chartData} options={options} />
    </div>
  );
}

export default Chart;
