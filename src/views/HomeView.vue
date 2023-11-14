<script setup>
import { ref } from 'vue';
import searchSVG from '../assets/icons/search.svg';

const url = ref('');
const errorMessage = ref('');
const isError = ref('');
const usesHttps = ref(false);
const dataProcessed = ref(false);
const cookies = ref('');

function processURL() {
  resetValues();
  if(url.value != ""){
    try {
      const fccUrl = new URL(url.value);
      usesHttps.value = checkHttps(fccUrl); 


      dataProcessed.value = true;

      fetch('http://127.0.0.1:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: fccUrl })
      })
      .then(res => res.json())
      .then( (result) => {
        cookies.value = result['cookies']
        // console.log(result);
      })
      .catch( error => {
        console.error("Error: ", error);
      })
    } catch (err) {
      console.log(err)
      isError.value = true;
      dataProcessed.value = false;
      errorMessage.value = "Invalid URL!";
    }
  }
}

function checkHttps(fccUrl){
  if (fccUrl.protocol === "https:"){
    return true;
  }
  return false;
}

function resetValues(){
  isError.value = false;
  dataProcessed.value = false;
  usesHttps.value = false;
}
</script>

<template>
  <div class="container">
    <h1>URL Privacy Score Generator</h1>
    <div class="input-div">
      <input v-model="url" placeholder="Enter your URL here" @keyup.enter="processURL">
      <button @click="processURL">
        <searchSVG />
      </button>
    </div>
    <div class="error-message" v-if="isError">{{ errorMessage }}</div>
    <div v-if="dataProcessed">
      Uses Https: {{ usesHttps }} <br>
      Cookies: {{ cookies }} <br>
    </div>
  </div>
</template>

<style>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}
.input-div {
  display: flex;
  align-items: center;
}
.error-message {
  color: red;
}
</style>
