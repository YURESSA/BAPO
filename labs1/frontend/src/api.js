// src/api.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getTasks() {
  try {
    const res = await axios.get(`${API_URL}/tasks`);
    return res.data;
  } catch (e) {
    console.error("getTasks error", e);
    return [];
  }
}

export async function createTask(task) {
  const res = await axios.post(`${API_URL}/tasks`, task);
  return res.data;
}

export async function updateTask(id, task) {
  const res = await axios.put(`${API_URL}/tasks/${id}`, task);
  return res.data;
}

export async function deleteTask(id) {
  await axios.delete(`${API_URL}/tasks/${id}`);
}
