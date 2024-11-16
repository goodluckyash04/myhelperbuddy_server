const express = require("express");
const router = express.Router();

// Third Party Import
const { validationResult } = require("express-validator");

// Project Imports
const User = require("../Models/User.js");
const {
  validateUserRegistration,
  signInValidation,
} = require("../middleware/validation");
const { isMatch } = require("../middleware/utility");
const { authMiddleware, generateToken } = require("../middleware/authenticate");

// -------------------------------------------|| REGISTER ||-------------------------------------------

router.post("/register", validateUserRegistration, async (req, res) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    // Return validation errors if any
    return res.status(422).json({ errors: errors.array() });
  }

  const { firstName, lastName, userId, email, password } = req.body;

  // Check if email or userId already exists
  const existingUser = await User.findOne({
    $or: [{ email: email.toLowerCase() }, { userId: userId.toLowerCase() }],
  });
  if (existingUser) {
    return res.status(409).json({ error: "Email or User ID already exists" });
  }

  // Create a new user
  const user = new User({
    firstName,
    lastName,
    userId,
    email,
    password,
  });

  try {
    await user.save();
    res.status(201).json({ message: "User registered successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// -------------------------------------------|| SIGN-IN ||-------------------------------------------

router.post("/signin", signInValidation, async (req, res) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    // Return validation errors if any
    return res.status(422).json({ errors: errors.array() });
  }
  const { identifier, password } = req.body;

  try {
    // Find user by either email or username
    const user = await User.findOne({
      $or: [
        { email: identifier.toLowerCase() },
        { userId: identifier.toLowerCase() },
      ],
    });

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // Check if the provided password matches the stored hashed password
    const isPasswordMatch = isMatch(password, user.password);

    if (!isPasswordMatch) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    // Create a JWT token upon successful authentication
    const token = generateToken(user);

    res.json({ message: "Login successful", token });
  } catch (error) {
    res.status(500).json({ error: "Internal Server Error" });
  }
});

module.exports = router;
