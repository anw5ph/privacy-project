const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const puppeteer = require('puppeteer');

const app = express();
const port = 3001;

app.use(cors());
// Middleware to parse JSON in the request body
app.use(bodyParser.json());

// Endpoint to handle the POST request
app.post('/api/getCookies', async (req, res) => {
  // Access the requestedUrl from the request body
  const requestedUrl = req.body.requestedUrl;
  firstPartyCookies = {};
  thirdPartyCookies = {};

  // Do something with the requestedUrl, for example, log it
  console.log('Requested URL:', requestedUrl);
  try {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(requestedUrl, { waitUntil: 'domcontentloaded' });

    await delay(20000);
  
    // Access and log cookies
    const client = await page.target().createCDPSession();
    const all_browser_cookies = (await client.send('Network.getAllCookies')).cookies;
    const first_party_cookies = await page.cookies();
    var i = 0;
    firstPartyCookies = first_party_cookies.reduce((acc, cookie) => {
      acc[i] = cookie;
      i += 1;
      return acc;
    }, {});

    const firstPartyDomains = first_party_cookies.map(cookie => cookie.domain);
    thirdPartyCookies = all_browser_cookies.reduce((acc, cookie) => {
      if (!firstPartyDomains.includes(cookie.domain)) {
        acc[i] = cookie;
        i += 1;
      }
      return acc;
    }, {});
  
    await browser.close();
  } catch (error) {
    console.log(error);
  }
  res.json({firstPartyCookies, thirdPartyCookies, "firstPartyCookiesLength": Object.keys(firstPartyCookies).length, "thirdPartyCookiesLength": Object.keys(thirdPartyCookies).length});
});

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:${port}`);
});
