const API_BASE = "http://127.0.0.1:8000";

async function fetchJobs() {
  const res = await fetch(`${API_BASE}/jobs/`);
  if (!res.ok) throw new Error("Failed to fetch jobs");
  const jobs = await res.json();
  const list = document.getElementById("jobs-list");
  list.innerHTML = "";
  jobs.forEach((job) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="job-title">${job.title} @ ${job.company}</div>
      <div class="job-meta">#${job.id} • ${job.location}</div>
      <p>${job.description}</p>
    `;
    list.appendChild(li);
  });
}

async function submitResume(event) {
  event.preventDefault();
  const form = event.target;
  const data = {
    candidate_name: form.candidate_name.value,
    email: form.email.value,
    resume_text: form.resume_text.value,
  };
  const ids = form.target_job_ids.value
    .split(",")
    .map((id) => parseInt(id.trim(), 10))
    .filter((id) => !Number.isNaN(id));
  if (ids.length) data.target_job_ids = ids;

  const status = document.getElementById("form-status");
  const button = form.querySelector("button");
  button.disabled = true;
  status.textContent = "Matching...";

  try {
    const res = await fetch(`${API_BASE}/resumes/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Match failed");
    const matches = await res.json();
    renderResults(matches);
    status.textContent = "Success!";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
  }
}

function renderResults(matches) {
  const list = document.getElementById("results");
  list.innerHTML = "";
  matches.forEach(({ job, score }) => {
    const li = document.createElement("li");
    const pct = Math.round(score * 100);
    li.innerHTML = `
      <div class="job-title">${job.title}</div>
      <div class="job-meta">${job.company} • Confidence ${pct}%</div>
      <p>${job.description}</p>
    `;
    list.appendChild(li);
  });
}

document.getElementById("resume-form").addEventListener("submit", submitResume);

fetchJobs().catch((err) => console.error(err));





