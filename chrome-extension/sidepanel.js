const API = "http://127.0.0.1:8000";
const question = document.getElementById("question");
const answer = document.getElementById("answer");
const statusEl = document.getElementById("status");
const askBtn = document.getElementById("askBtn");
const speakBtn = document.getElementById("speakBtn");
const clearBtn = document.getElementById("clearBtn");
const readBtn = document.getElementById("readBtn");

let recognition = null;
let listening = false;

async function checkHealth() {
  try {
    const r = await fetch(`${API}/health`);
    const data = await r.json();
    statusEl.textContent = data.ollama ? "\u25CF Online" : "\u25CF API OK / Ollama OFF";
  } catch {
    statusEl.textContent = "\u25CF API Offline";
  }
}

async function askQuestion() {
  const q = question.value.trim();
  if (!q) { answer.textContent = "Please enter a question."; return; }
  askBtn.disabled = true;
  answer.textContent = "Thinking...";
  try {
    const r = await fetch(`${API}/ask`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: q})
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "API error");
    answer.textContent = data.answer || "No answer returned.";
    speakAnswer(data.answer || "");
  } catch (e) {
    answer.textContent = `Error: ${e.message}`;
  } finally {
    askBtn.disabled = false;
    checkHealth();
  }
}

function speakAnswer(text) {
  if (!text || !("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-IN";
  u.rate = 1.0;
  speechSynthesis.speak(u);
}

async function requestMicrophone() {
  if (!navigator.mediaDevices?.getUserMedia)
    throw new Error("Microphone API is unavailable in this Chrome context.");
  const stream = await navigator.mediaDevices.getUserMedia({audio: true});
  stream.getTracks().forEach(t => t.stop());
}

function createRecognition() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) throw new Error("Chrome Speech Recognition is unavailable.");

  const r = new SR();
  r.lang = "en-IN";
  r.continuous = false;
  r.interimResults = false;
  r.maxAlternatives = 1;

  r.onstart = () => {
    listening = true;
    speakBtn.textContent = "\uD83C\uDFA4 Listening...";
    statusEl.textContent = "\u25CF Listening";
  };

  r.onresult = e => {
    question.value = e.results[0][0].transcript.trim();
    askQuestion();
  };

  r.onerror = e => {
    listening = false;
    speakBtn.textContent = "\uD83C\uDFA4 Speak";
    const msg = {
      "not-allowed": "Microphone permission was denied. Allow microphone access for Chrome.",
      "service-not-allowed": "Chrome speech recognition service is unavailable.",
      "audio-capture": "Chrome could not access the microphone.",
      "no-speech": "No speech detected. Try again.",
      "network": "Chrome speech recognition network service failed.",
      "aborted": "Speech recognition was stopped."
    }[e.error] || e.error;
    answer.textContent = `Voice error: ${msg}`;
    checkHealth();
  };

  r.onend = () => {
    listening = false;
    speakBtn.textContent = "\uD83C\uDFA4 Speak";
    checkHealth();
  };
  return r;
}

async function startVoice() {
  if (listening) { recognition?.stop(); return; }
  try {
    answer.textContent = "Requesting microphone access...";
    await requestMicrophone();
    if (!recognition) recognition = createRecognition();
    recognition.start();
  } catch (e) {
    answer.textContent =
      `Microphone error: ${e.message}\n\n` +
      "Check Chrome and Windows microphone permissions, then try again.";
    speakBtn.textContent = "\uD83C\uDFA4 Speak";
  }
}

askBtn.addEventListener("click", askQuestion);
speakBtn.addEventListener("click", startVoice);
clearBtn.addEventListener("click", () => {
  question.value = "";
  answer.textContent = "Ready.";
});
readBtn.addEventListener("click", () => speakAnswer(answer.textContent));
question.addEventListener("keydown", e => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) askQuestion();
});

checkHealth();
setInterval(checkHealth, 10000);




