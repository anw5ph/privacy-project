const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');

const app = express();
const port = 3002;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/storeCookies', async (req, res) => {

    // Create a backup of the data.json file before modifying
    fs.copyFileSync('data.json', 'backup.json');

    const requestedUrl = req.body.requestedUrl;
    const cookiesScore = req.body.cookiesScore;
    const httpScore = req.body.httpScore;
    const totalScore = req.body.totalScore;

    const rawData = fs.readFileSync('data.json');
    const jsonData = JSON.parse(rawData);

    const newData = {
        "url": requestedUrl,
        "httpsScore": httpScore,
        "cookieScore": cookiesScore,
        "overallScore": totalScore
    };

    const lastIndex = Object.keys(jsonData).length > 0 ? Math.max(...Object.keys(jsonData).map(Number)) : -1;
    jsonData[lastIndex + 1] = newData;

    fs.writeFileSync('data.json', JSON.stringify(jsonData, null, 2), 'utf-8');
    console.log("Succesfully stored cookie scoring data for " + requestedUrl + ".");
    res.json({message: "Succesfully stored cookie scoring data for " + requestedUrl + "."});
  
});
// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:${port}`);
});
