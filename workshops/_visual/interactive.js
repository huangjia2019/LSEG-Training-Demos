(function () {
  const dataNode = document.getElementById("demo-data");
  if (!dataNode) return;

  const demo = JSON.parse(dataNode.textContent);
  const scenarioSelect = document.getElementById("scenario-select");
  const runButton = document.getElementById("run-demo");
  const nextButton = document.getElementById("next-step");
  const resetButton = document.getElementById("reset-demo");
  const stepsNode = document.getElementById("interactive-steps");
  const stateNode = document.getElementById("state-view");
  const logNode = document.getElementById("terminal-log");
  const outputNode = document.getElementById("output-view");

  let scenarioIndex = 0;
  let stepIndex = -1;
  let timer = null;

  function scenario() {
    return demo.scenarios[scenarioIndex];
  }

  function currentStep() {
    return scenario().steps[Math.max(0, stepIndex)] || null;
  }

  function stopTimer() {
    if (timer) window.clearInterval(timer);
    timer = null;
  }

  function setStep(nextIndex) {
    stopTimer();
    const max = scenario().steps.length - 1;
    stepIndex = Math.max(-1, Math.min(nextIndex, max));
    render();
  }

  function renderScenarioOptions() {
    scenarioSelect.innerHTML = demo.scenarios.map((item, idx) => {
      return `<option value="${idx}">${item.label}</option>`;
    }).join("");
  }

  function renderSteps() {
    stepsNode.innerHTML = scenario().steps.map((step, idx) => {
      const classes = ["interactive-step"];
      if (idx < stepIndex) classes.push("done");
      if (idx === stepIndex) classes.push("active");
      return `<button class="${classes.join(" ")}" type="button" data-step="${idx}">
        <span class="idx">${String(idx + 1).padStart(2, "0")}</span>
        <span class="name">${step.name}</span>
        <span class="pattern">${step.pattern}</span>
        <span class="mini">${step.output}</span>
      </button>`;
    }).join("");
    stepsNode.querySelectorAll("[data-step]").forEach((node) => {
      node.addEventListener("click", () => setStep(Number(node.dataset.step)));
    });
  }

  function renderState() {
    if (stepIndex < 0) {
      stateNode.textContent = JSON.stringify({
        scenario: scenario().label,
        status: "ready",
        instruction: "Click Run Demo or Next Step."
      }, null, 2);
      return;
    }
    stateNode.textContent = JSON.stringify({
      scenario: scenario().label,
      step: currentStep().name,
      pattern: currentStep().pattern,
      state: currentStep().state
    }, null, 2);
  }

  function renderLog() {
    if (stepIndex < 0) {
      logNode.innerHTML = `<div class="active-line">$ ${demo.title}</div><div>${scenario().summary}</div>`;
      return;
    }
    const rows = scenario().steps.slice(0, stepIndex + 1).map((step, idx) => {
      const cls = idx === stepIndex ? "active-line" : "";
      return `<div class="${cls}">[${String(idx + 1).padStart(2, "0")}] ${step.log}</div>`;
    });
    logNode.innerHTML = rows.join("");
    logNode.scrollTop = logNode.scrollHeight;
  }

  function renderOutput() {
    const finalReached = stepIndex === scenario().steps.length - 1;
    if (stepIndex < 0) {
      outputNode.innerHTML = `<div class="output-headline">Ready to run</div><p>${scenario().summary}</p>`;
      return;
    }
    const step = currentStep();
    const final = scenario().final;
    const verdict = finalReached ? final.verdict : "RUNNING";
    const warn = /REVIEW|WARN|RUNNING/.test(verdict) ? " warn" : "";
    const cards = (finalReached ? final.cards : [
      ["Active step", step.name],
      ["Pattern", step.pattern],
      ["Output", step.output],
      ["Next", stepIndex + 1 < scenario().steps.length ? scenario().steps[stepIndex + 1].name : "final"]
    ]).map(([key, value]) => {
      return `<div class="output-card"><strong>${key}</strong><span>${value}</span></div>`;
    }).join("");
    outputNode.innerHTML = `
      <span class="verdict${warn}">${verdict}</span>
      <div class="output-headline">${finalReached ? final.headline : step.output}</div>
      <div class="output-cards">${cards}</div>
    `;
  }

  function render() {
    renderSteps();
    renderState();
    renderLog();
    renderOutput();
    nextButton.disabled = stepIndex >= scenario().steps.length - 1;
  }

  function runDemo() {
    stopTimer();
    stepIndex = -1;
    render();
    timer = window.setInterval(() => {
      if (stepIndex >= scenario().steps.length - 1) {
        stopTimer();
        return;
      }
      stepIndex += 1;
      render();
    }, 850);
  }

  scenarioSelect.addEventListener("change", () => {
    scenarioIndex = Number(scenarioSelect.value);
    stepIndex = -1;
    stopTimer();
    render();
  });
  runButton.addEventListener("click", runDemo);
  nextButton.addEventListener("click", () => setStep(stepIndex + 1));
  resetButton.addEventListener("click", () => setStep(-1));

  renderScenarioOptions();
  render();
})();
