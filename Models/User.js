const mongoose = require("mongoose");
const { Schema } = mongoose;
const {
  toPascalCase,
  hashPassword,
  noSpaces,
} = require("../middleware/utility");

// Define the User schema
const userSchema = new Schema(
  {
    firstName: {
      type: String,
      required: true,
      minlength: 2,
      maxlength: 50,
    },
    lastName: {
      type: String,
      required: true,
      minlength: 2,
      maxlength: 50,
    },
    userId: {
      type: String,
      required: true,
      unique: true,
      minlength: 3,
      maxlength: 15,
      match: /^[a-zA-Z0-9]+$/, // Allows only alphabets and digits
    },
    email: {
      type: String,
      required: true,
      unique: true,
      match: /.+@.+\..+/,
      index: true, // Index for faster querying
    },
    password: {
      type: String,
      required: true,
      minlength: 8,
      validate: {
        validator: noSpaces, // Validates that the password has no spaces
        message: "Password should not contain spaces.",
      },
    },
    role: {
      type: String,
      default: "user", // Default role
      enum: ["user", "admin", "moderator"], // List of allowed roles
    },
  },
  { timestamps: true } // Automatically adds createdAt and updatedAt fields
);

// Hash the password before saving
userSchema.pre("save", function (next) {
  this.userId = this.userId.toLowerCase(); // Convert username to lowercase
  this.email = this.email.toLowerCase(); // Convert email to lowercase
  this.firstName = toPascalCase(this.firstName); // Convert fname to PascalCase
  this.lastName = toPascalCase(this.lastName); // Convert lname to PascalCase
  if (this.isModified("password")) {
    this.password = hashPassword(this.password);
  }
  next();
});

const User = mongoose.model("User", userSchema); // PascalCase for model name
module.exports = User;
