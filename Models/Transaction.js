const mongoose = require("mongoose");
const { Schema } = mongoose;
const { getCurrentIST } = require("../middleware/utility");
// Reference to User model (assuming it's defined elsewhere)
const User = require("./User");

// Define the Transaction schema
const transactionSchema = new Schema(
  {
    // Specifies the Category of the transaction (e.g., Food, Rent)
    category: {
      type: String,
      enum: [
        "food",
        "shopping",
        "emi",
        "investment",
        "salary",
        "general",
        "other",
      ],
      default: "general",
    },

    // Specifies the type of transaction (e.g., expense, income, etc.)
    transactionType: {
      type: String,
      enum: ["income", "expense"],
      default: "expense",
      required: true,
    },

    // Date when the transaction occurred
    transactionDate: {
      type: Date,
      required: true,
    },

    // The monetary amount of the transaction
    amount: {
      type: Number,
      default: 0.0,
      required: true,
    },

    // The person or entity benefiting from the transaction
    beneficiary: {
      type: String,
      maxlength: 50,
    },

    // Additional information about the transaction
    description: {
      type: String,
      maxlength: 150,
    },

    // changes the delete status based
    transactionStatus: {
      type: Boolean,
      default: true,
    },

    transactionStausUpdate: {
      type: Date,
    },

    // Reference to the user who created the transaction
    createdBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
  },
  {
    timestamps: true, // Automatically adds `createdAt` and `updatedAt`
  }
);

// Convert UTC to IST using a pre-save middleware
transactionSchema.pre("save", function (next) {
  if (this.isNew) {
    this.createdAt = getCurrentIST(new Date());
    this.transactionDate = getCurrentIST(this.transactionDate);
    // Set createdAt in IST
  }

  this.updatedAt = getCurrentIST(new Date()); // Always update updatedAt in IST
  next();
});

// Create and export the Transaction model
const Transaction = mongoose.model("Transaction", transactionSchema);
module.exports = Transaction;
