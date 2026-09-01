const STORAGE_KEY = "fitlog-daily-routine-v2";
const DEFAULT_ROUTINE = [
  { id: "warmup", name: "가벼운 스트레칭", detail: "5분", icon: "🧘" },
  { id: "squats", name: "스쿼트", detail: "3세트 × 15회", icon: "🏋️" },
  { id: "pushups", name: "푸시업", detail: "3세트 × 10회", icon: "💪" },
  { id: "walk", name: "빠르게 걷기", detail: "20분", icon: "🚶" },
  { id: "cooldown", name: "마무리 스트레칭", detail: "5분", icon: "🌿" },
];
const routineList = document.getElementById("routine-list");
const progressText = document.getElementById("progress-text");
const progressPercent = document.getElementById("progress-percent");
const progressBar = document.getElementById("progress-bar");
const weekGrid = document.getElementById("week-grid");
const weekSummary = document.getElementById("week-summary");
const keyForDate = (date = new Date()) => { const offset = date.getTimezoneOffset() * 60000; return new Date(date.getTime() - offset).toISOString().slice(0, 10); };
function loadState() { try { const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); if (Array.isArray(saved.routine) && saved.routine.length) return { routine: saved.routine, history: saved.history || {} }; } catch {} return { routine: DEFAULT_ROUTINE, history: {} }; }
let state = loadState();
const saveState = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
const completedToday = () => state.history[keyForDate()] || [];
const isDone = (id) => completedToday().includes(id);
function escapeHtml(value) { const node = document.createElement("span"); node.textContent = value; return node.innerHTML; }
function renderRoutine() {
  const completed = completedToday();
  routineList.innerHTML = state.routine.length ? state.routine.map((exercise) => {
    const name = escapeHtml(exercise.name); const detail = escapeHtml(exercise.detail || "횟수 또는 시간을 입력하세요"); const done = completed.includes(exercise.id);
    return `<li class="routine-item ${done ? "done" : ""}" data-id="${exercise.id}"><button class="check-btn" type="button" aria-label="${name} 완료">${done ? "✓" : ""}</button><span class="exercise-icon">${exercise.icon || "✨"}</span><div class="exercise-info"><strong>${name}</strong><span>${detail}</span></div><button class="remove-btn" type="button" aria-label="${name} 삭제">×</button></li>`;
  }).join("") : '<li class="empty">등록된 운동이 없습니다. 새 루틴을 추가해 보세요.</li>';
  const total = state.routine.length; const count = completed.filter((id) => state.routine.some((item) => item.id === id)).length; const percent = total ? Math.round((count / total) * 100) : 0;
  progressText.textContent = `${count} / ${total}`; progressPercent.textContent = `${percent}%`; progressBar.style.width = `${percent}%`;
}
function weekDates() { const now = new Date(); const monday = new Date(now); monday.setDate(now.getDate() + (now.getDay() === 0 ? -6 : 1 - now.getDay())); return Array.from({ length: 7 }, (_, index) => { const day = new Date(monday); day.setDate(monday.getDate() + index); return day; }); }
function getStreak() { let streak = 0; const day = new Date(); while ((state.history[keyForDate(day)] || []).length) { streak += 1; day.setDate(day.getDate() - 1); } return streak; }
function renderWeek() {
  const labels = ["월", "화", "수", "목", "금", "토", "일"]; let activeDays = 0;
  weekGrid.innerHTML = weekDates().map((day, index) => { const key = keyForDate(day); const active = (state.history[key] || []).length > 0; if (active) activeDays += 1; return `<div class="day ${active ? "active" : ""} ${key === keyForDate() ? "today" : ""}"><span>${labels[index]}</span><b>${day.getDate()}</b><i>${active ? "✓" : ""}</i></div>`; }).join("");
  weekSummary.textContent = `${activeDays}일 운동`; document.getElementById("streak-count").textContent = getStreak();
}
function render() { renderRoutine(); renderWeek(); }
routineList.addEventListener("click", (event) => { const item = event.target.closest(".routine-item"); if (!item) return; const id = item.dataset.id; if (event.target.closest(".remove-btn")) { state.routine = state.routine.filter((exercise) => exercise.id !== id); state.history[keyForDate()] = completedToday().filter((doneId) => doneId !== id); } else if (event.target.closest(".check-btn")) { state.history[keyForDate()] = isDone(id) ? completedToday().filter((doneId) => doneId !== id) : [...completedToday(), id]; } else return; saveState(); render(); });
document.getElementById("add-form").addEventListener("submit", (event) => { event.preventDefault(); const name = document.getElementById("exercise-name"); const detail = document.getElementById("exercise-detail"); state.routine.push({ id: `custom-${Date.now()}`, name: name.value.trim(), detail: detail.value.trim(), icon: "✨" }); name.value = ""; detail.value = ""; saveState(); render(); name.focus(); });
document.getElementById("reset-btn").addEventListener("click", () => { state.history[keyForDate()] = []; saveState(); render(); });
document.getElementById("today-label").textContent = new Intl.DateTimeFormat("ko-KR", { month: "long", day: "numeric", weekday: "long" }).format(new Date());
render();
