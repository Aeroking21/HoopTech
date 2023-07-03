import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Login from "./Components/Login"
import Session from './Components/Session';
import Register from './Components/Register';
import Clear from './Components/Clear';
import Main from './Components/Main';


function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route exact path="/"
            element={<Login />}></Route>

          <Route exact path="/session"
            element={<Session />}></Route>

          <Route exact path="/register"
            element={<Register />}></Route>

          <Route exact path="/clear"
            element={<Clear />}></Route>

          <Route exact path="/main"
            element={<Main />}></Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;




















// import './App.css';
// import CalorieBurn from './Components/Form';
// import Statistics from './Components/Statistics';
// import { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
// import Chart from './Components/Graph';



// function App() {

//   const [btnClick, setBtnClick] = useState();
  


//   return (
//     <div className="grid grid-rows-2 grid-cols-2 grid-flow-col gap-2 border-4 border-indigo-600">

//       <CalorieBurn passData={setBtnClick} > </CalorieBurn>

//       <Statistics state={btnClick}> </Statistics>
      
//       <Chart state={btnClick}> </Chart>
//     </div>
//   )

// }

// export default App;
