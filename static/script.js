const chat = document.getElementById("chat");

const send = document.getElementById("send");

const message = document.getElementById("message");

const image = document.getElementById("image");

const preview = document.getElementById("preview");

let selectedImage = null;

// =========================
// Vista previa de imagen
// =========================

image.addEventListener("change", () => {

    preview.innerHTML = "";

    selectedImage = image.files[0];

    if (!selectedImage) return;

    const img = document.createElement("img");

    img.src = URL.createObjectURL(selectedImage);

    preview.appendChild(img);

});

// =========================
// Crear mensaje
// =========================

function addMessage(text, user = false) {

    const div = document.createElement("div");

    div.className = user ? "message user" : "message ai";

    div.innerHTML = `
        <div class="bubble">${text}</div>
    `;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;

    return div;

}

// =========================
// Enviar
// =========================

async function sendMessage() {

    const text = message.value.trim();

    if (text === "" && !selectedImage) return;

    addMessage(text || "📷 Imagen enviada", true);

    const thinking = addMessage("🩺 Pensando...");

    const data = new FormData();

    data.append("message", text);

    if (selectedImage) {

        data.append("image", selectedImage);

    }

    try {

        const response = await fetch("/chat", {

            method: "POST",

            body: data

        });

        const result = await response.json();

        thinking.querySelector(".bubble").innerHTML = result.reply;

    }

    catch {

        thinking.querySelector(".bubble").innerHTML =
            "❌ Error al conectar con el servidor.";

    }

    message.value = "";

    image.value = "";

    selectedImage = null;

    preview.innerHTML = "";

    chat.scrollTop = chat.scrollHeight;

}

// =========================
// Botón enviar
// =========================

send.addEventListener("click", sendMessage);

// =========================
// Ctrl + Enter
// =========================

message.addEventListener("keydown", (e) => {

    if (e.ctrlKey && e.key === "Enter") {

        e.preventDefault();

        sendMessage();

    }

});