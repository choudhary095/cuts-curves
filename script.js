window.addEventListener('load', function(){ setTimeout(function(){document.getElementById('load').classList.add('off')},350); });
setTimeout(function(){var l=document.getElementById('load'); if(l&&!l.classList.contains('off')) l.classList.add('off')},4000);
var nav=document.getElementById('nav');
window.addEventListener('scroll', function(){ nav.classList.toggle('solid', window.scrollY>40); },{passive:true});
var menu=document.getElementById('menu');
var ul=document.querySelector('nav ul');
if(menu){ var closeMenu=function(){ ul.classList.remove('open'); document.body.classList.remove('menu-open'); };
  menu.addEventListener('click', function(e){ e.stopPropagation(); ul.classList.toggle('open'); document.body.classList.toggle('menu-open'); });
  ul.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', closeMenu); });
}
var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){e.target.classList.add('in'); io.unobserve(e.target);} });},{threshold:.12,rootMargin:'0px 0px -50px 0px'});
document.querySelectorAll('[data-reveal]').forEach(function(el){io.observe(el)});
var tabBtns=document.querySelectorAll('.tab[data-tab]');
tabBtns.forEach(function(t){ t.addEventListener('click', function(){
  tabBtns.forEach(function(x){x.classList.remove('on')});
  t.classList.add('on');
  var target=t.getAttribute('data-tab');
  document.querySelectorAll('.tabpane[data-pane]').forEach(function(p){
    var isVisible=p.getAttribute('data-pane')===target;
    p.classList.toggle('on', isVisible);
    p.style.display=isVisible?'':'none';
  });
});});
document.querySelectorAll('.tabpane[data-pane]').forEach(function(p){
  p.style.display=p.classList.contains('on')?'':'none';
});
document.querySelectorAll('.year').forEach(function(y){y.textContent=new Date().getFullYear()});

(function(){
  var imgs=[].slice.call(document.querySelectorAll('.gallery img'));
  if(imgs.length<1) return;
  var lb=document.createElement('div');
  lb.className='lightbox';
  lb.setAttribute('role','dialog');
  lb.setAttribute('aria-label','Image viewer');
  lb.innerHTML='<img alt=""/>'
    +'<button class="lb-close" aria-label="Close">×</button>'
    +'<button class="lb-arrow lb-prev" aria-label="Previous">‹</button>'
    +'<button class="lb-arrow lb-next" aria-label="Next">›</button>'
    +'<span class="lb-count"></span>';
  document.body.appendChild(lb);
  var lbImg=lb.querySelector('img'), count=lb.querySelector('.lb-count');
  var idx=0;
  function show(i){
    idx=(i+imgs.length)%imgs.length;
    lbImg.src=imgs[idx].src;
    lbImg.alt=imgs[idx].alt||'';
    count.textContent=(idx+1)+' / '+imgs.length;
  }
  function open(i){ show(i); lb.classList.add('open'); document.body.classList.add('menu-open'); }
  function close(){ lb.classList.remove('open'); document.body.classList.remove('menu-open'); }
  imgs.forEach(function(img, i){ img.addEventListener('click', function(){ open(i); }); });
  lb.querySelector('.lb-close').addEventListener('click', function(e){ e.stopPropagation(); close(); });
  lb.querySelector('.lb-prev').addEventListener('click', function(e){ e.stopPropagation(); show(idx-1); });
  lb.querySelector('.lb-next').addEventListener('click', function(e){ e.stopPropagation(); show(idx+1); });
  lb.addEventListener('click', function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown', function(e){
    if(!lb.classList.contains('open')) return;
    if(e.key==='Escape') close();
    else if(e.key==='ArrowLeft') show(idx-1);
    else if(e.key==='ArrowRight') show(idx+1);
  });
})();