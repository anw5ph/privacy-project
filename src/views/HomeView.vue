<script setup>
import { ref } from 'vue';
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

async function processURL() {
  resetValues();
  if (url.value != "") {
    isLoading.value = true; // Start loading
    try {
      const fccUrl = new URL(url.value);
      usesHttps.value = checkHttps(fccUrl);

      await fetch('http://127.0.0.1:3001/api/getCookies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ requestedUrl: fccUrl })
      })
        .then(res => res.json())
        .then((result) => {
          firstPartyCookies.value = result['firstPartyCookies'];
          thirdPartyCookies.value = result['thirdPartyCookies'];
          firstPartyCookiesLength.value = result['firstPartyCookiesLength'];
          thirdPartyCookiesLength.value = result['thirdPartyCookiesLength'];

          processCookies();
          dataProcessed.value = true;
        })
        .catch(error => {
          console.error("Error: ", error);
        })
        
    } catch (err) {
      console.error(err);
      isError.value = true;
      errorMessage.value = "Invalid URL!";
      isLoading.value = false; // Stop loading
    } finally {
      isLoading.value = false; // Stop loading
    }
  }
}

function processCookies() {
  var data = [{
    values: [(firstPartyCookiesLength.value) / (firstPartyCookiesLength.value + thirdPartyCookiesLength.value), (thirdPartyCookiesLength.value) / (firstPartyCookiesLength.value + thirdPartyCookiesLength.value)],
    labels: ['First-Party Cookies', 'Third-Party Cookies'],
    type: 'pie'
  }];

  var layout = {
    height: 400,
    width: 500
  };

  setTimeout(() => {
    Plotly.newPlot('myDiv', data, layout);
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
}
</script>

<template>
  <div class="container">
    <div class="header">
      <h1 class="title">URL Privacy Score Generator</h1>
      <div class="input-div">
        <input type="text" id="search" class="form-control" v-model="url" placeholder="Enter your URL here" @keyup.enter="processURL">
        &nbsp;<button type="button" class="btn btn-primary" @click="processURL" :disabled="isLoading">
          <searchSVG />
        </button>
      </div>
      <RouterLink to="rankings">
        <button type="button" class="btn btn-primary" id="ranking-button">Rankings</button>
      </RouterLink>
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

<style>
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
  margin-bottom: 20px;
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