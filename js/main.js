/* ===========================================================
   RVRR Construction & Property Sales — main.js v2
   Motion layer: loader, smart header, reveals, counters,
   parallax, tilt cards, magnetic buttons, custom cursor.
   =========================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var body = document.body;

  /* ---- Page loader (shows on first visit and page reload) ---- */
  var isReload = false;
  try {
    var nav = performance.getEntriesByType("navigation");
    if (nav && nav[0] && nav[0].type === "reload") isReload = true;
  } catch (e) {}

  var seen = false;
  try { seen = !isReload && sessionStorage.getItem("rvrr-loaded") === "1"; } catch (e) {}
  function ready() { body.classList.add("is-ready"); }
  if (!seen && !reduceMotion) {
    var loader = document.createElement("div");
    loader.className = "loader";
    loader.setAttribute("aria-hidden", "true");
    loader.innerHTML = '<div class="loader-inner">' +
      '<div class="loader-card">' +
        '<img src="images/logo.jpg" alt="RVRR Construction &amp; Property Sales" class="loader-logo" width="600" height="403" />' +
      '</div>' +
      '<div class="loader-bar"><i></i></div>' +
      '<p class="loader-tag">Building Trust &middot; Shaping Lifestyles</p>' +
    '</div>';
    body.appendChild(loader);
    window.addEventListener("load", function () {
      setTimeout(function () {
        loader.classList.add("done");
        ready();
        setTimeout(function () { loader.remove(); }, 1200);
      }, 950);
    });
    // safety net if load never fires quickly
    setTimeout(function () { if (!loader.classList.contains("done")) { loader.classList.add("done"); ready(); } }, 3500);
    try { sessionStorage.setItem("rvrr-loaded", "1"); } catch (e) {}
  } else {
    requestAnimationFrame(function () { requestAnimationFrame(ready); });
  }

  var header = document.querySelector(".header");

  /* ---- Mobile nav toggle ---- */
  var hamburger = document.querySelector(".hamburger");
  var navLinks = document.querySelector(".nav-links");
  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      var open = navLinks.classList.toggle("open");
      hamburger.classList.toggle("open", open);
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
      if (header) { header.classList.toggle("menu-open", open); header.classList.remove("hide"); }
      body.classList.toggle("menu-open", open);
      body.style.overflow = open ? "hidden" : "";
    });
    navLinks.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        hamburger.classList.remove("open");
        navLinks.classList.remove("open");
        if (header) header.classList.remove("menu-open");
        body.classList.remove("menu-open");
        body.style.overflow = "";
      });
    });
  }

  /* ---- Scroll UI: progress bar, smart header, back-to-top ---- */
  var progress = document.createElement("div");
  progress.className = "scroll-progress";
  body.appendChild(progress);

  var toTop = document.createElement("button");
  toTop.className = "to-top";
  toTop.setAttribute("aria-label", "Back to top");
  toTop.innerHTML = '<svg class="ring" viewBox="0 0 54 54"><circle cx="27" cy="27" r="24"/></svg><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>';
  toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }); });
  body.appendChild(toTop);
  var ringCircle = toTop.querySelector(".ring circle");

  var lastY = window.scrollY;
  var parallaxEls = [].slice.call(document.querySelectorAll("[data-parallax]"));
  var ticking = false;

  function onScroll() {
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var p = max > 0 ? y / max : 0;
    progress.style.transform = "scaleX(" + p + ")";
    if (ringCircle) ringCircle.style.strokeDashoffset = 151 - 151 * p;
    toTop.classList.toggle("show", y > 600);
    if (header) {
      header.classList.toggle("scrolled", y > 30);
    }
    if (!reduceMotion) {
      parallaxEls.forEach(function (el) {
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.2;
        var r = el.getBoundingClientRect();
        var offset = (r.top + r.height / 2 - window.innerHeight / 2) * speed;
        el.style.transform = "translate3d(0," + (-offset).toFixed(1) + "px,0)";
      });
    }
    lastY = y;
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---- Auto-stagger reveal children in grids ---- */
  [".pillars", ".feature-grid", ".sub-grid", ".value-grid", ".process", ".contact-info"].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (grid) {
      grid.querySelectorAll(":scope > .reveal, :scope > .step, :scope > .ci-item").forEach(function (el, i) {
        el.style.setProperty("--d", (i % 4) * 0.12 + "s");
        if (!el.classList.contains("reveal")) el.classList.add("reveal");
      });
    });
  });
  // Section headings & banners animate too
  document.querySelectorAll(".page-banner .container > *").forEach(function (el, i) {
    el.classList.add("hero-fade");
    el.style.transitionDelay = 0.15 + i * 0.12 + "s";
  });

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, .clip-reveal, .process");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---- Animated stat counters ---- */
  var counters = document.querySelectorAll("[data-count]");
  function runCounter(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion) { el.textContent = target + suffix; return; }
    var dur = 2000, t0 = null;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 4))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window && counters.length) {
    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        runCounter(e.target);
        cObs.unobserve(e.target);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cObs.observe(el); });
  } else {
    counters.forEach(runCounter);
  }

  /* ---- Hero background slideshow ---- */
  var slides = document.querySelectorAll(".hero-slide");
  if (slides.length > 1 && !reduceMotion) {
    var si = 0;
    setInterval(function () {
      slides[si].classList.remove("active");
      si = (si + 1) % slides.length;
      slides[si].classList.add("active");
    }, 6000);
  }

  /* ---- 3D tilt cards ---- */
  if (finePointer && !reduceMotion) {
    document.querySelectorAll(".pillar, .value-card, [data-tilt]").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transition = "transform .1s linear, box-shadow .5s";
        card.style.transform = "perspective(1000px) rotateY(" + x * 7 + "deg) rotateX(" + -y * 7 + "deg) translateY(-6px)";
      });
      card.addEventListener("mouseleave", function () {
        card.style.transition = "transform .8s cubic-bezier(.22,1,.36,1), box-shadow .5s";
        card.style.transform = "";
      });
    });

    /* ---- Magnetic buttons ---- */
    document.querySelectorAll(".btn, .socials a, .to-top").forEach(function (btn) {
      btn.addEventListener("mousemove", function (e) {
        var r = btn.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        btn.style.transform = "translate(" + x * 0.22 + "px," + y * 0.3 + "px)";
      });
      btn.addEventListener("mouseleave", function () { btn.style.transform = ""; });
    });

    /* ---- Custom cursor ---- */
    var dot = document.createElement("div"); dot.className = "cursor-dot";
    var ring = document.createElement("div"); ring.className = "cursor-ring";
    body.appendChild(dot); body.appendChild(ring);
    var mx = -100, my = -100, rx = -100, ry = -100;
    window.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = "translate(" + mx + "px," + my + "px) translate(-50%,-50%)";
    });
    (function loop() {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      ring.style.transform = "translate(" + rx + "px," + ry + "px) translate(-50%,-50%)";
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll("a, button, input, select, textarea, .pillar, .sub-card").forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("hover"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("hover"); });
    });
  }

  /* ---- Floating WhatsApp chat button ---- */
  var wa = document.createElement("a");
  wa.className = "wa-float";
  wa.href = "https://wa.me/919959802777";
  wa.target = "_blank";
  wa.rel = "noopener";
  wa.setAttribute("aria-label", "Chat with us on WhatsApp");
  wa.innerHTML = '<span class="wa-tip">Chat with us</span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.7 4.8-1.3A10 10 0 1 0 12 2zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.4 0-.9.1-3-1s-3.6-3.5-3.7-3.7-.9-1.2-.9-2.3.6-1.6.8-1.8.4-.3.6-.3h.5c.2 0 .4 0 .6.5s.7 1.7.7 1.8.1.3 0 .5-.1.3-.3.5-.3.4-.4.5-.3.3-.1.6.5.9 1.1 1.5c.8.7 1.4.9 1.7 1s.4.1.6-.1.7-.8.9-1.1.4-.2.6-.1 1.5.7 1.7.8.4.2.5.3 0 .6-.2 1.2z"/></svg>';
  body.appendChild(wa);

  /* ---- Contact form: validate, then open visitor's mail app pre-filled to rvrrservice.llp@gmail.com ---- */
  var form = document.getElementById("contactForm");
  if (form) {
    var FORM_EMAIL = "rvrrservice.llp@gmail.com";
    var success = document.getElementById("formSuccess");
    var errorBox = document.getElementById("formError");

    function showError(msg) {
      if (!errorBox) return;
      errorBox.innerHTML = msg;
      errorBox.style.display = "block";
    }

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (errorBox) errorBox.style.display = "none";
      if (success) success.style.display = "none";

      var invalid = [].slice.call(form.querySelectorAll("[required]")).filter(function (f) { return !f.checkValidity(); });
      form.querySelectorAll(".invalid").forEach(function (f) { f.classList.remove("invalid"); });
      if (invalid.length) {
        invalid.forEach(function (f) { f.classList.add("invalid"); });
        invalid[0].focus();
        showError("Please fill in all required fields with valid details.");
        return;
      }

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      if (data._honey) return; // bot

      // Open the visitor's own email app with every detail pre-filled, addressed to us
      var bodyText =
        "Hello RVRR Team,\n\nI would like to enquire about your services. My details are below:\n\n" +
        "Full Name: " + data.name + "\n" +
        "Phone Number: " + data.phone + "\n" +
        "Email Address: " + data.email + "\n" +
        "Service of Interest: " + (data.service || "Not specified") + "\n\n" +
        "Message:\n" + data.message + "\n\n" +
        "Thank you,\n" + data.name;
      var subject = "Website Enquiry" + (data.service ? " - " + data.service : "") + " - " + data.name;
      var mailto = "mailto:" + FORM_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(bodyText);
      window.location.href = mailto;

      if (success) {
        success.innerHTML = 'Your email app has opened with your enquiry ready — just press <strong>Send</strong> there. ' +
          'Didn\'t open? <a href="' + mailto + '" style="text-decoration:underline">Click here</a> or email us at ' +
          '<a href="mailto:' + FORM_EMAIL + '" style="text-decoration:underline">' + FORM_EMAIL + '</a>.';
        success.style.display = "block";
        success.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }

  /* ---- Footer year ---- */
  var yEl = document.getElementById("year");
  if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---- Accessibility: mark decorative inline SVGs as hidden ---- */
  document.querySelectorAll("svg:not([role])").forEach(function (svg) {
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
  });

  /* ---- Accessibility: inject a skip-to-content link ---- */
  var skip = document.createElement("a");
  skip.href = "#main-content";
  skip.className = "skip-link";
  skip.textContent = "Skip to main content";
  skip.addEventListener("click", function (e) {
    e.preventDefault();
    var target = document.getElementById("main-content") ||
      document.querySelector("main") || document.querySelector("h1");
    if (target) {
      target.setAttribute("tabindex", "-1");
      target.focus();
      target.scrollIntoView();
    }
  });
  body.insertBefore(skip, body.firstChild);

  /* ---- Mobile Footer Menu: highlight active page ---- */
  function updateMobileFooterMenu() {
    var rawPath = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    var hash = window.location.hash.toLowerCase();
    var items = document.querySelectorAll(".mfm-item");
    if (!items.length) return;

    var target = "home";
    if (rawPath === "about.html") {
      target = "about";
    } else if (rawPath === "contact.html") {
      target = "contact";
    } else if (rawPath === "services.html") {
      target = (hash === "#property") ? "property" : "services";
    } else if (rawPath.indexOf("service-") === 0) {
      if (rawPath.indexOf("plots") !== -1 || rawPath.indexOf("lands") !== -1 || rawPath.indexOf("commercial-space") !== -1 || rawPath.indexOf("buildings") !== -1 || rawPath.indexOf("flats") !== -1 || rawPath.indexOf("houses") !== -1) {
        target = "property";
      } else {
        target = "services";
      }
    } else {
      target = "home";
    }

    items.forEach(function (el) {
      if (el.getAttribute("data-page") === target) {
        el.classList.add("active");
        el.setAttribute("aria-current", "page");
      } else {
        el.classList.remove("active");
        el.removeAttribute("aria-current");
      }
    });
  }

  document.querySelectorAll(".mfm-item").forEach(function (item) {
    item.addEventListener("click", function () {
      document.querySelectorAll(".mfm-item").forEach(function (el) {
        el.classList.remove("active");
        el.removeAttribute("aria-current");
      });
      item.classList.add("active");
      item.setAttribute("aria-current", "page");
    });
  });

  updateMobileFooterMenu();
  window.addEventListener("hashchange", updateMobileFooterMenu);
})();


