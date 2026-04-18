(() => {
  const sidebar = document.getElementById("sidebar");
  const frame = document.getElementById("service-view");
  const emptyState = document.getElementById("empty-state");
  const frameError = document.getElementById("frame-error");
  const openInBrowserBtn = document.getElementById("open-in-browser");

  let services = [];
  let currentId = null;

  function iconMarkup(svc) {
    if (svc.icon_url) {
      return `<img src="${svc.icon_url}" alt="">`;
    }
    const letter = (svc.name || "?").trim().charAt(0).toUpperCase();
    return `<span class="initial">${letter}</span>`;
  }

  function renderSidebar() {
    sidebar.innerHTML = "";
    services.forEach((svc, idx) => {
      const btn = document.createElement("button");
      btn.className = "service-btn";
      btn.dataset.id = svc.id;
      btn.title = `${svc.name}  (⌘${idx + 1})`;
      btn.innerHTML = `${iconMarkup(svc)}<span class="tooltip">${svc.name}</span>`;
      btn.addEventListener("click", () => selectService(svc.id));
      if (svc.id === currentId) btn.classList.add("active");
      sidebar.appendChild(btn);
    });
  }

  function setActive(id) {
    currentId = id;
    document.querySelectorAll(".service-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.id === id);
    });
  }

  function selectService(id) {
    const svc = services.find((s) => s.id === id);
    if (!svc) return;
    setActive(id);
    emptyState.hidden = true;
    frameError.hidden = true;
    frame.hidden = false;
    document.title = `AgentOps — ${svc.name}`;
    frame.src = svc.url;
    window.pywebview?.api?.select_service(id);
  }

  function showEmpty() {
    emptyState.hidden = false;
    frame.hidden = true;
  }

  window.addEventListener("keydown", (e) => {
    if (!(e.metaKey || e.ctrlKey)) return;
    if (e.key >= "1" && e.key <= "9") {
      const idx = parseInt(e.key, 10) - 1;
      if (services[idx]) {
        e.preventDefault();
        selectService(services[idx].id);
      }
    } else if (e.key.toLowerCase() === "r") {
      if (currentId) {
        e.preventDefault();
        const svc = services.find((s) => s.id === currentId);
        if (svc) frame.src = svc.url;
      }
    }
  });

  openInBrowserBtn?.addEventListener("click", () => {
    const svc = services.find((s) => s.id === currentId);
    if (svc) window.pywebview?.api?.open_in_browser(svc.url);
  });

  async function init() {
    try {
      services = (await window.pywebview.api.list_services()) || [];
    } catch (err) {
      console.error("Failed to load services:", err);
      services = [];
    }
    if (!services.length) {
      showEmpty();
      return;
    }
    const last = await window.pywebview.api.get_last_service();
    const initial =
      services.find((s) => s.id === last) ||
      services.find((s) => s.default) ||
      services[0];
    renderSidebar();
    selectService(initial.id);
  }

  window.addEventListener("pywebviewready", init);
})();
