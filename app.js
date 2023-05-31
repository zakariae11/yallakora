const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const ejs = require('ejs');

const app = express();
const port = 3000;

// Connect to MongoDB
MongoClient.connect('mongodb://localhost:27017', {
    useUnifiedTopology: true
})
    .then(client => {
        const db = client.db('yallakora');
        const collection = db.collection('matches_details');

        app.set('view engine', 'ejs');

        // Define a route to fetch and display the data
        app.get('/', (req, res) => {
            collection.find().toArray()
                .then(matches => {
                    res.render('index', { matches });
                })
                .catch(error => {
                    console.error('An error occurred:', error);
                    res.send('An error occurred.');
                });
        });

        // Start the server
        app.listen(port, () => {
            console.log(`Server running on port ${port}`);
        });
    })
    .catch(error => {
        console.error('Failed to connect to MongoDB:', error);
    });
