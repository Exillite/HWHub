const express = require("express");
// import express from 'express';

const app = express();
const port = 9966;

// Serve static files from the "src" directory
app.use('/call', express.static("src"));
app.use('/call/sp', express.static(__dirname + '/node_modules/simple-peer'));

// Define your routes
app.get("/call", (req, res) => {
    res.sendFile(__dirname + "/src/index.html");
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});