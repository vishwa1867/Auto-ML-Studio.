// backend/routes/csvRoute.js
const express = require("express");
const { spawn } = require("child_process");
const multer = require("multer");
const path = require("path");

const router = express.Router();
const upload = multer({ dest: "uploads/" });

router.post("/analyze", upload.single("file"), (req, res) => {
  const filePath = path.resolve(req.file.path);

  const py = spawn("python", ["x.py", filePath]);

  let data = "";
  py.stdout.on("data", (chunk) => {
    data += chunk.toString();
  });

  py.stderr.on("data", (err) => {
    console.error("Python error:", err.toString());
  });

  py.on("close", () => {
    try {
      const result = JSON.parse(data);
      res.json(result);
    } catch (e) {
      res.status(500).json({ error: "Failed to parse Python output" });
    }
  });
});

module.exports = router;
