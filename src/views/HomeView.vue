<script setup>
import { ref, computed } from 'vue';
import searchSVG from '../assets/icons/search.svg';
import loadingSVG from '../assets/icons/loading.svg';
import Plotly from 'plotly.js-dist'

const url = ref('');
const errorMessage = ref('');
const isError = ref(false);
const usesHttps = ref(false);
const dataProcessed = ref(false);
const isLoading = ref(false); // New loading state variable
const firstPartyCookies = ref([]);
const firstPartyCookiesLength = ref(0);
const thirdPartyCookies = ref([]);
const thirdPartyCookiesLength = ref(0);
const cookiesScore = ref(0);
const httpScore = ref(0);
const totalScore = ref(0);
const safety = ref('');

const safetyClass = computed(() => {
  if (safety.value === "Your site has a low privacy score") return 'red-text';
  else if (safety.value === "Your site has a moderate privacy score") return 'yellow-text';
  else if (safety.value === "Your site has a high privacy score") return 'green-text';
  return ''; // default class if none of the conditions are met
});


async function processURL() {
  resetValues();
  if (url.value != "") {
    isLoading.value = true; // Start loading
    try {
      const fccUrl = new URL(url.value);
      usesHttps.value = checkHttps(fccUrl);

      // Fetch for getting cookies
      const getCookiesResponse = await fetch('http://127.0.0.1:3001/api/getCookies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ requestedUrl: fccUrl })
      });

      const cookieData = await getCookiesResponse.json();
      firstPartyCookies.value = cookieData['firstPartyCookies'];
      thirdPartyCookies.value = cookieData['thirdPartyCookies'];
      firstPartyCookiesLength.value = cookieData['firstPartyCookiesLength'];
      thirdPartyCookiesLength.value = cookieData['thirdPartyCookiesLength'];

      calculateAverageScore(firstPartyCookiesLength.value, thirdPartyCookiesLength.value);
      processCookies();

      // Fetch for storing cookies
      const storeCookiesResponse = await fetch('http://127.0.0.1:3001/api/storeCookies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          requestedUrl: fccUrl, 
          cookiesScore: cookiesScore.value, 
          httpScore: httpScore.value, 
          totalScore: totalScore.value
        })
      });

      const storeResponse = await storeCookiesResponse.json();
      console.log(storeResponse['message']);
      dataProcessed.value = true;

    } catch (err) {
      console.error(err);
      isError.value = true;
      errorMessage.value = "Invalid URL!";
    } finally {
      isLoading.value = false; // Stop loading
    }
  }
}

function getCookieScore(cookies) {
    if (cookies >= 50) return 0;
    if (cookies >= 46) return 1;
    if (cookies >= 41) return 2;
    if (cookies >= 36) return 3;
    if (cookies >= 31) return 4;
    if (cookies >= 26) return 5;
    if (cookies >= 21) return 6;
    if (cookies >= 16) return 7;
    if (cookies >= 11) return 8;
    if (cookies >= 6) return 9;
    if (cookies <= 5) return 10;
}

function calculateAverageScore(firstPartyCookies, thirdPartyCookies) {
    const firstPartyScore = getCookieScore(firstPartyCookies);
    const thirdPartyScore = getCookieScore(thirdPartyCookies);

    const weightedAverage = (firstPartyScore/10 * 0.3) + (thirdPartyScore/10 * 0.7);
    cookiesScore.value = weightedAverage;

    if(usesHttps.value){
      httpScore.value = 1;
    }
    else{
      httpScore.value = 0;
    }

    totalScore.value = httpScore.value + cookiesScore.value;
    if(totalScore.value >= 0 && totalScore.value < 2/3){
      safety.value = "Your site has a low privacy score";
    }
    else if(totalScore.value >= 2/3 && totalScore.value < 4/3){
      safety.value = "Your site has a moderate privacy score";
    }
    else{
      safety.value = "Your site has a high privacy score";
    }
}

