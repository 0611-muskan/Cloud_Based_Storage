const API = "http://localhost:5000/files";

// Get user email from token
function getUserEmail() {
  const token = localStorage.getItem("token");

  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.email;
  } catch {
    return null;
  }
}

// Upload file
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");

  if (!fileInput.files[0]) {
    alert("Please select a file");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("email", getUserEmail()); // ✅ IMPORTANT

  await fetch(`${API}/upload`, {
    method: "POST",
    body: formData
  });

  loadFiles();
}

// Load files (user-specific)
async function loadFiles() {
  const email = getUserEmail();

  const res = await fetch(`${API}?email=${email}`);
  const data = await res.json();

  const list = document.getElementById("fileList");
  list.innerHTML = "";

  data.forEach(file => {
    if (!file.Key) return;

    const li = document.createElement("li");

    const cleanName = file.Key.split("/")[1].split("-").slice(1).join("-");
    const sizeMB = (file.Size / (1024 * 1024)).toFixed(2);

    li.innerHTML = `
      <span class="file-info">📄 ${cleanName} (${sizeMB} MB)</span>
      <div>
        <button class="btn-danger" onclick="deleteFile('${file.Key}')">Delete</button>
        <button class="btn-success" onclick="shareFile('${file.Key}')">Share</button>
        <button class="btn-primary" onclick="downloadFile('${file.Key}')">Download</button>
      </div>
    `;

    list.appendChild(li);
  });
}

// Delete file
async function deleteFile(key) {
  await fetch(`${API}/${encodeURIComponent(key)}`, {
  method: "DELETE"
});

  loadFiles();
}

// Share file
async function shareFile(key) {
  const res = await fetch(`${API}/share/${encodeURIComponent(key)}`);
  const data = await res.json();

  await navigator.clipboard.writeText(data.url);

  document.getElementById("shareLink").innerHTML = `
    ✅ Link copied!
    <br>
    <a href="${data.url}" target="_blank">Open File</a>
  `;
}

// Download
async function downloadFile(key) {
 const res = await fetch(`${API}/share/${encodeURIComponent(key)}`);
  const data = await res.json();

  window.open(data.url, "_blank");
}

// Logout
function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// Load on start
loadFiles();