const express = require('express');
const MongoClient = require('mongodb').MongoClient;

const app = express();
const port = 3000;

// MongoDB connection URL
const url = 'mongodb://localhost:27017';
const dbName = 'yallakora';

// API endpoint to retrieve the match details
app.get('/matches', (req, res) => {
    MongoClient.connect(url, (err, client) => {
        if (err) {
            console.error('Error connecting to MongoDB:', err);
            res.status(500).json({ error: 'An error occurred' });
            return;
        }

        const db = client.db(dbName);
        const collection = db.collection('matches_details');

        collection.find().toArray((err, docs) => {
            if (err) {
                console.error('Error retrieving data from MongoDB:', err);
                res.status(500).json({ error: 'An error occurred' });
                return;
            }

            res.json(docs);
        });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});
