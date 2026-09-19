// These option lists come straight from the encoders your model was
// trained on in Colab, so every choice here is one the model recognizes.
const EDUCATION_CODES = ["c", "d", "cc", "i", "j", "k", "m", "r", "q", "w", "x", "e", "aa", "ff"];
const ETHNICITY_CODES = ["v", "h", "bb", "j", "n", "z", "dd", "ff", "o"];

function fillSelect(id, options) {
  const select = document.getElementById(id);
  select.innerHTML = "";
  options.forEach((opt) => {
    const el = document.createElement("option");
    el.value = opt;
    el.textContent = opt;
    select.appendChild(el);
  });
}

fillSelect("f5", EDUCATION_CODES);
fillSelect("f6", ETHNICITY_CODES);

const form = document.getElementById("predict-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultDiv.innerHTML = "";

  const payload = {};
  for (let i = 0; i < 15; i++) {
    payload[i] = document.getElementById("f" + i).value;
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      resultDiv.innerHTML = `<div class="result-box error">${data.error || "Something went wrong."}</div>`;
      return;
    }

    const cls = data.prediction === "Approved" ? "approved" : "rejected";
    let html = `<div class="result-box ${cls}">
      Prediction: <strong>${data.prediction}</strong>
      <span class="prob">Model confidence of approval: ${data.approve_probability}%</span>`;

    if (data.warnings && data.warnings.length > 0) {
      data.warnings.forEach((w) => {
        html += `<span class="warn">&#9888; ${w}</span>`;
      });
    }

    html += `</div>`;
    resultDiv.innerHTML = html;
  } catch (err) {
    resultDiv.innerHTML = `<div class="result-box error">Could not reach the backend. Is app.py running?</div>`;
  }
});
