const express = require("express");
const router = express.Router();

// Third Party Import
const { validationResult } = require("express-validator");

// Project Imports
const Transaction = require("../Models/Transaction");
const {
  createTransactionValidation,
} = require("../middleware/validation/transaction");

const { authMiddleware } = require("../middleware/authenticate");

// -------------------------------------------|| CREATE ||-------------------------------------------
router.post(
  "/",
  createTransactionValidation,
  authMiddleware,
  async (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const existTransaction = await Transaction.findOne({
        category: req.body.category,
        transactionType: req.body.transactionType,
        amount: req.body.amount,
        transactionDate: req.body.transactionDate,
        description: req.body.description,
        beneficiary: req.body.beneficiary,
        status: req.body.transactionStatus,
        mode: req.body.transactionMode,
        createdBy: req.user._id,
      });
      if (existTransaction) {
        return res
          .status(409)
          .json({ error: "A similar transaction already exists." });
      }
      const transaction = new Transaction({
        ...req.body,
        createdBy: req.user._id, // Use user ID from token
      });
      await transaction.save();
      res.status(201).json(transaction);
    } catch (err) {
      console.error(err);
      // Check for unique constraint error and return appropriate response
      next(err); // Pass the error to the error handling middleware
    }
  }
);

// -------------------------------------------|| GET ||-------------------------------------------
router.get("/", authMiddleware, async (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    // Apply optional filters
    const query = {
      isDeleted: req.query?.transactionStatus !== undefined,
      createdBy: req.user._id, // Fetch transactions created by the authenticated user
    };

    // If currentMonth is true, add the current month filter
    if (req.query?.currentMonth) {
      const now = new Date(new Date().getTime() + 330 * 60 * 1000);
      const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      const endOfMonth = new Date(
        now.getFullYear(),
        now.getMonth() + 1,
        0,
        23,
        59,
        59
      );

      query["transactionDate"] = {
        $gte: startOfMonth,
        $lte: endOfMonth,
      };
    }
    const transactions = await Transaction.find(query, {
      isDeleted: 0,
      createdBy: 0,
      deletedAt: 0,
    }).sort({ transactionDate: -1 });
    const summary = {
      balance: 0,
      expense: 0,
      income: 0,
      previousPending: 0,
      pending: 0,
      paid: 0,
      emi: 0,
      investment: 0,
    };
    for (let transaction of transactions) {
      if (transaction.transactionType === "income") {
        summary.balance += transaction.amount;
        summary.income += transaction.amount;
      } else {
        summary.balance -= transaction.amount;
        summary.expense += transaction.amount;
        if (transaction.status?.toLowerCase() === "pending") {
          summary.pending += transaction.amount;
        } else if (transaction.status?.toLowerCase() === "completed") {
          summary.paid += transaction.amount;
        }
      }
      if (transaction.category.toLowerCase() === "emi") {
        summary.emi += transaction.amount;
      } else if (transaction.category.toLowerCase() === "investment") {
        summary.investment += transaction.amount;
      }
    }
    res.status(200).json({ transactions, summary });
  } catch (err) {
    console.error(err);
    next(err); // Pass the error to the error handling middleware
  }
});

// -------------------------------------------|| PUT ||-------------------------------------------

router.put(
  "/",
  createTransactionValidation,
  authMiddleware,
  async (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const query = {
        _id: req.query.id, // Only fetch transactions with a true status
        createdBy: req.user._id, // Fetch transactions created by the authenticated user
      };
      const existTransaction = await Transaction.findOneAndUpdate(query, {
        category: req.body.category,
        transactionType: req.body.transactionType,
        amount: req.body.amount,
        transactionDate: req.body.transactionDate,
        description: req.body.description,
        beneficiary: req.body.beneficiary,
        status: req.body.status,
        mode: req.body.mode,
      });
      if (!existTransaction) {
        return res.status(409).json({ error: "No Transaction Found" });
      }

      res.status(201).json(existTransaction);
    } catch (err) {
      console.error(err);
      // Check for unique constraint error and return appropriate response
      next(err); // Pass the error to the error handling middleware
    }
  }
);

// -------------------------------------------|| DELETE ||-------------------------------------------
router.delete("/", authMiddleware, async (req, res, next) => {
  try {
    const query = {
      _id: req.query.id, // Only fetch transactions with a true status
      createdBy: req.user._id, // Fetch transactions created by the authenticated user
    };
    const istTime = new Date();
    const istOffset = 330; // IST offset in minutes (5 hours and 30 minutes)
    const now = new Date(istTime.getTime() + istOffset * 60 * 1000);

    await Transaction.updateOne(
      query,
      {
        transactionStatus: req.query?.transactionStatus,
        transactionStausUpdate: now,
      },
      {
        transactionStatus: 0,
        createdBy: 0,
        transactionStausUpdate: 0,
      }
    );
    res.status(200).json({ message: "Transaction Deleted" });
  } catch (err) {
    console.error(err);
    next(err); // Pass the error to the error handling middleware
  }
});

module.exports = router;
