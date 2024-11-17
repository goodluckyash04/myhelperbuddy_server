const mongoose = require("mongoose");
const { Schema } = mongoose;
const { getCurrentIST } = require("../middleware/utility");
const User = require("./User");

const financialProductSchema = new Schema(
  {
    // Name of the financial product
    name: {
      type: String,
      maxlength: 100,
      required: true,
    },

    type: {
      type: String,
      maxlength: 100,
      required: true,
    },

    amount: {
      type: Number,
      default: 0.0,
      required: true,
    },

    noOfInstallments: {
      type: Number,
      default: 0,
    },

    startedOn: {
      type: Date,
      required: true,
    },

    status: {
      type: String,
      enum: ["Open", "Closed"],
      default: "Open",
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

    // Reference to the user who created the financial product
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

// Middleware to convert timestamps to IST
financialProductSchema.pre("save", function (next) {
  if (this.isNew) {
    this.createdAt = getCurrentIST(new Date());
    this.startedOn = getCurrentIST(this.startedOn);
  }
  this.updatedAt = getCurrentIST(new Date());
  next();
});

financialProductSchema.pre("findOneAndUpdate", function (next) {
  this.set({ updatedAt: getCurrentIST(new Date()) });
  next();
});

// Create and export the FinancialProduct model
const FinancialProduct = mongoose.model(
  "FinancialProduct",
  financialProductSchema
);
module.exports = FinancialProduct;
