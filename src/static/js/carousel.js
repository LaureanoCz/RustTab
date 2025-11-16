document.addEventListener('DOMContentLoaded', function(){
  const carousel = document.querySelector('.carousel');
  if(!carousel) return;
  const slidesWrap = carousel.querySelector('.slides');
  const slides = Array.from(carousel.querySelectorAll('.slide'));
  const prevBtn = carousel.querySelector('.carousel-btn.prev');
  const nextBtn = carousel.querySelector('.carousel-btn.next');
  const indicators = Array.from(carousel.querySelectorAll('.indicator'));
  let index = 0;
  let interval = null;

  function update(){
    slidesWrap.style.transform = `translateX(${ -index * 100 }%)`;
    slides.forEach((s,i)=> s.setAttribute('aria-hidden', i===index ? 'false' : 'true'));
    indicators.forEach((b,i)=> b.setAttribute('aria-selected', i===index ? 'true' : 'false'));
  }

  function next(){ index = (index+1) % slides.length; update(); }
  function prev(){ index = (index-1 + slides.length) % slides.length; update(); }

  function start(){ stop(); interval = setInterval(next, 4000); }
  function stop(){ if(interval) { clearInterval(interval); interval = null; } }

  nextBtn.addEventListener('click', ()=>{ next(); start(); });
  prevBtn.addEventListener('click', ()=>{ prev(); start(); });

  indicators.forEach(btn=> btn.addEventListener('click', (e)=>{ index = Number(btn.dataset.slide); update(); start(); }));

  carousel.addEventListener('mouseenter', stop);
  carousel.addEventListener('mouseleave', start);
  carousel.addEventListener('focusin', stop);
  carousel.addEventListener('focusout', start);

  document.addEventListener('keydown', (e)=>{
    if(!carousel.contains(document.activeElement) && !carousel.matches(':hover')) return;
    if(e.key === 'ArrowRight') { next(); start(); }
    if(e.key === 'ArrowLeft') { prev(); start(); }
  });

  update();
  start();
});
