<template>
  <div class="habits">
    <h1>一键开启</h1>
    <form @submit.prevent="applyHabits">
      <ul>
        <li v-for="habit in habits" :key="habit.habit_id">
          <input type="checkbox" :value="habit.habit_id" v-model="selectedHabits" />
          {{ habit.username }} 的习惯
        </li>
      </ul>
      <button type="submit">应用</button>
      <button type="button" @click="deleteHabits">删除</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      habits: [],
      selectedHabits: [],
    };
  },
  async created() {
    try {
      const response = await fetch("/habits/");
      const result = await response.json();
      this.habits = result.user_habits;
    } catch (error) {
      console.error("获取习惯失败", error);
    }
  },
  methods: {
    async applyHabits() {
      try {
        const response = await fetch("/habits/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ habit_id: this.selectedHabits }),
        });
        if (response.ok) {
          alert("习惯已成功应用");
          this.selectedHabits = [];
        } else {
          alert("应用习惯失败");
        }
      } catch (error) {
        console.error("应用习惯失败", error);
      }
    },
    async deleteHabits() {
      try {
        const response = await fetch("/habits/", {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ habit_id: this.selectedHabits }),
        });
        if (response.ok) {
          alert("习惯已成功删除");
          this.selectedHabits = [];
          this.habits = this.habits.filter(habit => !this.selectedHabits.includes(habit.habit_id));
        } else {
          alert("删除习惯失败");
        }
      } catch (error) {
        console.error("删除习惯失败", error);
      }
    },
  },
};
</script>

<style>
/* ...样式代码... */
</style>
