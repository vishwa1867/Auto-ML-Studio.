const { MongoClient } = require("mongodb");

const uri = "mongodb://localhost:27017";

async function run() {
  const client = new MongoClient(uri);

  try {
    await client.connect();
    console.log("✅ Connected to MongoDB");

    const db = client.db("myAppDB");
    const users = db.collection("users");

    const result = await users.insertOne({
      name: "Vishwa",
      role: "Backend Dev",
      active: true
    });
    console.log("Inserted ID:", result.insertedId);

    const user = await users.findOne({ name: "Vishwa" });
    console.log("Found User:", user);

  } finally {
    await client.close();
  }
}

run().catch(console.dir);
