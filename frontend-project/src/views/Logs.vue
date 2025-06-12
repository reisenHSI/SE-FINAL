<template>
  <div class="logs-container">
    <h2>日志查询</h2>

    <div class="filter-section">
      <label>
        用户名:
        <select v-model="filters.check_username">
          <option value="">全部</option>
          <option v-for="user in filterOptions.usernames" :key="user" :value="user">{{ user }}</option>
        </select>
      </label>

      <label>
        设备名:
        <select v-model="filters.devicename">
          <option value="">全部</option>
          <option v-for="dev in filterOptions.devicenames" :key="dev" :value="dev">{{ dev }}</option>
        </select>
      </label>

      <label>
        起始时间:
        <input type="date" v-model="filters.start_time" />
      </label>

      <label>
        结束时间:
        <input type="date" v-model="filters.end_time" />
      </label>

      <button @click="fetchLogs(true)">查询</button>
      <button @click="resetFilters">重置</button>
    </div>

    <div class="summary">
      <p>共 {{ totalCount }} 条日志记录</p>
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
  name: 'Logs',
  data() {
    return {
      logs: [],
      totalCount: 0,
      filterOptions: {
        usernames: [],
        devicenames: []
      },
      filters: {
        username: '',
        devicename: '',
        start_time: '',
        end_time: ''
      },
      errorMsg: ''
    }
  },
  mounted() {
    this.fetchLogs(false)
  },
  methods: {
    async fetchLogs(isFilter) {
      this.errorMsg = ''
      try {
        let response
        if (isFilter) {
          // POST 筛选
          response = await axios.post(`${API_BASE_URL}home/query_logs/`, this.filters)

        } else {
          // GET 全查
          response = await axios.get(`${API_BASE_URL}home/query_logs/`)
        }

        if (response.data.status === 'success') {
          this.logs = response.data.logs
          this.totalCount = response.data.total_count
          this.filterOptions.usernames = response.data.filter_options.usernames || []
          this.filterOptions.devicenames = response.data.filter_options.devicenames || []
        } else {
          this.errorMsg = response.data.message || '查询失败'
        }
      } catch (e) {
        this.errorMsg = '网络或服务器错误: ' + e.message
      }
    },
    resetFilters() {
      this.filters = {
        username: localStorage.getItem('username'),
        check_username: '',
        devicename: '',
        start_time: '',
        end_time: ''
      }
      this.fetchLogs(false)
    }
  }
}
</script>

<style scoped>
.logs-container {
  padding: 20px;
  background: #f8fbff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h2 {
  color: #2a6ecf;
  margin-bottom: 20px;
}

.filter-section {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  align-items: flex-end;
}

.filter-section label {
  display: flex;
  flex-direction: column;
  font-weight: bold;
  font-size: 14px;
  color: #2a6ecf;
}

.filter-section input,
.filter-section select {
  margin-top: 4px;
  padding: 6px 8px;
  border: 1px solid #c5d1e8;
  border-radius: 4px;
  min-width: 140px;
}

button {
  background-color: #2a6ecf;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
  margin-top: 4px;
  height: 36px;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #1e50a1;
  transform: translateY(-2px);
}

.summary {
  margin-bottom: 12px;
  color: #333;
  font-weight: 600;
}

.log-list {
  list-style: none;
  padding: 0;
  max-height: 500px;
  overflow-y: auto;
  border: 1px solid #d0e3f1;
  border-radius: 8px;
  background: white;
  width: 80%;
}

.log-item {
  padding: 12px 16px;
  border-bottom: 1px solid #e0e8f7;
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #555;
}

.timestamp {
  min-width: 140px;
  color: #999;
}

.operation {
  flex: 1;
}

.error-msg {
  margin-top: 20px;
  color: #d9534f;
  font-weight: bold;
}
</style>
