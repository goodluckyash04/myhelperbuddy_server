const mongoose = require("mongoose");
const { Schema } = mongoose;
const { getCurrentIST } = require("../middleware/utility");
const User = require("./User");

const transactionSchema = new Schema(
  {
    // Enum field to represent type of transaction (e.g., income, expense)
    transactionType: {
      type: String,
      required: true,
      enum: ["income", "expense"],
    },

    category: {
      type: String,
      required: true,
    },

    transactionDate: {
      type: Date,
      required: true,
    },

    amount: {
      type: Number,
      default: 0.0,
      required: true,
    },

    beneficiary: {
      type: String,
      maxlength: 100,
    },

    description: {
      type: String,
      maxlength: 255,
    },

    // Foreign key to FinancialProduct
    source: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "FinancialProduct",
      default: null,
    },

    status: {
      type: String,
      default: "Pending",
    },

    mode: {
      type: String,
      default: null,
    },

    // Soft delete fields
    isDeleted: {
      type: Boolean,
      default: false,
    },
    deletedAt: {
      type: Date,
      default: null,
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

// Middleware to adjust timestamps to IST
transactionSchema.pre("save", function (next) {
  if (this.isNew) {
    this.createdAt = getCurrentIST(new Date());
    this.transactionDate = getCurrentIST(this.transactionDate);
  }
  this.updatedAt = getCurrentIST(new Date());
  next();
});

transactionSchema.pre("findOneAndUpdate", function (next) {
  this.set({ updatedAt: getCurrentIST(new Date()) });
  next();
});

// Create and export the Transaction model
const Transaction = mongoose.model("Transaction", transactionSchema);
module.exports = Transaction;
