const form = document.querySelector("#route-form");
const queryInput = document.querySelector("#query");
const submitButton = document.querySelector("#submit");
const result = document.querySelector("#result");

const labels = {
  github: "GitHub",
  linear: "Linear",
  unclear: "Unclear",
  not_available: "Not available",
};

function showError(message) {
  result.hidden = false;
  result.className = "result error";
  result.textContent = message;
}

function showResult(body) {
  const destination = labels[body.destination] ?? body.destination;
  const confidence = `${Math.round(body.confidence * 100)}%`;
  result.hidden = false;
  result.className = "result";
  result.innerHTML = `
    <h2>${destination}</h2>
    <dl class="meta">
      <dt>Intent</dt>
      <dd></dd>
      <dt>Confidence</dt>
      <dd></dd>
    </dl>
    <p class="reply"></p>
  `;
  const [intent, confidenceNode] = result.querySelectorAll("dd");
  intent.textContent = body.intent;
  confidenceNode.textContent = confidence;
  result.querySelector(".reply").textContent = body.reply;
}

async function routeQuery(query) {
  submitButton.disabled = true;
  submitButton.textContent = "Routing…";
  try {
    const response = await fetch("/api/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const text = await response.text();
    let body;
    try {
      body = JSON.parse(text);
    } catch {
      throw new Error(
        response.ok
          ? "The router returned an unreadable response."
          : "The router could not classify that query.",
      );
    }
    if (!response.ok) {
      const detail = body.detail;
      throw new Error(
        typeof detail === "string" ? detail : "The router could not classify that query.",
      );
    }
    showResult(body);
  } catch (error) {
    showError(error.message || "The router could not classify that query.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Route query";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (!query) {
    showError("Enter a query.");
    return;
  }
  routeQuery(query);
});
