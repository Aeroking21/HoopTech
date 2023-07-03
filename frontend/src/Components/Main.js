import CalorieBurn from './Form';
import Statistics from './Statistics';
import { useState} from 'react';

import Chart from './Graph';



function Main() {

  const [btnClick, setBtnClick] = useState();


  return (
    <div className="flex flex-row justify-evenly bg-gradient-to-b from-white to-orange-300">

      <CalorieBurn  passData={setBtnClick} > </CalorieBurn>

      <div className="flex flex-col items-center py-24">

        <Chart  state={btnClick}> </Chart>

        <Statistics state={btnClick}> </Statistics>

       </div>

    </div>
  )

}

export default Main;