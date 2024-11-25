<script setup>
defineProps({
  id: String,

  life: Number,
  strength: Number,
  armor: Number,
  speed: Number,

  action: String
})
</script>

<template>
  <div>
    <div class="agent">
      <img width="80" src="/agent.png">

      <div class="info">
        <div class="id">{{ id }}</div>

        <div class="stats">
          <div>Vie : {{ life }}</div>
          <div>Force : {{ strength }}</div>
          <div>Armure : {{ armor }}</div>
          <div>Vitesse : {{ speed }}</div>

        </div>
      </div>
    </div>
    <div v-if="action != null" class="action">{{ action }}</div>
  </div>
</template>

<style scoped>
.agent {
  width: fit-content;
  padding: 10px 40px 10px 30px;

  display: flex;

  justify-content: center;
  align-items: center;

  gap: 30px;

  border: 2px solid #ecf0f1;
  border-radius: 10px;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.id {
  font-size: 18px;
  font-weight: 500;
}

.stats {
  display: flex;
  flex-direction: column;

  gap: 1px;

  font-size: 12px;
  font-weight: 300;
}

.action {
  text-align: center;

  font-size: 15px;
  font-weight: 500;

  background-color: #e74c3c;

  width: 100%;

  margin-top: 10px;

  border-radius: 50px;
}
</style>
