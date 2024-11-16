// Third Party Imports
const express = require("express");
const cors = require("cors");
const process = require("process");

// Project Imports
const connectToMongo = require("./db");
const port = process.env.PORT || 3000;

const app = express(); // Initialize Express instance

const corsOpts = {
  origin: "*", // Specific allowed origins
  methods: "*", // Allowed methods
  allowedHeaders: "*", // Allowed headers
};

// Middleware setup
app.use(cors(corsOpts));
app.use(express.json()); // Parse JSON bodies

// Import route handlers
const authRoutes = require("./Routes/auth");
const transactionRoutes = require("./Routes/transaction");
// const loanRoutes = require("./Routes/loan");
// const taskRoutes = require("./Routes/task");

// Route configuration
app.use("/goex/auth", authRoutes);
app.use("/goex/transaction", transactionRoutes);
// app.use("/goex/loan", loanRoutes);
// app.use("/goex/task", taskRoutes);

connectToMongo();

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Error occurred:", err); // Log the error details
  res.status(500).json({ message: "Internal server error" }); // Return a user-friendly message
});

// Start the server
app.listen(port, (error) => {
  if (!error) {
    console.log(`Server running on port ${port}`);
  } else {
    console.error("Error occurred, server can't start", error); // Log error
  }
});

// Signal handling for graceful shutdown
process.on("SIGINT", () => {
  console.log("Gracefully shutting down...");
  // Perform necessary cleanup tasks, such as closing database connections
  process.exit(0); // Exit with success
});
