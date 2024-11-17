const { body } = require("express-validator");

const createTransactionValidation = [
  body("amount").isFloat().withMessage("Amount must be a positive number"),
];

module.exports = {
  createTransactionValidation,
};
