import { useState } from "react";

function About() {
  const [info, setInfo] = useState("");

  const getInfo = async () => {
    const res = await fetch("http://localhost:5000/api/about");
    const data = await res.json();
    setInfo(data.message);
  };

  return (
    <div>
      <h2>About Page</h2>
      <button onClick={getInfo}>Get About Info</button>
      <p>{info}</p>
    </div>
  );
}

export default About;
