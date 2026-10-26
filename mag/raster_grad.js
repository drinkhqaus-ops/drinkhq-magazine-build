() => {
  const split = s => { const out=[]; let d=0, cur=''; for (const ch of s) { if(ch==='(')d++; if(ch===')')d--; if(ch===','&&d===0){out.push(cur.trim());cur='';} else cur+=ch; } if(cur.trim())out.push(cur.trim()); return out; };
  let n=0, skipped=0;
  for (const el of document.querySelectorAll('*')) {
    const bi = getComputedStyle(el).backgroundImage;
    if (!bi || !bi.startsWith('linear-gradient(') || bi.indexOf('linear-gradient(',1)>-1 || bi.includes('url(')) { if (bi && bi.includes('gradient') && !bi.startsWith('linear-gradient(')) skipped++; continue; }
    const r = el.getBoundingClientRect(); const w=Math.max(1,Math.round(el.offsetWidth||r.width)), h=Math.max(1,Math.round(el.offsetHeight||r.height));
    if (w<2||h<2) continue;
    let parts = split(bi.slice(16,-1)); let ang=180;
    const p0=parts[0];
    if (/deg$/.test(p0)) { ang=parseFloat(p0); parts.shift(); }
    else if (/^to /.test(p0)) { const m={'to top':0,'to right':90,'to bottom':180,'to left':270}; ang=m[p0]??180; parts.shift(); }
    const stops = [];
    for (const p of parts) { const m = p.match(/^(rgba?\([^)]*\)|transparent|#[0-9a-f]+|[a-z]+)\s*(.*)$/i); if(!m) continue; const pos=(m[2]||'').trim().split(/\s+/).filter(Boolean); if(pos.length===0) stops.push([m[1],null]); else for (const q of pos) stops.push([m[1], q.endsWith('%')?parseFloat(q)/100:null]); }
    if (stops.length<2) continue;
    if (stops[0][1]===null) stops[0][1]=0; if (stops[stops.length-1][1]===null) stops[stops.length-1][1]=1;
    for (let i=1;i<stops.length;i++){ if(stops[i][1]===null){ let j=i; while(stops[j][1]===null) j++; const a=stops[i-1][1], b=stops[j][1]; for(let k=i;k<j;k++) stops[k][1]=a+(b-a)*(k-i+1)/(j-i+1); } if(stops[i][1]<stops[i-1][1]) stops[i][1]=stops[i-1][1]; }
    const S=1.5, c=document.createElement('canvas'); c.width=w*S; c.height=h*S; const g=c.getContext('2d');
    const a=ang*Math.PI/180, L=Math.abs(w*Math.sin(a))+Math.abs(h*Math.cos(a)), cx=w/2, cy=h/2, dx=Math.sin(a), dy=-Math.cos(a);
    const gr=g.createLinearGradient((cx-dx*L/2)*S,(cy-dy*L/2)*S,(cx+dx*L/2)*S,(cy+dy*L/2)*S);
    for (const [col,pos] of stops) gr.addColorStop(Math.min(1,Math.max(0,pos)), col==='transparent'?'rgba(0,0,0,0)':col);
    g.fillStyle=gr; g.fillRect(0,0,c.width,c.height);
    el.style.backgroundImage=`url(${c.toDataURL('image/png')})`; el.style.backgroundSize='100% 100%'; el.style.backgroundRepeat='no-repeat'; n++;
  }
  return [n, skipped];
}
