// Third Party Imports
const bcrypt = require("bcrypt");

// Number of salt rounds for hashing passwords (consider higher for more security)
const SALT_ROUNDS = 10;

const toPascalCase = (str) => {
  return str
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
};

// to ensure no spaces in the password
const noSpaces = (str) => !/\s/.test(str); // Returns true if no spaces are found

// create hashPassword
const hashPassword = (password) => {
  return bcrypt.hashSync(password, SALT_ROUNDS);
};

// verify hashPassword
const isMatch = (userPassword, hashPassword) =>
  bcrypt.compareSync(userPassword, hashPassword);

const getCurrentIST = (date) => {
  const istOffset = 5.5 * 60 * 60 * 1000; // IST is UTC +05:30
  const utcTime = date.getTime(); // Get time in milliseconds since epoch
  const istTime = utcTime + istOffset; // Convert UTC to IST
  console.log(new Date(istTime));
  return new Date(istTime); // Return the IST date
};

module.exports = {
  toPascalCase,
  hashPassword,
  noSpaces,
  isMatch,
  getCurrentIST,
};
