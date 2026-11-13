const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("chatMessages");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

function addMessage(text, who) {
  const wrap = document.createElement("div");
  wrap.className = `message ${who}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  const time = document.createElement("span");
  time.className = "time";
  time.textContent = who === "user" ? "You" : "Assistant";
  wrap.append(bubble, time);
  messages.appendChild(wrap);
  messages.scrollTop = messages.scrollHeight;
  return wrap;
}

async function sendMessage(text) {
  const clean = text.trim();
  if (!clean) return;
  addMessage(clean, "user");
  input.value = "";
  sendBtn.disabled = true;
  sendBtn.textContent = "Thinking...";
  const pending = addMessage("Please wait while I prepare a response...", "bot");
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: clean})
    });
    const data = await response.json();
    pending.querySelector(".bubble").textContent = response.ok ? data.reply : (data.error || "Something went wrong.");
  } catch (error) {
    pending.querySelector(".bubble").textContent = "I couldn't connect to the server. Please try again.";
  } finally {
    sendBtn.disabled = false;
    sendBtn.innerHTML = 'Send <span>➤</span>';
    input.focus();
    messages.scrollTop = messages.scrollHeight;
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  sendMessage(input.value);
});
document.querySelectorAll("[data-prompt]").forEach(button => {
  button.addEventListener("click", () => sendMessage(button.dataset.prompt));
});
clearBtn.addEventListener("click", () => {
  messages.replaceChildren();
  addMessage("Chat cleared. What would you like to ask?", "bot");
});
