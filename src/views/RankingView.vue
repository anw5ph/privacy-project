<script setup>
import { reactive, onMounted } from 'vue';
import rawData from '../backend/data.json';

// Convert the object of objects into an array of objects
const dataArray = Object.values(rawData);

let reactiveData = reactive(dataArray);

// function sortByHTTPS(){
//   reactiveData.sort((a, b) => b.httpsScore - a.httpsScore);
// }

// function sortByCookies(){
//   reactiveData.sort((a, b) => b.cookieScore - a.cookieScore);
// }

function sortByTotal(){
  reactiveData.sort((a, b) => b.overallScore - a.overallScore);
}

onMounted(sortByTotal);

function getRowClass(overallScore) {
  if (overallScore < 2 / 3) return 'table-danger';
  if (overallScore < 4 / 3) return 'table-warning';
  return 'table-success';
}

</script>

<template>
  <div class="container">
    <div class="header">
      <h1 class="title">URL Privacy Score Rankings</h1>
      <RouterLink class="link" to="/">
        <button type="button" class="btn btn-primary" id="back-button">
          Back
        </button>
      </RouterLink>
      <!-- <div class="button-row">
        <button type="button" class="btn btn-success" @click="sortByHTTPS">Sort by HTTPS Score</button>
        <button type="button" class="btn btn-danger" @click="sortByCookies">Sort by Cookies Score</button>
        <button type="button" class="btn btn-warning" @click="sortByTotal">Sort by Total Score</button>
      </div> -->
    </div>
    <table class="table" id="tableCSS">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">URL</th>
          <th scope="col">HTTPS Score</th>
          <th scope="col">Cookies Score</th>
          <th scope="col">Total Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in reactiveData" :key="index" :class="getRowClass(item.overallScore)">
          <th scope="row">{{ parseInt(index) + 1  }}</th>
          <td>{{ item.url }}</td>
          <td>{{ item.httpsScore }}</td>
          <td>{{ item.cookieScore }}</td>
          <td>{{ item.overallScore }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
.button-row{
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  width: 50%;
}
.title {
  margin-top: 20px;
}

#back-button {
  margin-bottom: 10px;
}

.header {
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

.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

#tableCSS {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-radius: 20px;
}</style>