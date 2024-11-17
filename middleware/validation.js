const { check, body, query } = require("express-validator");

// registration validator
const validateUserRegistration = [
  check("firstName")
    .isLength({ min: 2, max: 50 })
    .withMessage("First name must be between 2 and 50 characters.")
    .matches(/^[a-zA-Z]+$/)
    .withMessage("First name should contain only alphabetical characters"),
  check("lastName")
    .isLength({ min: 2, max: 50 })
    .withMessage("Last name must be between 2 and 50 characters.")
    .matches(/^[a-zA-Z]+$/)
    .withMessage("Last name should contain only alphabetical characters"),
  check("userId")
    .isLength({ min: 3, max: 15 })
    .matches(/^[a-zA-Z0-9]+$/) // Allow only alphabets and digits
    .withMessage(
      "User ID must be alphanumeric and between 3 and 15 characters."
    ),
  check("email").isEmail().withMessage("Please enter a valid email address."),
  check("password")
    .isLength({ min: 8 })
    .matches(/^\S*$/) // Ensure no spaces
    .withMessage("Password must be at least 8 characters with no spaces."),
];

const signInValidation = [
  check("identifier").notEmpty().withMessage("Identifier is required."), // Identifier should not be empty
  check("password").notEmpty().withMessage("Identifier is required."), // Identifier should not be empty
];

module.exports = {
  validateUserRegistration,
  signInValidation,
};
