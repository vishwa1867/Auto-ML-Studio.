<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <style>
    body {
      margin: 0; font-family: Arial, sans-serif;
      display: flex; justify-content: center; align-items: center;
      height: 100vh; background: linear-gradient(135deg, black, #1e3c72, #2a5298);
      color: white;
    }
    .box {
      background: rgba(0,0,0,0.7); padding: 30px; border-radius: 10px;
      width: 300px; text-align: center;
    }
    input, button {
      width: 100%; padding: 10px; margin: 10px 0; border: none;
      border-radius: 5px;
    }
    button {
      background: #1e90ff; color: white; cursor: pointer;
    }
    a { color: #1e90ff; text-decoration: none; }
  </style>
</head>
<body>
  <div class="box">
    <h2>Login</h2>
    <form id="loginForm">
      <input type="email" id="email" placeholder="Email" required>
      <input type="password" id="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
    <a href="signup.html">Create account</a><br>
    <a href="http://localhost:5000/auth/google">Sign in with Google</a>
  </div>

  <script>
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const res = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (data.success) {
        localStorage.setItem("token", data.token);
        window.location.href = "index.html";
      } else {
        alert(data.msg);
      }
    });
  </script>
</body>
</html>
