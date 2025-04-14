document.getElementById("enablePlugin").addEventListener("change", (e) => {
  chrome.storage.sync.set({ enabled: e.target.checked });
});
chrome.storage.sync.get(["enabled"], (data) => {
  document.getElementById("enablePlugin").checked = data.enabled || false;
});
