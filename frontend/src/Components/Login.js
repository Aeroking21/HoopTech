import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();

    const usernameval = event.target.username.value;
    const passwordval = event.target.password.value;

    const userstring = localStorage.getItem(String(usernameval));

    if (userstring === null) {
      alert("Please Register first");
    } else if (userstring.split(",")[0] === String(passwordval)) {
      navigate("/session", {
        state: { id: String(usernameval) },
        replace: true,
      });
    } else {
      alert("Incorrect username or password");
    }

    event.target.reset();
  };

  return (
    <div className="bg-gradient-to-b from-white to-orange-400 flex flex-row justify-center min-h-screen">
      <div className="elative isolate overflow-hidden flex items-center">
        <div className="flex-row text-center justify-start">
          {/* <img src="../../public/ballerlogo.png" style="height: 50px" alt="logo"></img> */}
          <h2 className="text-5xl font-bold py-10 text-transparent bg-clip-text bg-gradient-to-br from-black to-red-500">
            BB Trainer
          </h2>
          <form onSubmit={handleSubmit} className="w-full max-w-sm">
            <div>
              <label className="text-xl font-bold text-black" for="username">
                Username:&nbsp;
                <input
                  className="m-2 rounded-3xl text-md"
                  placeholder="Username"
                  type="text"
                  id="username"
                />
              </label>
            </div>
            <div>
              <label className="text-xl font-bold text-black" for="password">
                Password:&nbsp;&nbsp;
                <input
                  className="m-2 rounded-3xl text-md"
                  placeholder="******"
                  type="password"
                  id="password"
                />
              </label>
            </div>
            <div className="mt-10 flex items-center justify-evenly ">
              <button
                type="submit"
                className="rounded-full font-bold bg-orange-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Login
              </button>
              <button
                onClick={() => navigate("/register")}
                className="rounded-full font-bold bg-red-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Sign Up
              </button>
            </div>
          </form>
          <br />
          <br />
        </div>
      </div>
    </div>
  );
}

export default Login;
