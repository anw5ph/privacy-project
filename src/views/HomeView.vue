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
const cookies = ref([]);

function processURL() {
  resetValues();
  if (url.value != "") {
    isLoading.value = true; // Start loading
    try {
      const fccUrl = new URL(url.value);
      usesHttps.value = checkHttps(fccUrl);
      fetch('http://127.0.0.1:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: fccUrl })
      })
        .then(res => res.json())
        .then((result) => {
          cookies.value = result['cookies'];
          processCookies();
          dataProcessed.value = true;
        })
        .catch(error => {
          console.error("Error: ", error);
        })
        .finally(() => {
          isLoading.value = false; // Stop loading
        });
    } catch (err) {
      console.log(err)
      isError.value = true;
      errorMessage.value = "Invalid URL!";
      isLoading.value = false; // Stop loading
    }
  }
}

function processCookies() {
  var data = [{
    values: [19, 26, 55],
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
        <button type="button" class="btn btn-primary" @click="processURL">
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
      <div>
        <b>URL:</b> {{ url }}
        <b>Total Cookies: </b> 0
      </div>
      <table class="table table-striped">
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
          <tr v-for="(cookie,index) in cookies" :key="cookie">
            <th scope="row">{{ parseInt(index) + 1  }}</th>
            <td>{{ cookie['name'] }}</td>
            <td>{{ cookie['domain'] }}</td>
            <td>{{ cookie['path'] }}</td>
            <td>{{ cookie[''] }}</td>
            <td>{{ cookie['secure'] }}</td>
          </tr>
        </tbody>
      </table>
      <div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
    </div>
  </div>
</template>

<style>
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