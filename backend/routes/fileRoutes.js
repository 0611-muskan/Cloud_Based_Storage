const express = require("express");
const multer = require("multer");
const s3 = require("../aws");
const { randomUUID } = require("crypto");

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

// Upload (USER-SPECIFIC)
router.post("/upload", upload.single("file"), async (req, res) => {
  const file = req.file;
  const email = req.body.email;

  if (!email) {
    return res.status(400).json({ message: "Email required" });
  }

  const params = {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: `${email}/${randomUUID()}-${file.originalname}`, // ✅ folder
    Body: file.buffer
  };

  try {
    const data = await s3.upload(params).promise();
    res.json({ url: data.Location });
  } catch (err) {
    res.status(500).json(err);
  }
});

// List files (USER-SPECIFIC)
router.get("/", async (req, res) => {
  const email = req.query.email;

  if (!email) {
    return res.status(400).json({ message: "Email required" });
  }

  const params = {
    Bucket: process.env.AWS_BUCKET_NAME,
    Prefix: `${email}/` // ✅ filter user
  };

  try {
    const data = await s3.listObjectsV2(params).promise();
    res.json(data.Contents || []);
  } catch (err) {
    res.status(500).json(err);
  }
});

// Delete
router.delete("/:key", async (req, res) => {
  const params = {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: req.params.key
  };

  try {
    await s3.deleteObject(params).promise();
    res.json({ message: "Deleted" });
  } catch (err) {
    res.status(500).json(err);
  }
});

// Share
router.get("/share/:key", async (req, res) => {
  const params = {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: req.params.key,
    Expires: 60
  };

  try {
    const url = s3.getSignedUrl("getObject", params);
    res.json({ url });
  } catch (err) {
    res.status(500).json(err);
  }
});

module.exports = router;