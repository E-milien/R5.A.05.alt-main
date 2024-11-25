<script setup>
import Agent from './components/Agent.vue'
</script>

<template>
  <div>
    <div class="container">
      <div class="content">
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
        <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10"/>
      </div>
      <div class="container-arena">
        <h1 class="title">Arena 1</h1>
        <div class="arena">
          <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10" action="HIT"/>
          <img width="100" src="/fight.png">
          <Agent id="9510" :life="10" :strength="10" :armor="10" :speed="10" action="DODGE"/>
        </div>
        <h2 class="subtitle">Round 1</h2>
      </div>
    </div>
  </div>
</template>

<style scoped>
.title {
  text-align: center;
  font-size: 40px;

  margin-bottom: 70px;
}

.container {
  display: flex;

  justify-content: space-between;
  align-items: center;
}

.content {
  background-color: #34495e;

  min-height: 100vh;
  width: 320px;

  padding: 0px 30px;

  display: flex;
  flex-direction: column;
  
  justify-content: center;
  align-items: center;

  gap: 20px;
}

.container-arena {
  display: flex;
  flex-direction: column;

  justify-content: center;
  align-items: center;

  width: 100%;
}

.arena {
  display: flex;
  
  justify-content: center;
  align-items: center;

  padding: 10px 30px;

  gap: 40px;
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400..900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

* {
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Roboto', sans-serif;
  font-size: 16px;
 
  color: #ecf0f1;
  background-color: #2c3e50;
}
</style>
