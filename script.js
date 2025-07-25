async function receberCodigo() {
    try {
        const res = await fetch("/codigo/gerar");
        const data = await res.json();
        document.getElementById("saida").textContent = "Código: " + data.codigo;
    } catch (error) {
        document.getElementById("saida").textContent = "Erro ao obter código: " + error;
    }
}

document.addEventListener("DOMContentLoaded", () => {
   const inputTexto = document.getElementById("texto-a-traduzir");

    inputTexto.addEventListener("keydown", async (event) => {
       if (event.key === "Enter") {
           event.preventDefault();

           await traduzirTexto();
       } 
    });
});

async function traduzirTexto() {
    const texto = document.getElementById("texto-a-traduzir").value.trim();
    const origem = document.getElementById("idioma-origem").value;
    const destino = document.getElementById("idioma-destino").value;

    if (!texto) return alert("Digite o texto para traduzir!");

    try {
        const res = await fetch("/traduzir", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({texto, de:origem, para:destino})
        });
        const data = await res.json();
        document.getElementById("saida").textContent = "Tradução: " + data.traducao;
    } catch (error) {
        document.getElementById("saida").textContent = "Erro ao traduzir: " + error;
    }
}

async function enviarMensagem() {
    const input = document.getElementById("mensagem");
    const chatBox = document.getElementById("chat-box");
    const userMsg = input.value.trim();

    if (!userMsg) return;

    chatBox.textContent += `Você: ${userMsg}\n`;
    input.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: userMsg })
        });
        const data = await res.json();
        chatBox.textContent += `IA: ${data.resposta}\n\n`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        chatBox.textContent += "Erro ao conversar: " + error + "\n";
    }
}

function alternarTema() {
    document.body.classList.toggle("dark-mode");
    const btn = document.getElementById("toggle-theme");
    const isDark = document.body.classList.contains("dark-mode");
    
    btn.textContent = isDark ? "☀️" : "🌙";
    
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

document.addEventListener("DOMContentLoaded", () => {
    const temaSalvo = localStorage.getItem("theme");
    const btn = document.getElementById("toggle-theme");

    if (temaSalvo === "dark") {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }
    btn.textContent = temaSalvo === "dark" ? "☀️" : "🌙 ";

    const input = document.getElementById("mensagem");
    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                enviarMensagem();
            }
        });
    }
});

document.getElementById("menu-toggle").addEventListener("click", () => {
  const navMenu = document.getElementById("nav-menu");

  if (navMenu.classList.contains("show")) {
    navMenu.classList.remove("show");
  } else {
    navMenu.classList.add("show");
  }
});