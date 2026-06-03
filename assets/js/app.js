function norm(s) {
  return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
}

function cssEscape(value) {
  if (typeof CSS !== "undefined" && typeof CSS.escape === "function") {
    return CSS.escape(value);
  }
  return String(value).replace(/[^a-zA-Z0-9_\u00A0-\uFFFF-]/g, "\\$&");
}

function isMobileNav() {
  return window.matchMedia("(max-width: 980px)").matches;
}

function getNavToggle() {
  return document.querySelector("[data-nav-toggle]");
}

function getNavBackdrop() {
  return document.querySelector("[data-nav-backdrop]");
}

function setDrawerOpen(open) {
  const nav = document.querySelector(".nav");
  const backdrop = getNavBackdrop();
  const toggle = getNavToggle();
  if (!nav) return;

  nav.classList.toggle("is-open", open);
  nav.setAttribute("aria-hidden", open ? "false" : "true");
  backdrop?.classList.toggle("is-open", open);
  if (backdrop) {
    if (open) backdrop.removeAttribute("hidden");
    else backdrop.setAttribute("hidden", "");
  }
  document.body.classList.toggle("nav-drawer-open", open);
  toggle?.setAttribute("aria-expanded", open ? "true" : "false");
  toggle?.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
  syncNavAccessibility();
}

function closeMobileNav() {
  if (!isMobileNav()) return;
  setDrawerOpen(false);
}

function openMobileNav() {
  if (!isMobileNav()) return;
  setDrawerOpen(true);
}

function initMobileNav() {
  const nav = document.querySelector(".nav");
  const toggle = getNavToggle();
  const backdrop = getNavBackdrop();
  if (!nav || !toggle) return;

  toggle.addEventListener("click", () => {
    if (nav.classList.contains("is-open")) closeMobileNav();
    else openMobileNav();
  });

  backdrop?.addEventListener("click", closeMobileNav);
  document.querySelector("[data-nav-close]")?.addEventListener("click", closeMobileNav);

  window.matchMedia("(max-width: 980px)").addEventListener("change", (e) => {
    if (!e.matches) closeMobileNav();
  });
}

