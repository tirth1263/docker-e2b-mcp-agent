const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 },
  );
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("visible"));
}

const tabs = document.querySelectorAll(".code-tab");
const panels = document.querySelectorAll(".code-content");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.dataset.tab;
    tabs.forEach((item) => {
      const active = item === tab;
      item.classList.toggle("active", active);
      item.setAttribute("aria-selected", String(active));
    });
    panels.forEach((panel) => {
      const active = panel.id === `code-${target}`;
      panel.classList.toggle("active", active);
      panel.hidden = !active;
    });
  });
});

document.querySelectorAll(".copy-button").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.parentElement.querySelector("code").innerText;
    try {
      await navigator.clipboard.writeText(code);
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    } catch {
      button.textContent = "Select text";
    }
  });
});

const runButton = document.querySelector("#run-demo");
const terminalOutput = document.querySelector("#terminal-output");
const workflowSteps = [
  ["00:00", "Sandbox", "E2B environment created"],
  ["00:02", "Gateway", "GitHub + Notion MCP tools ready"],
  ["00:04", "GitHub", "Repositories ranked by stars"],
  ["00:07", "Agent", "Top three summaries drafted"],
  ["00:09", "Notion", "Page created successfully"],
];

const wait = (duration) => new Promise((resolve) => setTimeout(resolve, duration));

runButton.addEventListener("click", async () => {
  runButton.disabled = true;
  runButton.innerHTML = '<span class="run-icon" aria-hidden="true">●</span> Running preview…';
  terminalOutput.innerHTML = '<p><span class="prompt">$</span> uv run main.py</p>';

  for (const [time, label, message] of workflowSteps) {
    await wait(420);
    const line = document.createElement("p");
    line.className = "terminal-step";
    line.innerHTML = `<span>${time}</span><strong>${label.padEnd(9, " ")}</strong> ${message}`;
    terminalOutput.appendChild(line);
  }

  await wait(250);
  const success = document.createElement("p");
  success.className = "terminal-success";
  success.textContent = "✓ Workflow complete · Notion brief is ready";
  terminalOutput.appendChild(success);
  runButton.disabled = false;
  runButton.innerHTML = '<span class="run-icon" aria-hidden="true">↻</span> Replay workflow';
});
