<template>
  <div class="birthdays-view">
    <h2>Дни рождения коллег</h2>
    <div class="birthdays-list">
      <div class="birthday-card">
        <div class="avatar">👤</div>
        <div class="info">
          <h3>Имя Фамилия</h3>
          <p>15 ноября</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.birthdays-view {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

.birthdays-list {
  margin-top: 2rem;
}

.birthday-card {
  display: flex;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;

  .avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #3498db;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-right: 1rem;
  }

  .info {
    h3 {
      margin: 0 0 0.25rem 0;
    }

    p {
      margin: 0;
      color: #666;
    }
  }
}
</style>
