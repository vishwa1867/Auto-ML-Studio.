const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const session = require("express-session");
const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;

const app = express();
app.use(cors({ origin: "http://localhost:5173", credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ✅ MongoDB Connection
mongoose.connect("mongodb://127.0.0.1:27017/aspDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.error("❌ MongoDB Error:", err));

// ✅ User Schema
const userSchema = new mongoose.Schema({
  email: { type: String, unique: true },
  password: String,
  googleId: String,
});
const User = mongoose.model("User", userSchema);

// ✅ JWT Secret
const JWT_SECRET = "super_secret_key"; // change this
const FRONTEND_URL = "http://localhost:5173";

// ---------- SIGNUP ----------
app.post("/api/signup", async (req, res) => {
  const { email, password } = req.body;
  try {
    const hashed = await bcrypt.hash(password, 10);
    const newUser = new User({ email, password: hashed });
    await newUser.save();
    res.json({ success: true, msg: "User created ✅", redirect: FRONTEND_URL + "/login" });
  } catch (err) {
    res.status(400).json({ success: false, msg: "Email already exists ❌" });
  }
});

// ---------- LOGIN ----------
app.post("/api/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });

  if (!user) return res.status(400).json({ success: false, msg: "User not found ❌" });

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) return res.status(400).json({ success: false, msg: "Invalid password ❌" });

  const token = jwt.sign({ id: user._id, email: user.email }, JWT_SECRET, { expiresIn: "1h" });

  res.json({ success: true, token, redirect: FRONTEND_URL + "/home" });
});

// ✅ Middleware for protected routes
function authMiddleware(req, res, next) {
  const token = req.headers["authorization"];
  if (!token) return res.status(401).json({ msg: "No token" });

  try {
    const decoded = jwt.verify(token.split(" ")[1], JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ msg: "Invalid token" });
  }
}

// ---------- HOME ----------
app.get("/api/home", authMiddleware, (req, res) => {
  res.json({ success: true, msg: `Welcome ${req.user.email} 🎉` });
});

// ---------- Google OAuth ----------
app.use(session({ secret: "google_secret", resave: false, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());

passport.use(new GoogleStrategy({
  clientID: "YOUR_GOOGLE_CLIENT_ID",
  clientSecret: "YOUR_GOOGLE_CLIENT_SECRET",
  callbackURL: "http://localhost:5000/auth/google/callback",
}, async (accessToken, refreshToken, profile, done) => {
  let user = await User.findOne({ googleId: profile.id });
  if (!user) {
    user = new User({ googleId: profile.id, email: profile.emails[0].value });
    await user.save();
  }
  return done(null, user);
}));

passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
  const user = await User.findById(id);
  done(null, user);
});

app.get("/auth/google", passport.authenticate("google", { scope: ["profile", "email"] }));
app.get("/auth/google/callback",
  passport.authenticate("google", { failureRedirect: FRONTEND_URL + "/login" }),
  (req, res) => {
    res.redirect(FRONTEND_URL + "/home");
  }
);

// ---------- Start ----------
app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));
