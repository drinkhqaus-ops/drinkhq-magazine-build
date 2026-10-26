(function(){
  var body=document.body, editing=false;
  var picker=document.createElement('input'); picker.type='file'; picker.accept='image/*'; picker.hidden=true; body.appendChild(picker);
  var target=null;
  function setEdit(on){
    editing=on; body.classList.toggle('editing',on);
    document.getElementById('bEdit').classList.toggle('on',on);
    document.getElementById('bEdit').textContent=on?'Stop editing':'Edit text & images';
    document.querySelectorAll('.page .safe, .page .cv-lines, .page .cv-date, .page .cv-top, .page .cv-free, .page .folio').forEach(function(el){el.contentEditable=on?'true':'false';});
  }
  document.getElementById('bEdit').onclick=function(){setEdit(!editing);};
  document.getElementById('bBleed').onclick=function(){var on=body.classList.toggle('bleed');this.classList.toggle('on',on);this.textContent=on?'Hide bleed':'Show bleed';};
  document.addEventListener('click',function(e){
    if(!editing) return;
    var ad=e.target.closest('.ad'); var pic=e.target.closest('.pic');
    if(ad){target={ad:ad};picker.click();e.preventDefault();return;}
    if(pic){target={pic:pic};picker.click();e.preventDefault();}
  },true);
  picker.onchange=function(){
    var f=picker.files[0]; if(!f||!target) return;
    var r=new FileReader(); r.onload=function(){
      if(target.ad){var im=target.ad.querySelector('.adart'); im.src=r.result; im.hidden=false; target.ad.classList.add('has-art');}
      else {target.pic.src=r.result; var tag=target.pic.parentNode.querySelector('.imgtag'); if(tag) tag.remove();}
      picker.value='';
    }; r.readAsDataURL(f);
  };
  document.getElementById('bSave').onclick=function(){
    var was=editing; setEdit(false);
    var html='<!doctype html>\n'+document.documentElement.outerHTML;
    if(was) setEdit(true);
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([html],{type:'text/html'}));
    var t=document.title.replace(/\s+/g,'-'); a.download=t+'_edited.html'; a.click();
  };

  // ---- two print modes ----
  function emailStyle(on){
    var s=document.getElementById('emailPrint');
    if(on&&!s){s=document.createElement('style');s.id='emailPrint';
      s.textContent='@page{size:148mm 210mm;margin:0}@media print{.sheet{width:148mm!important;height:210mm!important}.clip{left:-3mm!important;top:-3mm!important}.sheet::before,.sheet::after{display:none!important}}';
      document.head.appendChild(s);}
    if(!on&&s) s.remove();
  }
  var swapped=[];
  function shrinkImages(dpi){
    swapped=[];
    document.querySelectorAll('.page img').forEach(function(im){
      if(!im.naturalWidth||im.hidden) return;
      var r=im.getBoundingClientRect(); if(!r.width||!r.height) return;
      var s=Math.max(r.width/im.naturalWidth, r.height/im.naturalHeight); // css px per source px (cover)
      var k=Math.min(1, s*dpi/96); if(k>0.92) return;
      var c=document.createElement('canvas'); c.width=Math.max(1,Math.round(im.naturalWidth*k)); c.height=Math.max(1,Math.round(im.naturalHeight*k));
      var x=c.getContext('2d'); x.imageSmoothingQuality='high'; x.drawImage(im,0,0,c.width,c.height);
      var png=/^data:image\/png/.test(im.src)||/\.png/i.test(im.src);
      try{ var d=png?c.toDataURL('image/png'):c.toDataURL('image/jpeg',0.82); swapped.push([im,im.src]); im.src=d; }catch(err){}
    });
  }
  function restore(){ swapped.forEach(function(p){p[0].src=p[1];}); swapped=[]; emailStyle(false); }
  window.addEventListener('afterprint', restore);
  document.getElementById('bPress').onclick=function(){ emailStyle(false); window.print(); };
  document.getElementById('bEmail').onclick=function(){ emailStyle(true); shrinkImages(180); setTimeout(function(){ window.print(); }, 400); };
})();
