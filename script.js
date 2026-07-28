// ---- 数据：唯一的“真相来源” (source of truth) ----
let tasks = [];            // 每个任务: { id, text, done }
let currentFilter = 'all'; // 'all' | 'active' | 'done'
let nextId = 1;

// ---- DOM 引用 ----
const form = document.getElementById('task-form');
const input = document.getElementById('task-input');
const list = document.getElementById('task-list');
const filtersEl = document.getElementById('filters');
const emptyMessage = document.getElementById('empty-message');

// ---- 修改数据的函数：只负责改 tasks，然后调用 render() ----

function addTask(text) {
  const trimmed = text.trim();
  if (!trimmed) return;
  tasks.push({ id: nextId++, text: trimmed, done: false });
  render();
}

function deleteTask(id) {
  tasks = tasks.filter((task) => task.id !== id);
  render();
}

function toggleTask(id) {
  const task = tasks.find((t) => t.id === id);
  if (task) task.done = !task.done;
  render();
}

function editTask(id, newText) {
  const trimmed = newText.trim();
  if (!trimmed) return;
  const task = tasks.find((t) => t.id === id);
  if (task) task.text = trimmed;
  render();
}

function setFilter(filter) {
  currentFilter = filter;
  render();
}

// ---- 只读数据、不修改 tasks ----

function getFilteredTasks() {
  if (currentFilter === 'active') return tasks.filter((t) => !t.done);
  if (currentFilter === 'done') return tasks.filter((t) => t.done);
  return tasks;
}

// ---- 把一个 task 对象变成一个 <li> DOM 节点 ----

function createTaskElement(task) {
  const li = document.createElement('li');
  li.className = 'task-item' + (task.done ? ' done' : '');
  li.dataset.id = task.id;

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = task.done;
  checkbox.addEventListener('change', () => toggleTask(task.id));

  const text = document.createElement('span');
  text.className = 'task-text';
  text.textContent = task.text;
  text.addEventListener('dblclick', () => startEditing(li, task));

  const editBtn = document.createElement('button');
  editBtn.type = 'button';
  editBtn.textContent = 'Edit';
  editBtn.addEventListener('click', () => startEditing(li, task));

  const deleteBtn = document.createElement('button');
  deleteBtn.type = 'button';
  deleteBtn.className = 'delete-btn';
  deleteBtn.textContent = 'Delete';
  deleteBtn.addEventListener('click', () => deleteTask(task.id));

  li.append(checkbox, text, editBtn, deleteBtn);
  return li;
}

// 把某一行的文字换成一个输入框，方便编辑
function startEditing(li, task) {
  const editInput = document.createElement('input');
  editInput.type = 'text';
  editInput.className = 'task-edit-input';
  editInput.value = task.text;

  const finishEditing = () => editTask(task.id, editInput.value);

  editInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') finishEditing();
    if (e.key === 'Escape') render(); // 取消编辑，恢复原样
  });
  editInput.addEventListener('blur', finishEditing);

  li.querySelector('.task-text').replaceWith(editInput);
  editInput.focus();
  editInput.select();
}

// ---- 唯一负责“画面”的函数：每次数据变化后，从 tasks 重新画整个列表 ----

function render() {
  const filtered = getFilteredTasks();

  list.innerHTML = '';
  filtered.forEach((task) => list.appendChild(createTaskElement(task)));

  emptyMessage.hidden = filtered.length > 0;

  [...filtersEl.children].forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.filter === currentFilter);
  });
}

// ---- 事件绑定：把用户操作接到上面的函数上 ----

form.addEventListener('submit', (e) => {
  e.preventDefault();
  addTask(input.value);
  input.value = '';
  input.focus();
});

filtersEl.addEventListener('click', (e) => {
  const btn = e.target.closest('.filter-btn');
  if (!btn) return;
  setFilter(btn.dataset.filter);
});

render();
