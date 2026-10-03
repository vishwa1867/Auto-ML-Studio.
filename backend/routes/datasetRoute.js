const express = require("express");
const router = express.Router();
const multer = require("multer");
const upload = multer({ dest: "uploads/" });

router.post("/insights", upload.single("file"), (req, res) => {
    console.log("✅ File received:", req.file);
    console.log("✅ Body received:", req.body);

    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    res.json({ message: "File successfully uploaded!", file: req.file });
});

module.exports = router;
