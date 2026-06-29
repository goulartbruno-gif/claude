document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  toggle.addEventListener('click', () => links.classList.toggle('active'));
  links.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => links.classList.remove('active'))
  );

  document.querySelectorAll('.faq__question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.parentElement;
      const answer = item.querySelector('.faq__answer');
      const isActive = item.classList.contains('active');

      document.querySelectorAll('.faq__item.active').forEach(open => {
        open.classList.remove('active');
        open.querySelector('.faq__answer').style.maxHeight = null;
        open.querySelector('.faq__question').setAttribute('aria-expanded', 'false');
      });

      if (!isActive) {
        item.classList.add('active');
        answer.style.maxHeight = answer.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  const nav = document.getElementById('nav');
  window.addEventListener('scroll', () => {
    nav.style.background = window.scrollY > 80
      ? 'rgba(26,26,26,.98)'
      : 'rgba(26,26,26,.95)';
  }, { passive: true });

  // Scroll reveal — apenas como aprimoramento. Se o usuário pede menos
  // movimento ou o navegador não suporta IntersectionObserver, o conteúdo
  // permanece visível (nunca escondemos nada que dependa de JS para reaparecer).
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealEls = document.querySelectorAll(
    '.mulher__card, .produto__card, .diferencial__item, .b2b__feature, .faq__item'
  );

  if (!prefersReduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });

    revealEls.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity .6s ease, transform .6s ease';
      observer.observe(el);
    });
  }
});
