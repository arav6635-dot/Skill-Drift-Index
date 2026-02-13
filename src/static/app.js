const queryEl = document.getElementById("query");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusText = document.getElementById("statusText");
const resultPanel = document.getElementById("resultPanel");
const resultTitle = document.getElementById("resultTitle");
const confidenceBadge = document.getElementById("confidenceBadge");

const skillScore = document.getElementById("skillScore");
const riskScore = document.getElementById("riskScore");
const demandTrend = document.getElementById("demandTrend");
const salaryTrajectory = document.getElementById("salaryTrajectory");
const halfLife = document.getElementById("halfLife");
const peakRelevance = document.getElementById("peakRelevance");
const projectedDecline = document.getElementById("projectedDecline");
const explanation = document.getElementById("explanation");
const sourceList = document.getElementById("sourceList");

function titleCase(text) {
  if (!text || typeof text !== "string") {
    return "medium";
  }
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading;
  analyzeBtn.textContent = isLoading ? "Analyzing..." : "Analyze Skill Drift";
  statusText.textContent = isLoading ? "Running Gemini model" : "Ready";
}

function setResult(data) {
  resultPanel.classList.remove("hidden");
  resultTitle.textContent = data.query ? `Result for ${data.query}` : "Result";
  confidenceBadge.textContent = `${titleCase(data.confidence || "medium")} confidence`;

  skillScore.textContent = `${data.skill_drift_score ?? "--"}/100`;
  riskScore.textContent = `${data.risk_of_obsolescence ?? "--"}/100`;
  demandTrend.textContent = data.demand_trend || "--";
  salaryTrajectory.textContent = data.salary_trajectory || "--";
  halfLife.textContent = data.stack_half_life || "--";
  peakRelevance.textContent = data.peak_relevance || "--";
  projectedDecline.textContent = data.projected_decline || "--";
  explanation.textContent = data.explanation || data.notes || "No explanation available.";

  sourceList.innerHTML = "";
  const sources = Array.isArray(data.data_sources) ? data.data_sources : [];
  if (sources.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No source metadata provided";
    sourceList.appendChild(li);
    return;
  }

  for (const source of sources) {
    const li = document.createElement("li");
    li.textContent = source;
    sourceList.appendChild(li);
  }
}

async function runAnalysis() {
  const query = queryEl.value.trim();

  if (!query) {
    statusText.textContent = "Enter a tech stack or job title.";
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/skill-drift/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const payload = await response.json();

    if (!response.ok) {
      statusText.textContent = payload.error || "Request failed.";
      return;
    }

    setResult(payload);
    statusText.textContent = "Completed";
  } catch (error) {
    statusText.textContent = "Network error. Check server logs.";
  } finally {
    setLoading(false);
  }
}

analyzeBtn.addEventListener("click", runAnalysis);
queryEl.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    runAnalysis();
  }
});