function hashTarget() {
  return (location.hash || "").replace(/^#/, "");
}

function getPanel(id) {
  return document.getElementById(id);
}

function getMainScroll() {
  return document.querySelector("[data-main-scroll]");
}

function getNavScroll() {
  return document.querySelector("[data-nav-scroll]");
}

function resolvePanelId(id) {
  if (!id) return "start";
  const direct = getPanel(id);
  if (direct?.classList.contains("page-panel")) return id;
  const el = document.getElementById(id);
  const parent = el?.closest(".page-panel");
  return parent?.id || "start";
}

function getPanelOrder() {
  const seen = new Set();
  const order = [];
  for (const a of document.querySelectorAll("[data-nav-item]")) {
    const href = a.getAttribute("href") || "";
    const raw = href.replace(/^#/, "");
    if (!raw) continue;
    const pid = resolvePanelId(raw);
    if (!seen.has(pid)) {
      seen.add(pid);
      order.push(pid);
    }
  }
  return order;
}

let panelOrder = [];

function scrollMainTop() {
  const main = getMainScroll();
  if (main) main.scrollTop = 0;
  else window.scrollTo({ top: 0, behavior: "auto" });
}

function scrollNavLinkIntoView(id) {
  const hash = hashTarget();
  const link =
    document.querySelector(`[data-nav-item][href="#${cssEscape(hash)}"]`) ||
    document.querySelector(`[data-nav-item][href="#${cssEscape(id)}"]`);
  if (link) {
    link.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
}

function updateToolbarButtons(activeId) {
  const i = panelOrder.indexOf(activeId);
  const prev = document.querySelector("[data-panel-prev]");
  const next = document.querySelector("[data-panel-next]");
  if (prev) prev.disabled = i <= 0;
  if (next) next.disabled = i < 0 || i >= panelOrder.length - 1;
}

function showPanel(id, { scroll = true } = {}) {
  const panel = getPanel(id);
  if (!panel || !panel.classList.contains("page-panel")) return false;

  for (const el of document.querySelectorAll(".page-panel.is-active")) {
    el.classList.remove("is-active");
  }
  panel.classList.add("is-active");
  closeMobileNav();

  const titleEl = document.querySelector("[data-panel-title] strong");
  if (titleEl) {
    const h2 = panel.querySelector("h2");
    titleEl.textContent = h2 ? h2.textContent : id;
  }

  if (scroll) scrollMainTop();

  updateNavHighlight(id);
  updateToolbarButtons(id);
  requestAnimationFrame(() => scrollNavLinkIntoView(id));

  const sub = hashTarget();
  if (sub && sub !== id) {
    const target = document.getElementById(sub);
    if (target && target.closest(".page-panel") === panel) {
      requestAnimationFrame(() => {
        const main = getMainScroll();
        if (main) {
          const top = target.getBoundingClientRect().top - main.getBoundingClientRect().top + main.scrollTop - 8;
          main.scrollTo({ top, behavior: "smooth" });
        } else {
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    }
  }

  return true;
}

function navigatePanel(delta) {
  const current = resolvePanelId(hashTarget());
  const i = panelOrder.indexOf(current);
  if (i < 0) return;
  const next = panelOrder[i + delta];
  if (!next) return;
  history.replaceState(null, "", "#" + next);
  showPanel(next, { scroll: true });
}

function updateNavHighlight(activeId) {
  const hash = hashTarget();
  for (const a of document.querySelectorAll("[data-nav-item]")) {
    const href = a.getAttribute("href") || "";
    const id = href.replace(/^#/, "");
    const isActive = id === hash || id === activeId;
    a.classList.toggle("is-active", isActive);
    a.setAttribute("aria-current", isActive ? "page" : "false");
  }
}

function initPanelRouter() {
  panelOrder = getPanelOrder();
  if (!panelOrder.length) return;

  document.querySelector(".nav")?.addEventListener("click", (e) => {
    const a = e.target.closest("[data-nav-item]");
    if (!a) return;
    e.preventDefault();
    const href = a.getAttribute("href") || "";
    const id = href.replace(/^#/, "");
    if (!id) return;
    const panelId = resolvePanelId(id);
    if (showPanel(panelId)) {
      history.replaceState(null, "", href.startsWith("#") ? href : "#" + id);
    }
  });

  document.querySelector("[data-panel-prev]")?.addEventListener("click", () => navigatePanel(-1));
  document.querySelector("[data-panel-next]")?.addEventListener("click", () => navigatePanel(1));

  window.addEventListener("hashchange", () => {
    showPanel(resolvePanelId(hashTarget()), { scroll: true });
  });

  document.addEventListener("keydown", (e) => {
    if (e.target.closest("input, textarea")) return;
    if (e.key === "Escape") {
      closeMobileNav();
      return;
    }
    if (e.key === "ArrowLeft") navigatePanel(-1);
    if (e.key === "ArrowRight") navigatePanel(1);
  });

  const initial = resolvePanelId(hashTarget());
  showPanel(initial, { scroll: false });
}

function initNavFilter() {
  const input = document.querySelector("[data-nav-filter]");
  const links = Array.from(document.querySelectorAll("[data-nav-item]"));
  if (!input || links.length === 0) return;

  input.addEventListener("input", () => {
    const q = norm(input.value);
    for (const a of links) {
      const li = a.closest("li");
      if (!li) continue;
      const t = norm(a.textContent);
      li.style.display = !q || t.includes(q) ? "" : "none";
    }
    for (const g of document.querySelectorAll(".nav-group")) {
      let next = g.nextElementSibling;
      let any = false;
      while (next && !next.classList.contains("nav-group")) {
        if (next.style.display !== "none") any = true;
        next = next.nextElementSibling;
      }
      g.style.display = !q || any ? "" : "none";
    }
  });
}

function initLightbox() {
  const box = document.createElement("div");
  box.className = "lightbox";
  box.innerHTML =
    '<button type="button" class="lightbox-close" aria-label="Закрыть">×</button>' +
    '<img alt="" />' +
    '<span class="lightbox-hint">Esc — закрыть</span>';
  document.body.appendChild(box);
  const img = box.querySelector("img");
  const close = () => box.classList.remove("is-open");
  box.querySelector(".lightbox-close").addEventListener("click", close);
  box.addEventListener("click", (e) => {
    if (e.target === box) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });

  const root = document.querySelector("[data-main-scroll]") || document;
  root.addEventListener("click", (e) => {
    const el = e.target.closest("img.zoomable, .img-grid img, .two-col img");
    if (!el || el.closest(".lamp")) return;
    const full = el.getAttribute("data-full") || el.getAttribute("src");
    if (!full) return;
    img.src = full;
    img.alt = el.alt || "";
    box.classList.add("is-open");
  });
}

function syncNavAccessibility() {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  if (isMobileNav()) {
    nav.setAttribute("aria-hidden", nav.classList.contains("is-open") ? "false" : "true");
  } else {
    nav.setAttribute("aria-hidden", "false");
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-drawer-open");
    getNavBackdrop()?.classList.remove("is-open");
    getNavBackdrop()?.setAttribute("hidden", "");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  try {
    initMobileNav();
    syncNavAccessibility();
    window.matchMedia("(max-width: 980px)").addEventListener("change", syncNavAccessibility);
    initPanelRouter();
    initNavFilter();
    initLightbox();
  } catch (err) {
    console.error("Guide init failed:", err);
    document.querySelector("main")?.classList.add("init-failed");
  }
});
