const jwt = require("jsonwebtoken");

const User = require("../Models/User"); // Your User model

SECRET_KEY = process.env.SECRET_KEY;

// generate access token
const generateToken = (user) =>
  jwt.sign(
    { userId: user._id, email: user.email, username: user.userId },
    SECRET_KEY,
    { expiresIn: "5h" } // Token expires in one hour
  );

// decode access token
const authMiddleware = async (req, res, next) => {
  try {
    // Extract token and remove 'Bearer ' prefix
    const token = req.header("authorization")?.replace("Bearer ", "");
    if (!token) {
      return res.status(401).json({ error: "No token provided." });
    }

    // Verify the token and catch specific errors
    let decoded;
    try {
      decoded = jwt.verify(token, SECRET_KEY);
    } catch (err) {
      if (err.name === "TokenExpiredError") {
        return res.status(401).json({ error: "Token has expired." });
      }
      return res.status(401).json({ error: "Invalid token." });
    }

    // Find user based on the userId from the token
    const user = await User.findById(decoded.userId, { password: 0 }); // Exclude sensitive fields
    if (!user) {
      return res.status(404).json({ error: "User not found." });
    }

    req.user = user; // Attach user to request object
    next(); // Call the next middleware/route handler
  } catch (error) {
    console.error("Error validating token:", error);
    res.status(500).json({ error: "Internal server error." });
  }
};

module.exports = { authMiddleware, generateToken };
