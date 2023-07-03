
import { useNavigate } from "react-router-dom";


function Register() {
  const navigate = useNavigate();

  const handleSubmit = (event) => {

    event.preventDefault();

    const nameval = event.target.name.value;
    const usernameval = event.target.username.value;
    const passwordval = event.target.password.value;
    //const ageval = event.target.age.value;
    //const weightval = event.target.weight.value;

    if (
      !String(nameval) ||
      !String(usernameval) ||
      !String(passwordval)
    
    ) {
      alert("Invalid information");
      return;
    }
    for (let i = 0; i < localStorage.length; i++) {
      if (localStorage.key(i) === String(usernameval)) {
        alert("Username exists");
        return;
      }
    }

    var usersArr = [];
    usersArr.push([
      String(passwordval),
      String(nameval),
      //String(ageval),
      //String(weightval),
    ]);
    localStorage.setItem(String(usernameval), String(usersArr));

    navigate("/");

    event.target.reset();
  };

  return (
    <div className="bg-gradient-to-b from-white to-red-300 flex flex-row justify-center min-h-screen">

        <div className="relative isolate overflow-hidden flex items-center">
          

          <div className="flex-row text-center justify-start">
            <h2 className="text-5xl font-bold text-transparent bg-clip-text py-6 bg-gradient-to-br from-red-900 to-orange-500">
              Sign Up
            </h2>
            <br />
            <form
              onSubmit={handleSubmit}
              className="w-full max-w-full text-left px-6"
            >
              <div>
                <label className="text-xl font-bold text-black">
                  Name:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <input
                    className="m-2 rounded-3xl shadow-md text-md"
                    placeholder="Name"
                    type="text"
                    id="name"
                  />
                </label>
              </div>
              <div>
                <label className="text-xl font-bold text-black">
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
                <label className="text-xl font-bold text-black">
                  Password:&nbsp;&nbsp;
                  <input
                    className="m-2 rounded-3xl text-md"
                    type="password"
                    id="password"
                  />
                </label>
              </div>

              <div className="mt-10 flex items-center justify-center gap-x-6 lg:justify-center">
                <button
                  type="submit"
                  className="rounded-full font-bold bg-red-500 px-3.5 py-1.5 text-xl leading-7 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
                >
                  Confirm
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

export default Register;
