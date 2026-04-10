(() => {
  function init() {
    const prefersReducedMotion =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const targets = new Set();

    // Hero: staged entrance on page load.
    document
      .querySelectorAll(
        ".article-hero .article-meta, .article-hero .article-title, .article-hero .article-lead, .article-hero .article-hero-row"
      )
      .forEach((el, i) => {
        el.classList.add("reveal");
        el.style.setProperty("--reveal-delay", `${i * 90}ms`);
        targets.add(el);
      });

    // Sidebar cards + main content blocks reveal on scroll.
    document
      .querySelectorAll(".article-sidebar .sidebar-card, .article-content > *")
      .forEach((el) => {
        // Skip if already handled in hero.
        if (targets.has(el)) return;
        el.classList.add("reveal");
        targets.add(el);
      });

    // If the user prefers reduced motion, show everything instantly.
    if (prefersReducedMotion) {
      targets.forEach((el) => el.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const el = entry.target;
          if (!el.style.getPropertyValue("--reveal-delay")) {
            // Tiny, consistent delay helps avoid harsh pops on fast scroll.
            el.style.setProperty("--reveal-delay", "40ms");
          }
          el.classList.add("is-visible");
          observer.unobserve(el);
        }
      },
      { threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
    );

    targets.forEach((el) => observer.observe(el));

    // Smooth anchor navigation for the sidebar "In this article" links.
    // Keeps the interaction sleek without needing heavy scroll libs.
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", (e) => {
        const href = a.getAttribute("href");
        if (!href || href === "#") return;
        const id = href.slice(1);
        const target = document.getElementById(id);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        history.pushState(null, "", href);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();