function processCookies() {
  var data = [{
    values: [(firstPartyCookiesLength.value) / (firstPartyCookiesLength.value + thirdPartyCookiesLength.value), (thirdPartyCookiesLength.value) / (firstPartyCookiesLength.value + thirdPartyCookiesLength.value)],
    labels: ['First-Party Cookies', 'Third-Party Cookies'],
    type: 'pie'
  }];

  var config = {responsive: true}

  var layout = {
    // height: 400,
    // width: 500
  };

  var data2;

  if (totalScore.value >= 0 && totalScore.value < 2/3) {
    data2 = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: totalScore.value,
      title: { text: "Privacy Score" },
      type: "indicator",
      mode: "gauge+number",
      gauge: {
        axis: { range: [null, 2] },
        bar: { 
          color: "red",
          thickness: 1,
        },
        steps: [
          {range: [0, 2], color: "lightgrey"}
        ],
      }
    }
    ];
  }
  else if (totalScore.value >= 2/3 && totalScore.value < 4/3) {
    data2 = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: totalScore.value,
      title: { text: "Privacy Score" },
      type: "indicator",
      mode: "gauge+number",
      gauge: {
        axis: { range: [null, 2] },
        bar: { 
          color: "yellow",
          thickness: 1,
        },
        steps: [
          {range: [0, 2], color: "lightgrey"}
        ],
      }
    }
    ];
  }
  else {
    data2 = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: totalScore.value,
      title: { text: "Privacy Score" },
      type: "indicator",
      mode: "gauge+number",
      gauge: {
        axis: { range: [null, 2] },
        bar: { 
          color: "green",
          thickness: 1,
        },
        steps: [
          {range: [0, 2], color: "lightgrey"}
        ],
      }
    }
    ];
  }

  var layout2 = { margin: { t: 0, b: 0 } };
  var config2 = {responsive: true}

  setTimeout(() => {
    Plotly.newPlot('myDiv', data, layout, config);
    Plotly.newPlot('myDiv2', data2, layout2, config2);
  }, 100); // Delay of 100 milliseconds
}

function checkHttps(fccUrl) {
  if (fccUrl.protocol === "https:") {
    return true;
  }
  return false;
}

function resetValues() {
  isError.value = false;
  dataProcessed.value = false;
  usesHttps.value = false;
  totalScore.value = 0;
  cookiesScore.value = 0;
  httpScore.value = 0;
}
</script>

<template>
  <div class="container">
    <div class="header">
      <h1 class="title">URL Privacy Score Generator</h1>
      <RouterLink class="link" to="rankings" :class="{ disabled: isLoading}" >
        <button type="button" :disabled="isLoading" class="btn btn-primary" id="ranking-button">
          Rankings
        </button>
      </RouterLink>
      <div class="input-div">
        <input type="text" id="search" class="form-control" v-model="url" placeholder="Enter your URL here" @keyup.enter="processURL">
        &nbsp;<button type="button" class="btn btn-primary" @click="processURL" :disabled="isLoading">
          <searchSVG />
        </button>
      </div>
    </div>
    <div class="error-message" v-if="isError">{{ errorMessage }}</div>
    <div v-if="isLoading" class="loading-screen">
      Scanning URL
      <loadingSVG />
    </div>
    <div v-if="dataProcessed" class="data">
      <div class="top-row">
        <div class="box">
          <div class="info">
            <b>Total Cookies: </b> {{ firstPartyCookiesLength + thirdPartyCookiesLength}} <br>
            <b>Uses Https: </b> {{ usesHttps }}
          </div>
        <div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
      </div>
      <div class="box2">
        <div class="score-info">
          <h3 class="score-info-text" :class="safetyClass">{{ safety }}</h3>
        </div>
        <div id='myDiv2'><!-- Plotly chart will be drawn inside this DIV --></div>
      </div>
      </div>
      <table class="table table-striped" id="tableCSS">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Cookie Name</th>
            <th scope="col">Domain</th>
            <th scope="col">Path</th>
            <th scope="col">Cookie Type</th>
            <th scope="col">Secure</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cookie,index) in firstPartyCookies" :key="cookie">
            <th scope="row">{{ parseInt(index) + 1  }}</th>
            <td>{{ cookie['name'] }}</td>
            <td>{{ cookie['domain'] }}</td>
            <td>{{ cookie['path'] }}</td>
            <td>{{"First-party" }}</td>
            <td>{{ cookie['secure'] }}</td>
          </tr>
          <tr v-for="(cookie,index) in thirdPartyCookies" :key="cookie">
            <th scope="row">{{ parseInt(index) + 1  }}</th>
            <td>{{ cookie['name'] }}</td>
            <td>{{ cookie['domain'] }}</td>
            <td>{{ cookie['path'] }}</td>
            <td>{{"Third-party" }}</td>
            <td>{{ cookie['secure'] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.disabled {
  opacity: 0.5;
  pointer-events: none;
}
.red-text { color: red; }
.yellow-text { color: #FDDA0D; }
.green-text { color: green; }

.score-info-text{
  font-size: 15px;
}
.score-info{
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}

#ranking-button{
  margin-bottom: 10px;
}
.top-row{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.info{
  margin-left: 10px;
}
#tableCSS{
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
}
.box2{
  display: flex;
  flex-direction: column;
  width: 49%;
  height: auto;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  margin-bottom: 15px;
}
.box{
  width: 49%;
  height: auto;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  margin-bottom: 15px;
}
#search{
  width: 400px;
}
.header{
  background-color: lightblue;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  margin-bottom: 10px;
}
.title{
  margin-top: 20px;
}
.data {
  width: 100%;
}

.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

.input-div {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.error-message {
  color: red;
}

.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>