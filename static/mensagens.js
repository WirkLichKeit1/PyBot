const socket = io();

const userId = document.body.dataset.userId;
const contatoSelect = document.getElementById("contato_id");
const chatBox = document.getElementById("chat-box");
const formEnvio = document.getElementById("form-envio");
const inputMensagem = document.getElementById("mensagem");

// Carregar mensagens ao entrar
window.addEventListener("DOMContentLoaded", () => {
  if (contatoSelect && contatoSelect.value) {
    entrarNoChat(contatoSelect.value);
    carregarMensagens(contatoSelect.value);
  }
});

function entrarNoChat(contatoId) {
  socket.emit("entrar_chat", { contato_id: contatoId });
}

function carregarMensagens(contatoId) {
  fetch(`/api/mensagens/${contatoId}`)
    .then(res => res.json())
    .then(data => {
      chatBox.innerHTML = "";
      data.forEach(msg => {
        const div = document.createElement("div");
        div.className = `mensagem ${msg.remetente_id == userId ? "enviada" : "recebida"}`;
        div.innerHTML = `<p>${msg.conteudo}</p><span>${msg.timestamp}</span>`;
        chatBox.appendChild(div);
      });
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}

if (formEnvio) {
  formEnvio.addEventListener("submit", (e) => {
    e.preventDefault();
    const msg = inputMensagem.value.trim();
    if (msg && contatoSelect.value) {
      socket.emit("enviar_mensagem", {
        destinatario_id: contatoSelect.value,
        mensagem: msg
      });
      inputMensagem.value = "";
    }
  });
}

socket.on("nova_mensagem", (msg) => {
  const contatoAtual = contatoSelect.value;
  const ehDestinatario = msg.remetente_id != userId;

  if (ehDestinatario && msg.remetente_id != contatoAtual) return;

  const div = document.createElement("div");
  div.className = `mensagem ${msg.remetente_id == userId ? "enviada" : "recebida"}`;
  div.innerHTML = `<p>${msg.mensagem}</p><span>agora</span>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
});
