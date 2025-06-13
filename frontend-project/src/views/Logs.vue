<template>
  <div class="logs-container">
    <div class="header-bar">
      <button class="back-btn" @click="goBack">← 返回</button>
      <h2>日志查询</h2>
    </div>

    <div class="filter-section">
      <div class="filter-item">
        <label>用户名</label>
        <select v-model="filters.username">
          <option value="">全部</option>
          <option v-for="user in filterOptions.usernames" :key="user" :value="user">{{ user }}</option>
        </select>
      </div>

      <div class="filter-item">
        <label>设备名</label>
        <select v-model="filters.devicename">
          <option value="">全部</option>
          <option v-for="dev in filterOptions.devicenames" :key="dev" :value="dev">{{ dev }}</option>
        </select>
      </div>

      <div class="filter-item">
        <label>起始时间</label>
        <input type="date" v-model="filters.start_time" />
      </div>

      <div class="filter-item">
        <label>结束时间</label>
        <input type="date" v-model="filters.end_time" />
      </div>

      <div class="filter-actions">
        <button @click="fetchLogs(true)">查询</button>
        <button @click="resetFilters" class="reset-btn">重置</button>
      </div>
    </div>

    <div class="summary">
      共 {{ totalCount }} 条日志记录
    </div>

    <ul class="log-list">
      <li v-for="log in logs" :key="log.id" class="log-item">
        <span class="timestamp">{{ log.timestamp }}</span>
        <span class="operation">{{ log.formatted_operation }}</span>
      </li>
    </ul>

    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
  </div>
</template>

<script>
import { API_BASE_URL } from "../main";
import axios from "axios";

export default {
  name: "Logs",
  data() {
    return {
      logs: [],
      totalCount: 0,
      filterOptions: {
        usernames: [],
        devicenames: [],
      },
      filters: {
        username: "",
        devicename: "",
        start_time: "",
        end_time: "",
      },
      errorMsg: "",
    };
  },
  mounted() {
    this.fetchLogs(false);
  },
  methods: {
    async fetchLogs(isFilter) {
      this.errorMsg = "";
      try {
        let response;
        if (isFilter) {
          response = await axios.post(`${API_BASE_URL}home/query_logs/`, this.filters);
        } else {
          response = await axios.get(`${API_BASE_URL}home/query_logs/`);
        }

        if (response.data.status === "success") {
          this.logs = response.data.logs;
          this.totalCount = response.data.total_count;
          this.filterOptions.usernames = response.data.filter_options.usernames || [];
          this.filterOptions.devicenames = response.data.filter_options.devicenames || [];
        } else {
          this.errorMsg = response.data.message || "查询失败";
        }
      } catch (e) {
        this.errorMsg = "网络或服务器错误: " + e.message;
      }
    },
    resetFilters() {
      this.filters = {
        username: "",
        devicename: "",
        start_time: "",
        end_time: "",
      };
      this.fetchLogs(false);
    },
    goBack() {
      window.history.back();
    },
  },
};
</script>

<style scoped>
.logs-container {
  max-width: 960px;
  margin: 30px auto;
  padding: 24px 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgb(0 0 0 / 0.1);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  color: #3b5998;
  font-weight: 700;
  margin-bottom: 28px;
  text-align: center;
  font-size: 2rem;
  user-select: none;
}

.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px 32px;
  justify-content: center;
  margin-bottom: 28px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eaeef7;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 180px;
  flex-grow: 1;
}

.filter-item label {
  font-weight: 600;
  font-size: 0.95rem;
  color: #3b5998;
  margin-bottom: 6px;
  user-select: none;
}

.filter-item select,
.filter-item input[type="date"] {
  height: 38px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1.8px solid #a8b8dc;
  font-size: 1rem;
  color: #374151;
  background: #f7faff;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.filter-item select:focus,
.filter-item input[type="date"]:focus {
  border-color: #3b5998;
  box-shadow: 0 0 6px rgba(59, 89, 152, 0.4);
  outline: none;
}

.filter-actions {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: nowrap;
  min-width: 160px;
}

button {
  height: 42px;
  padding: 0 24px;
  border-radius: 24px;
  border: none;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 10px rgb(59 89 152 / 0.35);
  user-select: none;
  color: #fff;
  background: linear-gradient(135deg, #3b5998 0%, #1d3b70 100%);
}

button:hover {
  background: linear-gradient(135deg, #4e6ebf 0%, #27509a 100%);
  box-shadow: 0 8px 18px rgb(59 89 152 / 0.6);
  transform: translateY(-2px);
}

.reset-btn {
  background: #e0e6f2;
  color: #555a75;
  box-shadow: none;
}

.reset-btn:hover {
  background: #c6cee2;
  color: #3b5998;
  box-shadow: 0 4px 10px rgb(59 89 152 / 0.25);
  transform: translateY(-1px);
}

.summary {
  text-align: center;
  font-weight: 600;
  color: #4a4a4a;
  font-size: 1.15rem;
  margin-bottom: 20px;
  user-select: none;
}

.log-list {
  max-height: 480px;
  overflow-y: auto;
  padding: 0;
  margin: 0 auto;
  width: 100%;
  list-style: none;
  border-radius: 12px;
  border: 1.8px solid #e0e6f2;
  background-color: #fbfcff;
  box-shadow: inset 0 2px 8px rgb(59 89 152 / 0.05);
}

.log-item {
  display: flex;
  gap: 18px;
  padding: 14px 24px;
  font-size: 1rem;
  color: #333a56;
  border-bottom: 1.2px solid #e6eaf7;
  user-select: text;
}

.log-item:last-child {
  border-bottom: none;
}

.timestamp {
  min-width: 160px;
  color: #9aa5c1;
  font-family: "Courier New", Courier, monospace;
  font-size: 0.95rem;
}

.operation {
  flex: 1;
  white-space: pre-wrap;
  line-height: 1.35;
  word-break: break-word;
}

.error-msg {
  margin-top: 28px;
  text-align: center;
  color: #db3b3b;
  font-weight: 700;
  font-size: 1.1rem;
  user-select: none;
}

.header-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: #3b5998;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
  user-select: none;
}

.back-btn:hover {
  background-color: rgba(59, 89, 152, 0.15);
}
</style>
