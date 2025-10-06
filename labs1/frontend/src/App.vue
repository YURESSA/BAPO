<template>
  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <div class="logo">
        <span class="logo-icon">📝</span>
        <h1>TaskFlow</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Add Task Card -->
      <div class="add-task-card glassmorphism">
        <input
          v-model="newTaskTitle"
          type="text"
          class="modern-input"
          placeholder="Task title"
          @keyup.enter="addTask"
        />
        <input
          v-model="newTaskDescription"
          type="text"
          class="modern-input"
          placeholder="Description (optional)"
          @keyup.enter="addTask"
        />
        <button class="add-btn" @click="addTask" :disabled="!newTaskTitle">
          ➕ Add Task
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="tasks.length === 0" class="empty-state">
        <div class="empty-icon">🎯</div>
        <h3>No tasks yet</h3>
        <p>Add your first task to get started!</p>
      </div>

      <!-- Tasks List -->
      <div v-else class="tasks-grid">
        <div v-for="task in tasks" :key="task.id" class="task-card">
          <div class="task-content">
            <div>
              <h3 class="task-title">{{ task.title }}</h3>
              <p class="task-description">{{ task.description }}</p>
            </div>
            <div class="task-actions">
              <button class="action-btn edit-btn" @click="openEditModal(task)">✏️</button>
              <button class="action-btn delete-btn" @click="deleteTask(task.id)">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-backdrop" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Edit Task</h2>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <input v-model="editTask.title" class="modern-input full-width" placeholder="Task title" />
          <textarea v-model="editTask.description" class="modern-textarea" placeholder="Description"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveEdit">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getTasks, createTask, updateTask as apiUpdateTask, deleteTask as apiDeleteTask } from "./api";

export default {
  data() {
    return {
      tasks: [],
      newTaskTitle: "",
      newTaskDescription: "",
      editTask: null,
      showEditModal: false
    };
  },
  async mounted() {
    this.tasks = await getTasks();
  },
  methods: {
    async addTask() {
      if (!this.newTaskTitle) return;
      const task = await createTask({
        title: this.newTaskTitle,
        description: this.newTaskDescription
      });
      this.tasks.push(task);
      this.newTaskTitle = "";
      this.newTaskDescription = "";
    },
    openEditModal(task) {
      this.editTask = { ...task };
      this.showEditModal = true;
    },
    async saveEdit() {
      const updated = await apiUpdateTask(this.editTask.id, this.editTask);
      const index = this.tasks.findIndex(t => t.id === updated.id);
      this.tasks[index] = updated;
      this.closeModal();
    },
    closeModal() {
      this.showEditModal = false;
      this.editTask = null;
    },
    async deleteTask(id) {
      if (confirm("Delete this task?")) {
        await apiDeleteTask(id);
        this.tasks = this.tasks.filter(t => t.id !== id);
      }
    }
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea, #764ba2);
  font-family: 'Inter', sans-serif;
  color: white;
}

.app-header {
  padding: 1rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255,255,255,0.2);
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 2rem;
  font-weight: bold;
}

.main-content {
  max-width: 900px;
  margin: 2rem auto;
  display: grid;
  gap: 2rem;
}

/* Add Task Card */
.add-task-card {
  display: grid;
  gap: 1rem;
  padding: 2rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.modern-input {
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
  color: white;
}

.add-btn {
  padding: 1rem;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  font-weight: bold;
  cursor: pointer;
}

/* Tasks Grid */
.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.task-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.task-card:hover {
  transform: translateY(-3px);
  background: rgba(255,255,255,0.15);
}

.task-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.task-description {
  color: rgba(255,255,255,0.8);
  font-size: 0.95rem;
}

.task-actions button {
  margin-left: 0.5rem;
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.task-actions button:hover {
  transform: scale(1.1);
}

/* Modal */
.modal-backdrop {
  position: fixed;
  top:0; left:0; width:100%; height:100%;
  background: rgba(0,0,0,0.5);
  display:flex; align-items:center; justify-content:center;
  z-index: 1000;
}

.modal-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border-radius: 16px;
  padding: 2rem; /* добавляем внутренние отступы */
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  gap: 1rem; /* небольшой отступ между блоками */
  box-sizing: border-box; /* чтобы padding учитывался корректно */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.close-btn {
  background: rgba(255,255,255,0.1);
  color: white;
  border: none;
  font-size: 1.2rem;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
}

.modal-body .modern-input,
.modal-body .modern-textarea {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  width: 100%;
  margin-bottom: 1rem;
}

.modal-body .modern-textarea {
  border-radius: 12px;
  padding: 1rem;
  min-height: 80px;
  resize: vertical;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
.modal-header,
.modal-body,
.modal-footer {
  padding: 0; /* уже есть gap в родителе, лишние паддинги не нужны */
}

.modal-body .modern-input,
.modal-body .modern-textarea {
  width: 100%;
  margin-bottom: 1rem;
  box-sizing: border-box; /* чтобы ширина учитывала padding */
}
.btn-secondary {
  background: rgba(255,255,255,0.2);
  color: white;
  border-radius: 12px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  color: white;
  border-radius: 12px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: rgba(255,255,255,0.7);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

</style>
