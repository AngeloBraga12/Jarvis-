const state = { mode: "idle", recognition: null, listening: false, audio: null, analyser: null, animation: 0 };

const $ = (id) => document.getElementById(id);
const visualizer = $("visualizer");
const stateLabel = $("stateLabel");
const inputLabel = $("inputLabel");
const outputLabel = $("outputLabel");
const commandInput = $("commandInput");
const activityList = $("activityList");
const canvas = $("waveCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * ratio));
  canvas.height = Math.max(1, Math.floor(rect.height * ratio));
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

function setState(mode, label) {
  state.mode = mode;
  visualizer.className = `visualizer state-${mode}`;
  stateLabel.innerHTML = `<i></i> ${label}`;
  inputLabel.textContent = mode === "listening" ? "Você falando" : "Entrada de voz";
  outputLabel.textContent = mode === "speaking" ? "JARVIS falando" : "Saída de voz";
  $("wakeButton").classList.toggle("listening", mode === "listening");
  $("micButton").classList.toggle("active", mode === "listening");
}

function drawWave() {
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  ctx.clearRect(0, 0, width, height);
  const mid = height * 0.57;
  const active = state.mode === "listening" || state.mode === "speaking";
  const amplitude = active ? 38 : 5;
  const speed = performance.now() / (state.mode === "thinking" ? 480 : 210);

  for (let side = 0; side < 2; side += 1) {
    ctx.beginPath();
    const center = side === 0 ? width * 0.27 : width * 0.73;
    const start = side === 0 ? width * 0.05 : width * 0.55;
    const end = side === 0 ? width * 0.45 : width * 0.95;
    for (let x = start; x <= end; x += 3) {
      const distance = Math.abs(x - center) / (width * 0.2);
      const envelope = Math.max(0, 1 - distance);
      const wave = Math.sin(x * 0.17 + speed) * Math.sin(x * 0.035 - speed * 0.7);
      const y = mid + wave * amplitude * envelope * (active ? 1 : 0.35);
      if (x === start) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = side === 0 ? "rgba(38,184,255,.95)" : "rgba(46,122,204,.35)";
    ctx.lineWidth = 2;
    ctx.shadowBlur = active ? 12 : 0;
    ctx.shadowColor = "rgba(35,177,255,.8)";
    ctx.stroke();
  }
  ctx.shadowBlur = 0;
  state.animation = requestAnimationFrame(drawWave);
}
drawWave();

function addActivity(title, detail, icon = "•") {
  const item = document.createElement("div");
  item.className = "activity";
  item.innerHTML = `<span class="activity-icon">${icon}</span><div><b>${escapeHtml(title)}</b><small>${escapeHtml(detail)}</small></div><time>agora</time>`;
  activityList.prepend(item);
  while (activityList.children.length > 6) activityList.lastElementChild.remove();
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[char]));
}

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "pt-BR";
  utterance.rate = 1.02;
  utterance.pitch = 0.95;
  utterance.onstart = () => setState("speaking", "Respondendo por voz");
  utterance.onend = () => setState("idle", "Pronto para ouvir");
  window.speechSynthesis.speak(utterance);
}

async function sendCommand(text) {
  const command = text.trim();
  if (!command) return;
  setState("thinking", "Processando comando");
  addActivity("Comando recebido", command, "↗");
  commandInput.value = "";

  try {
    const response = await fetch("/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command })
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Falha ao processar comando");

    const message = payload.message || "Comando recebido.";
    addActivity("JARVIS respondeu", message, "◉");
    setState("speaking", "Resposta pronta");
    speak(message);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Erro desconhecido";
    addActivity("Falha", message, "!");
    setState("idle", "Pronto para ouvir");
  }
}

async function loadSystem() {
  try {
    const response = await fetch("/system");
    const payload = await response.json();
    const data = payload.result || {};
    $("cpuValue").textContent = `${data.cpu_count ?? "--"} núcleos`;
    $("ramValue").textContent = data.memory ?? "Disponível";
    $("diskValue").textContent = data.disk_free ?? "Disponível";
    $("gpuValue").textContent = "N/D";
    addActivity("Sistema verificado", `${data.os ?? "Sistema"} • ${data.hostname ?? "host local"}`, "✓");
  } catch {
    $("connectionLabel").innerHTML = "<i style='background:#ff9e49'></i> Offline";
    addActivity("Backend indisponível", "Execute o servidor local do JARVIS", "!");
  }
}

function setupSpeechRecognition() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) return null;
  const recognition = new Recognition();
  recognition.lang = "pt-BR";
  recognition.interimResults = true;
  recognition.continuous = false;
  recognition.onstart = () => {
    state.listening = true;
    setState("listening", "Ouvindo você");
  };
  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i += 1) transcript += event.results[i][0].transcript;
    commandInput.value = transcript;
    if (event.results[event.results.length - 1].isFinal) sendCommand(transcript);
  };
  recognition.onerror = () => {
    state.listening = false;
    setState("idle", "Pronto para ouvir");
    addActivity("Microfone", "Não foi possível iniciar o reconhecimento de voz", "!");
  };
  recognition.onend = () => {
    state.listening = false;
    if (state.mode === "listening") setState("idle", "Pronto para ouvir");
  };
  return recognition;
}

state.recognition = setupSpeechRecognition();

function toggleListening() {
  if (!state.recognition) {
    commandInput.focus();
    addActivity("Microfone não suportado", "Digite o comando no campo abaixo", "!");
    return;
  }
  if (state.listening) state.recognition.stop(); else state.recognition.start();
}

$("wakeButton").addEventListener("click", toggleListening);
$("micButton").addEventListener("click", toggleListening);
$("commandForm").addEventListener("submit", (event) => {
  event.preventDefault();
  sendCommand(commandInput.value);
});
$("clearActivity").addEventListener("click", () => { activityList.innerHTML = ""; });

document.querySelectorAll("[data-command]").forEach((button) => {
  button.addEventListener("click", () => sendCommand(button.dataset.command));
});

addActivity("Interface iniciada", "Command Center carregado", "✓");
loadSystem();
setInterval(loadSystem, 30000);
