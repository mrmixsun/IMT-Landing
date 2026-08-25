/* ================================================================
   IMT-Landing — Interactions
   ================================================================ */

document.addEventListener('DOMContentLoaded', function () {

    /* --- Mobile Nav Toggle --- */
    const navToggle = document.getElementById('navToggle');
    const navLinks  = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            this.classList.toggle('active');
            navLinks.classList.toggle('open');
        });

        // Close nav on link click
        navLinks.querySelectorAll('.nav__link').forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.classList.remove('active');
                navLinks.classList.remove('open');
            });
        });
    }

    /* --- Nav scroll shadow --- */
    const nav = document.getElementById('nav');
    let lastScroll = 0;

    window.addEventListener('scroll', function () {
        const y = window.scrollY;
        if (y > 50) {
            nav.classList.add('nav--scrolled');
        } else {
            nav.classList.remove('nav--scrolled');
        }
        lastScroll = y;
    }, { passive: true });

    /* --- Audience Tabs --- */
    const tabContainer = document.getElementById('audienceTabs');
    if (tabContainer) {
        const tabBtns = tabContainer.querySelectorAll('.tabs__btn');
        const tabContents = tabContainer.querySelectorAll('.tabs__content');

        tabBtns.forEach(function (btn) {
            btn.addEventListener('click', function () {
                // Remove active from all
                tabBtns.forEach(function (b) { b.classList.remove('active'); });
                tabContents.forEach(function (c) { c.classList.remove('active'); });

                // Activate current
                this.classList.add('active');
                const target = document.getElementById('tab-' + this.dataset.tab);
                if (target) target.classList.add('active');
            });
        });
    }

    /* --- Scroll Reveal --- */
    const revealElements = document.querySelectorAll(
        '.section__header, .card, .quote, .direction, .principle, ' +
        '.audience-card, .gems__stat, .cta__option, .callout, ' +
        '.solution__definition, .hero__stat, .hero__actions'
    );

    if (revealElements.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach(function (el) {
            el.classList.add('reveal');
            observer.observe(el);
        });
    }

    /* --- Smooth scroll for anchor links (fallback) --- */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const offset = nav ? nav.offsetHeight : 0;
                window.scrollTo({
                    top: target.getBoundingClientRect().top + window.scrollY - offset,
                    behavior: 'smooth'
                });
            }
        });
    });

});