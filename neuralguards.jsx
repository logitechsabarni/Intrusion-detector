import { useState, useEffect, useRef, useCallback } from "react";

const ATTACK_TYPES = ['Normal','DoS','Probe','R2L','U2R','DDoS','SQL Injection','Port Scan','Brute Force','MITM','Ransomware','Zero-Day'];
const PROTOCOLS = ['tcp','udp','icmp','http','https'];
const SERVICES = ['http','ftp','ssh','smtp','dns','https','telnet','pop3','irc','snmp'];
const FLAGS = ['SF','S0','REJ','RSTO','SH','S1','S2','S3','OTH','RSTOS0'];
const COUNTRIES = ['US','CN','RU','DE','BR','IN','KR','JP','GB','UA','IR','NG','FR','NL','CA'];
const COLOR_MAP = {Normal:'#00ff88',DoS:'#ff2d55',Probe:'#00d4ff',R2L:'#ff8c00',U2R:'#b96dff',DDoS:'#ef4444','SQL Injection':'#ffd60a','Port Scan':'#06b6d4','Brute Force':'#f97316',MITM:'#ec4899',Ransomware:'#dc2626','Zero-Day':'#7c3aed'};
const SEV_MAP = {Normal:'clean',DoS:'critical',DDoS:'critical',U2R:'critical',Ransomware:'critical','Zero-Day':'critical',R2L:'high','SQL Injection':'high','Brute Force':'high',MITM:'high',Probe:'medium','Port Scan':'medium'};
const SEV_COLOR = {critical:'#ff2d55',high:'#ff8c00',medium:'#ffd60a',low:'#00d4ff',clean:'#00ff88'};

function rng(seed){let s=seed;return()=>{s=(s*1664525+1013904223)&0xffffffff;return(s>>>0)/0xffffffff;};}

function genData(n=600){
  const r=rng(42);
  const probs=[0.52,0.07,0.06,0.05,0.03,0.06,0.04,0.03,0.04,0.03,0.03,0.04];
  const cumProbs=probs.reduce((a,p,i)=>[...a,(a[i-1]||0)+p],[]);
  const pick=(arr)=>arr[Math.floor(r()*arr.length)];
  const pickWeighted=()=>{const v=r();return ATTACK_TYPES[cumProbs.findIndex(c=>v<c)]||ATTACK_TYPES[0];};
  const now=Date.now();
  return Array.from({length:n},(_,i)=>{
    const label=pickWeighted();
    const sev=SEV_MAP[label]||'low';
    const risk=Math.min(100,({critical:75,high:50,medium:30,low:10,clean:0}[sev]||0)+Math.floor(r()*26));
    return {
      id:i,
      duration:r()*100,
      protocol:pick(PROTOCOLS),
      service:pick(SERVICES),
      flag:pick(FLAGS),
      src_bytes:Math.floor(r()*50000),
      dst_bytes:Math.floor(r()*30000),
      count:Math.floor(r()*512)+1,
      srv_count:Math.floor(r()*512)+1,
      same_srv_rate:r(),
      diff_srv_rate:r(),
      src_ip:`${Math.floor(r()*223)+1}.${Math.floor(r()*255)}.${Math.floor(r()*255)}.${Math.floor(r()*254)+1}`,
      dst_ip:`10.0.${Math.floor(r()*255)}.${Math.floor(r()*254)+1}`,
      port:Math.floor(r()*65535)+1,
      packet_size:Math.floor(r()*8000)+64,
      ttl:[32,64,128,255][Math.floor(r()*4)],
      country:pick(COUNTRIES),
      label,sev,risk,
      is_attack:label!=='Normal'?1:0,
      timestamp:new Date(now-(n-i)*8000-Math.floor(r()*5000)),
    };
  });
}

const DATA=genData(600);

function useCountUp(target,duration=800){
  const [val,setVal]=useState(0);
  useEffect(()=>{
    let start=null;
    const from=0;
    const step=ts=>{
      if(!start)start=ts;
      const p=Math.min((ts-start)/duration,1);
      setVal(Math.floor(from+(target-from)*p));
      if(p<1)requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  },[target]);
  return val;
}

const css=`
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@300;400;600&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg0:#010912;--bg1:#040f1e;--bg2:#071628;--bg3:#091d34;
  --cyan:#00d4ff;--green:#00ff88;--red:#ff2d55;--orange:#ff8c00;
  --purple:#b96dff;--yellow:#ffd60a;--pink:#ff375f;
  --txt:#dde6f0;--muted:#4a6080;--border:rgba(0,212,255,0.12);
}
body{background:var(--bg0);color:var(--txt);font-family:'JetBrains Mono',monospace;overflow-x:hidden;}
.app{display:flex;min-height:100vh;}
.sidebar{width:200px;min-width:200px;background:var(--bg1);border-right:1px solid var(--border);padding:12px 0;display:flex;flex-direction:column;gap:0;}
.logo{font-family:'Orbitron',monospace;font-size:13px;font-weight:900;background:linear-gradient(90deg,var(--cyan),var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;text-align:center;padding:12px 8px 4px;letter-spacing:2px;}
.logo-sub{font-size:8px;color:#1e3a5f;text-align:center;letter-spacing:2px;margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid var(--border);}
.nav-item{display:flex;align-items:center;gap:8px;padding:8px 14px;font-size:11px;color:var(--muted);cursor:pointer;transition:all 0.2s;border-left:2px solid transparent;letter-spacing:0.5px;}
.nav-item:hover{color:var(--txt);background:rgba(0,212,255,0.05);}
.nav-item.active{color:var(--cyan);background:rgba(0,212,255,0.08);border-left-color:var(--cyan);}
.sidebar-footer{margin-top:auto;padding:12px 14px;border-top:1px solid var(--border);}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;margin-right:6px;animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
.main{flex:1;overflow-x:hidden;display:flex;flex-direction:column;}
.topbar{background:var(--bg1);border-bottom:1px solid var(--border);padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px;}
.topbar-title{font-family:'Orbitron',monospace;font-size:14px;color:var(--cyan);letter-spacing:2px;}
.topbar-right{display:flex;align-items:center;gap:16px;font-size:11px;color:var(--muted);}
.content{padding:16px 20px;flex:1;}
.page-title{font-family:'Orbitron',monospace;font-size:11px;color:var(--cyan);letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--border);}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px;}
.grid-6{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:14px;}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px;}
.metric-val{font-family:'Orbitron',monospace;font-size:22px;font-weight:700;line-height:1;}
.metric-lbl{font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;}
.metric-sub{font-size:10px;margin-top:4px;}
.card-title{font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'Orbitron',monospace;}
.badge{display:inline-block;padding:2px 7px;border-radius:20px;font-size:9px;font-weight:600;text-transform:uppercase;}
.badge-critical{background:rgba(255,45,85,0.18);color:#ff2d55;border:1px solid rgba(255,45,85,0.4);}
.badge-high{background:rgba(255,140,0,0.18);color:#ff8c00;border:1px solid rgba(255,140,0,0.4);}
.badge-medium{background:rgba(255,214,10,0.18);color:#ffd60a;border:1px solid rgba(255,214,10,0.4);}
.badge-low{background:rgba(0,212,255,0.18);color:#00d4ff;border:1px solid rgba(0,212,255,0.4);}
.badge-clean{background:rgba(0,255,136,0.18);color:#00ff88;border:1px solid rgba(0,255,136,0.4);}
.alert-item{border-left:3px solid;border-radius:0 6px 6px 0;padding:8px 12px;margin-bottom:5px;font-size:10.5px;animation:fadeIn 0.3s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateX(-6px);}to{opacity:1;transform:translateX(0);}}
.alert-item.critical{border-color:#ff2d55;background:rgba(255,45,85,0.06);}
.alert-item.high{border-color:#ff8c00;background:rgba(255,140,0,0.06);}
.alert-item.medium{border-color:#ffd60a;background:rgba(255,214,10,0.04);}
.alert-item.low{border-color:#00d4ff;background:rgba(0,212,255,0.04);}
.alert-item.clean{border-color:#00ff88;background:rgba(0,255,136,0.04);}
.mini-bar-wrap{margin-bottom:8px;}
.mini-bar-track{height:5px;background:rgba(255,255,255,0.05);border-radius:3px;overflow:hidden;}
.mini-bar-fill{height:100%;border-radius:3px;transition:width 0.6s ease;}
.tab-row{display:flex;gap:4px;margin-bottom:12px;background:var(--bg1);padding:4px;border-radius:8px;}
.tab{padding:5px 12px;border-radius:6px;font-size:11px;cursor:pointer;color:var(--muted);transition:all 0.2s;border:none;background:none;}
.tab.active{background:var(--bg3);color:var(--cyan);}
.table-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;font-size:10.5px;}
th{color:var(--muted);font-weight:600;padding:6px 8px;text-align:left;border-bottom:1px solid var(--border);letter-spacing:0.5px;}
td{padding:5px 8px;border-bottom:1px solid rgba(0,212,255,0.04);color:var(--txt);}
tr:hover td{background:rgba(0,212,255,0.03);}
.terminal{background:#000d1a;border:1px solid rgba(0,212,255,0.2);border-radius:8px;padding:12px;font-size:11px;line-height:1.8;max-height:280px;overflow-y:auto;color:#00ff88;}
.terminal::-webkit-scrollbar{width:3px;}
.terminal::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.2);}
.filter-row{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;align-items:center;}
select,input[type=text],input[type=number]{background:var(--bg3);border:1px solid var(--border);color:var(--txt);border-radius:6px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:11px;outline:none;}
select:focus,input:focus{border-color:var(--cyan);}
input[type=range]{accent-color:var(--cyan);}
button{background:rgba(0,212,255,0.08);border:1px solid var(--cyan);color:var(--cyan);border-radius:6px;padding:6px 14px;font-family:'JetBrains Mono',monospace;font-size:11px;cursor:pointer;transition:all 0.2s;}
button:hover{background:rgba(0,212,255,0.18);color:var(--green);border-color:var(--green);}
button.danger{border-color:var(--red);color:var(--red);background:rgba(255,45,85,0.08);}
button.success{border-color:var(--green);color:var(--green);background:rgba(0,255,136,0.08);}
.threat-card{background:var(--bg2);border:1px solid;border-radius:8px;padding:12px;margin-bottom:8px;}
.scroll-box{max-height:360px;overflow-y:auto;padding-right:4px;}
.scroll-box::-webkit-scrollbar{width:3px;}
.scroll-box::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.kpi-glow-cyan{color:var(--cyan);}
.kpi-glow-green{color:var(--green);}
.kpi-glow-red{color:var(--red);}
.kpi-glow-orange{color:var(--orange);}
.kpi-glow-purple{color:var(--purple);}
.kpi-glow-yellow{color:var(--yellow);}
.live-dot{width:8px;height:8px;border-radius:50%;background:var(--red);display:inline-block;margin-right:6px;animation:pulse 0.8s ease-in-out infinite;}
.progress-ring{transform:rotate(-90deg);}
.tooltip{position:relative;display:inline-block;}
.tooltip:hover .tip{display:block;}
.tip{display:none;position:absolute;bottom:120%;left:50%;transform:translateX(-50%);background:var(--bg3);border:1px solid var(--border);padding:6px 10px;border-radius:6px;font-size:10px;white-space:nowrap;z-index:100;}
.sparkline{display:inline-flex;align-items:flex-end;gap:2px;height:24px;}
.spark-bar{width:4px;border-radius:1px;background:var(--cyan);opacity:0.7;}
`;

function MiniSparkline({data,color='#00d4ff'}){
  const max=Math.max(...data,1);
  return(
    <div className="sparkline">
      {data.map((v,i)=>(
        <div key={i} className="spark-bar" style={{height:`${(v/max)*100}%`,background:color,opacity:0.5+0.5*(v/max)}}/>
      ))}
    </div>
  );
}

function DonutChart({data,size=120}){
  const total=data.reduce((s,d)=>s+d.value,0);
  let cum=0;
  const slices=data.map(d=>{
    const start=cum/total*360;
    const end=(cum+d.value)/total*360;
    cum+=d.value;
    const r=size/2-8;
    const cx=size/2,cy=size/2;
    const toRad=deg=>deg*Math.PI/180;
    const x1=cx+r*Math.cos(toRad(start-90));
    const y1=cy+r*Math.sin(toRad(start-90));
    const x2=cx+r*Math.cos(toRad(end-90));
    const y2=cy+r*Math.sin(toRad(end-90));
    const large=end-start>180?1:0;
    return{...d,d:`M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${large},1 ${x2},${y2} Z`,start,end};
  });
  return(
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={size/2-8} fill="rgba(4,15,30,0.8)" stroke="none"/>
      {slices.map((s,i)=>(
        <path key={i} d={s.d} fill={s.color} opacity={0.85} stroke="#010912" strokeWidth="1.5"/>
      ))}
      <circle cx={size/2} cy={size/2} r={size/2-24} fill="#010912"/>
    </svg>
  );
}

function BarChart({data,horizontal=false,height=160,colorFn}){
  if(!data||data.length===0)return null;
  const max=Math.max(...data.map(d=>d.value),1);
  if(horizontal){
    return(
      <div style={{display:'flex',flexDirection:'column',gap:6,height}}>
        {data.slice(0,8).map((d,i)=>{
          const pct=(d.value/max)*100;
          const color=colorFn?colorFn(d,i):(SEV_COLOR[d.label]||'#00d4ff');
          return(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,fontSize:10}}>
              <div style={{width:80,color:'#4a6080',textAlign:'right',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{d.label}</div>
              <div style={{flex:1,background:'rgba(255,255,255,0.04)',borderRadius:3,height:14,overflow:'hidden'}}>
                <div style={{width:`${pct}%`,height:'100%',background:color,borderRadius:3,transition:'width 0.5s ease'}}/>
              </div>
              <div style={{width:36,color,textAlign:'right'}}>{d.value}</div>
            </div>
          );
        })}
      </div>
    );
  }
  return(
    <div style={{display:'flex',alignItems:'flex-end',gap:4,height,padding:'0 4px'}}>
      {data.map((d,i)=>{
        const pct=(d.value/max)*100;
        const color=colorFn?colorFn(d,i):(COLOR_MAP[d.label]||'#00d4ff');
        return(
          <div key={i} style={{flex:1,display:'flex',flexDirection:'column',alignItems:'center',gap:3}}>
            <div style={{fontSize:8,color:'#4a6080'}}>{d.value}</div>
            <div style={{width:'100%',background:color,borderRadius:'2px 2px 0 0',height:`${pct}%`,minHeight:2,transition:'height 0.5s ease',opacity:0.85}}/>
            <div style={{fontSize:8,color:'#4a6080',textAlign:'center',writingMode:'vertical-rl',transform:'rotate(180deg)',height:40,overflow:'hidden'}}>{d.label}</div>
          </div>
        );
      })}
    </div>
  );
}

function LineChart({series,height=120,showGrid=true}){
  if(!series||series.length===0)return null;
  const allVals=series.flatMap(s=>s.data);
  const max=Math.max(...allVals,1);
  const w=400,h=height;
  const pad={t:8,r:8,b:20,l:32};
  const chartW=w-pad.l-pad.r;
  const chartH=h-pad.t-pad.b;
  const toX=(i,len)=>pad.l+i/(Math.max(len-1,1))*chartW;
  const toY=(v)=>pad.t+chartH-(v/max)*chartH;
  return(
    <svg viewBox={`0 0 ${w} ${h}`} style={{width:'100%',height}} preserveAspectRatio="none">
      {showGrid&&[0.25,0.5,0.75,1].map(pct=>(
        <line key={pct} x1={pad.l} y1={toY(max*pct)} x2={w-pad.r} y2={toY(max*pct)} stroke="rgba(0,212,255,0.06)" strokeWidth="1"/>
      ))}
      {series.map((s,si)=>{
        const pts=s.data.map((v,i)=>`${toX(i,s.data.length)},${toY(v)}`).join(' ');
        const fill=s.data.map((v,i)=>`${toX(i,s.data.length)},${toY(v)}`).join(' ');
        const fillPath=`M ${toX(0,s.data.length)},${toY(0)} L ${fill} L ${toX(s.data.length-1,s.data.length)},${toY(0)} Z`;
        return(
          <g key={si}>
            <path d={fillPath} fill={s.color} fillOpacity={0.1} strokeWidth={0}/>
            <polyline points={pts} fill="none" stroke={s.color} strokeWidth="1.5" strokeLinejoin="round"/>
          </g>
        );
      })}
    </svg>
  );
}

function ScatterPlot({data,height=180}){
  if(!data||data.length===0)return null;
  const xs=data.map(d=>d.x),ys=data.map(d=>d.y);
  const xmax=Math.max(...xs,1),ymax=Math.max(...ys,1);
  const w=400,h=height;
  const pad={t:8,r:8,b:20,l:32};
  return(
    <svg viewBox={`0 0 ${w} ${h}`} style={{width:'100%',height}} preserveAspectRatio="xMidYMid meet">
      <line x1={pad.l} y1={pad.t} x2={pad.l} y2={h-pad.b} stroke="rgba(0,212,255,0.15)" strokeWidth="1"/>
      <line x1={pad.l} y1={h-pad.b} x2={w-pad.r} y2={h-pad.b} stroke="rgba(0,212,255,0.15)" strokeWidth="1"/>
      {data.map((d,i)=>{
        const cx=pad.l+(d.x/xmax)*(w-pad.l-pad.r);
        const cy=h-pad.b-(d.y/ymax)*(h-pad.t-pad.b);
        return<circle key={i} cx={cx} cy={cy} r={3} fill={d.color||'#00d4ff'} opacity={0.6}/>;
      })}
    </svg>
  );
}

function Heatmap({rows,cols,data,height=200}){
  if(!rows||!cols||!data)return null;
  const flat=data.flat();
  const max=Math.max(...flat,1);
  const cellH=Math.max(16,(height-40)/rows.length);
  const cellW=`${100/cols.length}%`;
  return(
    <div style={{fontSize:9,color:'#4a6080'}}>
      <div style={{display:'flex',marginLeft:60,marginBottom:2}}>
        {cols.map((c,i)=><div key={i} style={{flex:1,textAlign:'center',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap',padding:'0 1px'}}>{c.substring(0,6)}</div>)}
      </div>
      {rows.map((row,ri)=>(
        <div key={ri} style={{display:'flex',alignItems:'center',marginBottom:1}}>
          <div style={{width:60,textAlign:'right',paddingRight:6,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{row.substring(0,8)}</div>
          {cols.map((col,ci)=>{
            const v=data[ri][ci]||0;
            const pct=v/max;
            const alpha=0.05+pct*0.9;
            return<div key={ci} style={{flex:1,height:cellH,background:`rgba(0,212,255,${alpha})`,border:'1px solid rgba(0,212,255,0.05)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:8,color:pct>0.5?'#00d4ff':'#2a4a6a'}}>{v>0?v:''}</div>;
          })}
        </div>
      ))}
    </div>
  );
}

function RadarChart({data,size=160}){
  const n=data.length;
  const cx=size/2,cy=size/2,r=size/2-24;
  const angle=i=>i*(2*Math.PI/n)-Math.PI/2;
  const pt=(i,scale)=>({x:cx+r*scale*Math.cos(angle(i)),y:cy+r*scale*Math.sin(angle(i))});
  const rings=[0.25,0.5,0.75,1];
  return(
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {rings.map(s=>(
        <polygon key={s} points={data.map((_,i)=>{const p=pt(i,s);return`${p.x},${p.y}`;}).join(' ')} fill="none" stroke="rgba(0,212,255,0.1)" strokeWidth="1"/>
      ))}
      {data.map((_,i)=>{const p=pt(i,1);return<line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="rgba(0,212,255,0.1)" strokeWidth="1"/>;})
      }
      <polygon points={data.map((d,i)=>{const p=pt(i,d.value);return`${p.x},${p.y}`;}).join(' ')} fill="rgba(0,212,255,0.15)" stroke="var(--cyan)" strokeWidth="1.5"/>
      {data.map((d,i)=>{const p=pt(i,1);const tp=pt(i,1.25);return<text key={i} x={tp.x} y={tp.y} fill="#4a6080" fontSize="9" textAnchor="middle" dominantBaseline="central">{d.label}</text>;})}
    </svg>
  );
}

function NetworkGraph({data,size=360}){
  const nodes=[];const edges=[];
  const seen=new Set();
  data.slice(0,30).forEach(d=>{
    if(!seen.has(d.src_ip)){seen.add(d.src_ip);nodes.push({id:d.src_ip,type:'src',color:SEV_COLOR[d.sev]||'#ff2d55'});}
    if(!seen.has(d.dst_ip)){seen.add(d.dst_ip);nodes.push({id:d.dst_ip,type:'dst',color:'#00d4ff'});}
    edges.push({s:d.src_ip,t:d.dst_ip,color:SEV_COLOR[d.sev]||'#ff2d55'});
  });
  const r=rng(99);
  const pos={};
  nodes.forEach((n,i)=>{
    const angle=(i/nodes.length)*2*Math.PI;
    const rad=size/2*0.38*(0.6+r()*0.4);
    pos[n.id]={x:size/2+rad*Math.cos(angle),y:size/2+rad*Math.sin(angle)};
  });
  return(
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{background:'rgba(4,15,30,0.5)',borderRadius:8}}>
      {edges.map((e,i)=>{
        const s=pos[e.s],t=pos[e.t];
        if(!s||!t)return null;
        return<line key={i} x1={s.x} y1={s.y} x2={t.x} y2={t.y} stroke={e.color} strokeOpacity={0.3} strokeWidth="1"/>;
      })}
      {nodes.map((n,i)=>{
        const p=pos[n.id];if(!p)return null;
        return<g key={i}><circle cx={p.x} cy={p.y} r={n.type==='src'?5:4} fill={n.color} opacity={0.8}/><text x={p.x} y={p.y-8} fill="#4a6080" fontSize="7" textAnchor="middle">{n.id.split('.').slice(-1)[0]}</text></g>;
      })}
    </svg>
  );
}

function WorldMap({countryData}){
  const POSITIONS={US:[220,110],CN:[540,120],RU:[500,75],DE:[360,90],BR:[220,200],IN:[510,145],KR:[580,110],JP:[600,105],GB:[340,88],UA:[420,88],IR:[470,120],NG:[370,160],FR:[355,95],NL:[358,86],CA:[190,85]};
  return(
    <svg viewBox="0 0 740 380" style={{width:'100%',background:'rgba(4,15,30,0.5)',borderRadius:8}}>
      <rect width="740" height="380" fill="rgba(4,15,30,0.8)" rx="8"/>
      <ellipse cx="370" cy="190" rx="340" ry="170" fill="rgba(0,20,40,0.6)" stroke="rgba(0,212,255,0.08)" strokeWidth="1"/>
      {[[-1,0],[1,0],[0,-1],[0,1]].map(([dx,dy],i)=>(
        <line key={i} x1={30+dx*340} y1={190+dy*170} x2={30+dx*340} y2={190+dy*170} stroke="rgba(0,212,255,0.05)" strokeWidth="1"/>
      ))}
      <line x1="30" y1="190" x2="710" y2="190" stroke="rgba(0,212,255,0.08)" strokeWidth="0.5" strokeDasharray="4,4"/>
      <line x1="370" y1="20" x2="370" y2="360" stroke="rgba(0,212,255,0.08)" strokeWidth="0.5" strokeDasharray="4,4"/>
      {countryData.map((d,i)=>{
        const pos=POSITIONS[d.country];
        if(!pos)return null;
        const r=Math.sqrt(d.count/Math.PI)*0.8+4;
        return(
          <g key={i}>
            <circle cx={pos[0]} cy={pos[1]} r={r} fill={d.color||'#ff2d55'} opacity={0.7} stroke={d.color||'#ff2d55'} strokeOpacity={0.3} strokeWidth="1"/>
            <text x={pos[0]} y={pos[1]+r+10} fill="#4a6080" fontSize="8" textAnchor="middle">{d.country}</text>
          </g>
        );
      })}
    </svg>
  );
}

function DashboardPage({data}){
  const attacks=data.filter(d=>d.is_attack);
  const crits=attacks.filter(d=>d.sev==='critical');
  const highs=attacks.filter(d=>d.sev==='high');
  const attackRate=(attacks.length/data.length*100).toFixed(1);
  const uniqueSrcs=new Set(attacks.map(d=>d.src_ip)).size;

  const buckets=Array.from({length:20},(_,i)=>({normal:0,attack:0}));
  data.forEach(d=>{
    const idx=Math.floor(d.id/data.length*20);
    if(idx<20){if(d.is_attack)buckets[idx].attack++;else buckets[idx].normal++;}
  });

  const typeDist=Object.entries(ATTACK_TYPES.slice(1).reduce((acc,t)=>{
    acc[t]=(data.filter(d=>d.label===t).length);return acc;
  },{})).map(([label,value])=>({label,value,color:COLOR_MAP[label]})).filter(d=>d.value>0);

  const sevCounts=['critical','high','medium','low'].map(s=>({label:s,value:attacks.filter(d=>d.sev===s).length}));

  const recentAlerts=attacks.sort((a,b)=>b.id-a.id).slice(0,12);
  const totalAnim=useCountUp(data.length);
  const attackAnim=useCountUp(attacks.length);

  return(
    <>
      <div className="grid-6">
        {[
          {v:totalAnim,l:'TOTAL PACKETS',s:'Last 24h',c:'var(--cyan)'},
          {v:attackAnim,l:'THREATS DETECTED',s:'Active',c:'var(--red)'},
          {v:`${attackRate}%`,l:'ATTACK RATE',s:'of traffic',c:'var(--orange)'},
          {v:crits.length,l:'CRITICAL',s:`+${highs.length} HIGH`,c:'#ff2d55'},
          {v:uniqueSrcs,l:'UNIQUE SOURCES',s:'tracked IPs',c:'var(--purple)'},
          {v:'94.2%',l:'ML ACCURACY',s:'Random Forest',c:'var(--green)'},
        ].map((m,i)=>(
          <div key={i} className="card" style={{borderBottom:`2px solid ${m.c}`,position:'relative',overflow:'hidden'}}>
            <div style={{position:'absolute',top:0,right:0,width:40,height:40,background:m.c,opacity:0.04,borderRadius:'0 10px 0 40px'}}/>
            <div className="metric-val" style={{color:m.c}}>{m.v}</div>
            <div className="metric-lbl">{m.l}</div>
            <div className="metric-sub" style={{color:m.c+'88'}}>{m.s}</div>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">TRAFFIC STREAM (20 BUCKETS)</div>
          <LineChart series={[
            {data:buckets.map(b=>b.normal),color:'#00ff88'},
            {data:buckets.map(b=>b.attack),color:'#ff2d55'},
          ]} height={130}/>
          <div style={{display:'flex',gap:12,marginTop:6,fontSize:10,color:'#4a6080'}}>
            <span><span style={{color:'#00ff88'}}>■</span> Normal</span>
            <span><span style={{color:'#ff2d55'}}>■</span> Attack</span>
          </div>
        </div>
        <div className="card">
          <div className="card-title">ATTACK DISTRIBUTION</div>
          <div style={{display:'flex',gap:12,alignItems:'center'}}>
            <DonutChart data={typeDist.slice(0,7)} size={110}/>
            <div style={{flex:1}}>
              {typeDist.slice(0,6).map((d,i)=>(
                <div key={i} style={{display:'flex',alignItems:'center',gap:6,marginBottom:4,fontSize:10}}>
                  <div style={{width:8,height:8,borderRadius:2,background:d.color,flexShrink:0}}/>
                  <span style={{color:'#4a6080',flex:1,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{d.label}</span>
                  <span style={{color:d.color}}>{d.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">LATEST ALERTS</div>
          <div className="scroll-box">
            {recentAlerts.map((a,i)=>(
              <div key={i} className={`alert-item ${a.sev}`}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:2}}>
                  <span style={{color:SEV_COLOR[a.sev],fontWeight:600}}>{a.label}</span>
                  <span className={`badge badge-${a.sev}`}>{a.sev}</span>
                </div>
                <div style={{color:'#4a6080',fontSize:10}}>
                  {a.src_ip} → PORT:{a.port} · {a.protocol.toUpperCase()} · RISK:{a.risk} · {a.timestamp.toTimeString().substring(0,8)}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <div className="card-title">SEVERITY BREAKDOWN</div>
          {sevCounts.map((s,i)=>(
            <div key={i} className="mini-bar-wrap">
              <div style={{display:'flex',justifyContent:'space-between',fontSize:10,marginBottom:3}}>
                <span style={{color:SEV_COLOR[s.label]}}>{s.label.toUpperCase()}</span>
                <span style={{color:'#4a6080'}}>{s.value}</span>
              </div>
              <div className="mini-bar-track">
                <div className="mini-bar-fill" style={{width:`${s.value/Math.max(attacks.length,1)*100}%`,background:SEV_COLOR[s.label]}}/>
              </div>
            </div>
          ))}
          <div style={{marginTop:16}} className="card-title">PROTOCOL MIX</div>
          <BarChart data={PROTOCOLS.map(p=>({label:p.toUpperCase(),value:data.filter(d=>d.protocol===p).length}))} height={80} colorFn={(_,i)=>['#00d4ff','#00ff88','#b96dff','#ffd60a','#ff8c00'][i]}/>
        </div>
      </div>
    </>
  );
}

function TrafficPage({data}){
  const [tab,setTab]=useState(0);
  const [protoFilter,setProtoFilter]=useState('all');
  const [sevFilter,setSevFilter]=useState('all');
  const [ipSearch,setIpSearch]=useState('');
  const [rows,setRows]=useState(50);

  const filtered=data.filter(d=>{
    if(protoFilter!=='all'&&d.protocol!==protoFilter)return false;
    if(sevFilter!=='all'&&d.sev!==sevFilter)return false;
    if(ipSearch&&!d.src_ip.includes(ipSearch)&&!d.dst_ip.includes(ipSearch))return false;
    return true;
  });

  const services=SERVICES.slice(0,6);
  const sevs=['critical','high','medium'];
  const heatData=services.map(svc=>sevs.map(sv=>data.filter(d=>d.service===svc&&d.sev===sv).length));

  const scatterData=data.slice(0,200).map(d=>({x:Math.log1p(d.src_bytes),y:Math.log1p(d.dst_bytes),color:COLOR_MAP[d.label]||'#00d4ff'}));

  return(
    <>
      <div className="tab-row">
        {['Overview','Flow Analysis','Packet Inspector'].map((t,i)=>(
          <button key={i} className={`tab${tab===i?' active':''}`} onClick={()=>setTab(i)}>{t}</button>
        ))}
      </div>

      {tab===0&&(
        <>
          <div className="filter-row">
            <select value={protoFilter} onChange={e=>setProtoFilter(e.target.value)}>
              <option value="all">All Protocols</option>
              {PROTOCOLS.map(p=><option key={p} value={p}>{p.toUpperCase()}</option>)}
            </select>
            <select value={sevFilter} onChange={e=>setSevFilter(e.target.value)}>
              <option value="all">All Severities</option>
              {['clean','low','medium','high','critical'].map(s=><option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div className="grid-2">
            <div className="card">
              <div className="card-title">PROTOCOL DISTRIBUTION ({filtered.length} pkts)</div>
              <BarChart data={PROTOCOLS.map(p=>({label:p.toUpperCase(),value:filtered.filter(d=>d.protocol===p).length}))} height={120} colorFn={(_,i)=>['#00d4ff','#00ff88','#b96dff','#ffd60a','#ff8c00'][i]}/>
            </div>
            <div className="card">
              <div className="card-title">SERVICE × SEVERITY HEATMAP</div>
              <Heatmap rows={services} cols={sevs} data={heatData} height={160}/>
            </div>
          </div>
          <div className="card">
            <div className="card-title">SRC vs DST BYTES (log scale)</div>
            <ScatterPlot data={scatterData} height={180}/>
            <div style={{display:'flex',flexWrap:'wrap',gap:8,marginTop:8}}>
              {Object.entries(COLOR_MAP).slice(0,6).map(([k,v])=>(
                <span key={k} style={{fontSize:9,color:'#4a6080',display:'flex',alignItems:'center',gap:4}}>
                  <span style={{width:8,height:8,borderRadius:2,background:v,display:'inline-block'}}/>
                  {k}
                </span>
              ))}
            </div>
          </div>
        </>
      )}

      {tab===1&&(
        <div className="grid-2">
          <div className="card">
            <div className="card-title">AVG BYTES BY ATTACK TYPE</div>
            <BarChart
              data={ATTACK_TYPES.slice(0,8).map(t=>({label:t,value:Math.floor(data.filter(d=>d.label===t).reduce((s,d)=>s+d.src_bytes,0)/Math.max(data.filter(d=>d.label===t).length,1))}))}
              height={140}
              colorFn={(d)=>COLOR_MAP[d.label]||'#00d4ff'}
            />
          </div>
          <div className="card">
            <div className="card-title">FLAG DISTRIBUTION</div>
            <BarChart
              data={FLAGS.slice(0,8).map(f=>({label:f,value:data.filter(d=>d.flag===f).length}))}
              height={140}
              colorFn={(_,i)=>['#00d4ff','#00ff88','#b96dff','#ffd60a','#ff8c00','#ff2d55','#ec4899','#06b6d4'][i]}
            />
          </div>
          <div className="card">
            <div className="card-title">ATTACKS BY COUNTRY (TOP 10)</div>
            <BarChart
              data={COUNTRIES.map(c=>({label:c,value:data.filter(d=>d.country===c&&d.is_attack).length})).sort((a,b)=>b.value-a.value).slice(0,8)}
              horizontal={true} height={180}
              colorFn={()=>'#ff2d55'}
            />
          </div>
          <div className="card">
            <div className="card-title">PORT RANGE ANALYSIS</div>
            <BarChart
              data={[
                {label:'Well-Known (0-1023)',value:data.filter(d=>d.port<=1023).length},
                {label:'Registered (1024-49151)',value:data.filter(d=>d.port>1023&&d.port<=49151).length},
                {label:'Dynamic (49152+)',value:data.filter(d=>d.port>49151).length},
              ]}
              height={140}
              colorFn={(_,i)=>['#00d4ff','#00ff88','#b96dff'][i]}
            />
          </div>
        </div>
      )}

      {tab===2&&(
        <>
          <div className="filter-row">
            <input type="text" placeholder="Filter by IP..." value={ipSearch} onChange={e=>setIpSearch(e.target.value)} style={{width:200}}/>
            <select value={rows} onChange={e=>setRows(Number(e.target.value))}>
              {[50,100,200].map(n=><option key={n} value={n}>Show {n}</option>)}
            </select>
            <span style={{color:'#4a6080',fontSize:11}}>{filtered.length} packets</span>
          </div>
          <div className="card table-wrap">
            <table>
              <thead>
                <tr><th>Time</th><th>Src IP</th><th>Dst IP</th><th>Proto</th><th>Service</th><th>Port</th><th>Src Bytes</th><th>Dst Bytes</th><th>Type</th><th>Severity</th><th>Risk</th></tr>
              </thead>
              <tbody>
                {filtered.slice(-rows).reverse().map((d,i)=>(
                  <tr key={i}>
                    <td style={{color:'#4a6080'}}>{d.timestamp.toTimeString().substring(0,8)}</td>
                    <td style={{color:d.is_attack?'#ff2d55':'#00ff88'}}>{d.src_ip}</td>
                    <td style={{color:'#4a6080'}}>{d.dst_ip}</td>
                    <td style={{color:'#00d4ff'}}>{d.protocol.toUpperCase()}</td>
                    <td style={{color:'#4a6080'}}>{d.service}</td>
                    <td>{d.port}</td>
                    <td>{d.src_bytes.toLocaleString()}</td>
                    <td>{d.dst_bytes.toLocaleString()}</td>
                    <td style={{color:COLOR_MAP[d.label]||'#00d4ff'}}>{d.label}</td>
                    <td><span className={`badge badge-${d.sev}`}>{d.sev}</span></td>
                    <td style={{color:SEV_COLOR[d.sev]}}>{d.risk}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  );
}

function MLPage({data}){
  const [tab,setTab]=useState(0);
  const [pktInputs,setPktInputs]=useState({src_bytes:1500,dst_bytes:500,port:80,duration:5,count:10,risk_score:20});
  const [prediction,setPrediction]=useState(null);

  const models=[
    {name:'Random Forest',acc:94.2,prec:93.8,rec:94.0,f1:93.9,color:'#00ff88'},
    {name:'Gradient Boosting',acc:92.7,prec:92.1,rec:92.5,f1:92.3,color:'#00d4ff'},
    {name:'Neural Network',acc:91.3,prec:90.8,rec:91.0,f1:90.9,color:'#b96dff'},
  ];

  const features=[
    {name:'src_bytes',importance:0.182},{name:'dst_bytes',importance:0.155},{name:'risk_score',importance:0.143},
    {name:'count',importance:0.121},{name:'port',importance:0.098},{name:'packet_size',importance:0.087},
    {name:'duration',importance:0.074},{name:'srv_count',importance:0.062},{name:'same_srv_rate',importance:0.048},
    {name:'diff_srv_rate',importance:0.030},
  ].sort((a,b)=>a.importance-b.importance);

  const classMetrics=ATTACK_TYPES.map(t=>({
    name:t,
    count:data.filter(d=>d.label===t).length,
    precision:(Math.random()*0.15+0.82).toFixed(3),
    recall:(Math.random()*0.15+0.80).toFixed(3),
    f1:(Math.random()*0.15+0.81).toFixed(3),
  }));

  const classifyPacket=()=>{
    const risk=pktInputs.risk_score;
    const suspicious=pktInputs.src_bytes>20000||pktInputs.port<1024&&pktInputs.count>100||risk>60;
    const label=risk>70?'DoS':risk>55?'Port Scan':risk>40?'Probe':risk>25?'Brute Force':'Normal';
    const conf=75+Math.random()*20;
    setPrediction({label,conf:conf.toFixed(1),is_attack:label!=='Normal',probs:ATTACK_TYPES.map(t=>({t,p:t===label?conf/100:(Math.random()*0.15)})).sort((a,b)=>b.p-a.p)});
  };

  return(
    <>
      <div className="tab-row">
        {['Model Comparison','Confusion Matrix','Feature Importance','Live Prediction'].map((t,i)=>(
          <button key={i} className={`tab${tab===i?' active':''}`} onClick={()=>setTab(i)}>{t}</button>
        ))}
      </div>

      {tab===0&&(
        <>
          <div className="grid-3">
            {models.map((m,i)=>(
              <div key={i} className="card" style={{borderTop:`2px solid ${m.color}`,position:'relative'}}>
                {i===0&&<div style={{position:'absolute',top:8,right:8,fontSize:9,color:'#ffd60a'}}>★ BEST</div>}
                <div style={{fontFamily:'Orbitron,monospace',fontSize:12,color:m.color,marginBottom:10}}>{m.name}</div>
                {[['ACCURACY',m.acc],['PRECISION',m.prec],['RECALL',m.rec],['F1 SCORE',m.f1]].map(([k,v])=>(
                  <div key={k} className="mini-bar-wrap">
                    <div style={{display:'flex',justifyContent:'space-between',fontSize:10,marginBottom:2}}>
                      <span style={{color:'#4a6080'}}>{k}</span>
                      <span style={{color:m.color}}>{v}%</span>
                    </div>
                    <div className="mini-bar-track">
                      <div className="mini-bar-fill" style={{width:`${v}%`,background:m.color}}/>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="card">
            <div className="card-title">CROSS-VALIDATION SCORES (5-FOLD)</div>
            <LineChart series={[
              {data:[93.2,94.8,93.9,95.1,94.2],color:'#00ff88'},
              {data:[91.8,92.9,92.4,93.1,92.7],color:'#00d4ff'},
              {data:[90.5,91.8,91.2,92.0,91.3],color:'#b96dff'},
            ]} height={120}/>
            <div style={{display:'flex',gap:16,marginTop:8,fontSize:10,color:'#4a6080'}}>
              {models.map(m=><span key={m.name}><span style={{color:m.color}}>■</span> {m.name}</span>)}
            </div>
          </div>
        </>
      )}

      {tab===1&&(
        <div className="card">
          <div className="card-title">CONFUSION MATRIX — RANDOM FOREST</div>
          <div style={{overflowX:'auto'}}>
            <table style={{minWidth:500}}>
              <thead>
                <tr><th>Actual\Pred</th>{ATTACK_TYPES.map(t=><th key={t} style={{fontSize:8,writingMode:'vertical-rl',transform:'rotate(180deg)',height:60}}>{t}</th>)}</tr>
              </thead>
              <tbody>
                {ATTACK_TYPES.map((row,ri)=>(
                  <tr key={ri}>
                    <td style={{color:COLOR_MAP[row]||'#00d4ff',fontSize:10,whiteSpace:'nowrap'}}>{row}</td>
                    {ATTACK_TYPES.map((col,ci)=>{
                      const isMatch=row===col;
                      const base=data.filter(d=>d.label===row).length;
                      const val=isMatch?Math.floor(base*0.92):Math.floor(base*(0.02+Math.random()*0.04));
                      const alpha=Math.min(1,val/50);
                      return<td key={ci} style={{background:isMatch?`rgba(0,255,136,${alpha*0.5})`:`rgba(255,45,85,${alpha*0.3})`,textAlign:'center',fontSize:9,color:isMatch?'#00ff88':'#ff2d55'}}>{val}</td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab===2&&(
        <div className="grid-2">
          <div className="card">
            <div className="card-title">FEATURE IMPORTANCE (RANDOM FOREST)</div>
            <BarChart data={features.map(f=>({label:f.name,value:Math.floor(f.importance*1000)}))} horizontal={true} height={240} colorFn={(d,i)=>i>features.length-4?'#ff2d55':i>features.length-7?'#00d4ff':'#1e3a5f'}/>
          </div>
          <div className="card">
            <div className="card-title">FEATURE RADAR — TOP 6</div>
            <div style={{display:'flex',justifyContent:'center'}}>
              <RadarChart data={features.slice(-6).map(f=>({label:f.name.substring(0,8),value:f.importance}))} size={200}/>
            </div>
            <div className="card-title" style={{marginTop:16}}>PER-CLASS PERFORMANCE</div>
            <div className="scroll-box" style={{maxHeight:160}}>
              <table>
                <thead><tr><th>Class</th><th>Count</th><th>Precision</th><th>Recall</th><th>F1</th></tr></thead>
                <tbody>
                  {classMetrics.map((m,i)=>(
                    <tr key={i}>
                      <td style={{color:COLOR_MAP[m.name]||'#00d4ff'}}>{m.name}</td>
                      <td style={{color:'#4a6080'}}>{m.count}</td>
                      <td style={{color:'#00d4ff'}}>{m.precision}</td>
                      <td style={{color:'#00ff88'}}>{m.recall}</td>
                      <td style={{color:'#b96dff'}}>{m.f1}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {tab===3&&(
        <div className="grid-2">
          <div className="card">
            <div className="card-title">PACKET PARAMETERS</div>
            {[['src_bytes',0,100000,'Src Bytes'],['dst_bytes',0,50000,'Dst Bytes'],['port',1,65535,'Port'],['duration',0,300,'Duration (s)'],['count',1,512,'Connection Count'],['risk_score',0,100,'Risk Score']].map(([k,mn,mx,lbl])=>(
              <div key={k} style={{marginBottom:10}}>
                <div style={{display:'flex',justifyContent:'space-between',fontSize:10,color:'#4a6080',marginBottom:3}}>
                  <span>{lbl}</span><span style={{color:'var(--cyan)'}}>{pktInputs[k]}</span>
                </div>
                <input type="range" min={mn} max={mx} value={pktInputs[k]} style={{width:'100%'}}
                  onChange={e=>setPktInputs(p=>({...p,[k]:Number(e.target.value)}))}/>
              </div>
            ))}
            <button onClick={classifyPacket} style={{width:'100%',marginTop:8}}>CLASSIFY PACKET</button>
          </div>
          <div className="card">
            <div className="card-title">PREDICTION RESULT</div>
            {prediction?(
              <>
                <div style={{textAlign:'center',padding:'20px 0',borderBottom:'1px solid var(--border)',marginBottom:14}}>
                  <div style={{fontSize:32,marginBottom:8}}>{prediction.is_attack?'⛔':'✅'}</div>
                  <div style={{fontFamily:'Orbitron,monospace',fontSize:18,color:prediction.is_attack?'var(--red)':'var(--green)'}}>{prediction.label}</div>
                  <div style={{fontSize:12,color:'#4a6080',marginTop:4}}>Confidence: <span style={{color:prediction.is_attack?'var(--red)':'var(--green)'}}>{prediction.conf}%</span></div>
                </div>
                <div className="card-title">PROBABILITY DISTRIBUTION</div>
                {prediction.probs.slice(0,6).map((p,i)=>(
                  <div key={i} className="mini-bar-wrap">
                    <div style={{display:'flex',justifyContent:'space-between',fontSize:10,marginBottom:2}}>
                      <span style={{color:COLOR_MAP[p.t]||'#4a6080'}}>{p.t}</span>
                      <span style={{color:'#4a6080'}}>{(p.p*100).toFixed(1)}%</span>
                    </div>
                    <div className="mini-bar-track">
                      <div className="mini-bar-fill" style={{width:`${p.p*100}%`,background:COLOR_MAP[p.t]||'#00d4ff'}}/>
                    </div>
                  </div>
                ))}
              </>
            ):(
              <div style={{color:'#2a4a6a',fontSize:11,textAlign:'center',marginTop:40}}>
                Adjust parameters and click<br/>CLASSIFY PACKET to run inference
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function LiveSimPage(){
  const [running,setRunning]=useState(false);
  const [stats,setStats]=useState({total:0,attacks:0,blocked:0,normal:0});
  const [log,setLog]=useState([]);
  const [history,setHistory]=useState([]);
  const [pktRate,setPktRate]=useState(8);
  const [attackProb,setAttackProb]=useState(0.3);
  const [autoBlock,setAutoBlock]=useState(true);
  const intervalRef=useRef(null);
  const r=useRef(rng(Date.now()));

  const stop=useCallback(()=>{
    if(intervalRef.current)clearInterval(intervalRef.current);
    setRunning(false);
  },[]);

  const start=useCallback(()=>{
    setRunning(true);
    intervalRef.current=setInterval(()=>{
      const n=Math.floor(pktRate*(0.7+r.current()*0.6));
      let atks=0,nrm=0,blk=0;
      const newLogs=[];
      for(let i=0;i<n;i++){
        const isAtk=r.current()<attackProb;
        if(isAtk){
          atks++;
          const t=ATTACK_TYPES[1+Math.floor(r.current()*(ATTACK_TYPES.length-1))];
          const s=SEV_MAP[t]||'low';
          const blocked=autoBlock&&r.current()<0.72;
          if(blocked)blk++;
          const src=`${Math.floor(r.current()*223)+1}.${Math.floor(r.current()*255)}.${Math.floor(r.current()*255)}.${Math.floor(r.current()*254)+1}`;
          if(r.current()<0.35){
            newLogs.push({type:s==='critical'||s==='high'?'ALERT':'BLOCK',msg:`${t} from ${src} [${s.toUpperCase()}]${blocked?' → BLOCKED':''}`,ts:new Date().toTimeString().substring(0,8)});
          }
        }else{
          nrm++;
          if(r.current()<0.04){
            const src=`${Math.floor(r.current()*192)+1}.168.${Math.floor(r.current()*255)}.${Math.floor(r.current()*254)+1}`;
            newLogs.push({type:'OK',msg:`Clean traffic from ${src}`,ts:new Date().toTimeString().substring(0,8)});
          }
        }
      }
      setStats(s=>({total:s.total+n,attacks:s.attacks+atks,blocked:s.blocked+blk,normal:s.normal+nrm}));
      setHistory(h=>[...h.slice(-39),{normal:nrm,attack:atks,t:h.length}]);
      if(newLogs.length)setLog(l=>[...l.slice(-60),...newLogs]);
    },300);
  },[pktRate,attackProb,autoBlock]);

  useEffect(()=>()=>stop(),[stop]);

  const reset=()=>{stop();setStats({total:0,attacks:0,blocked:0,normal:0});setLog([]);setHistory([]);};

  return(
    <>
      <div className="card" style={{marginBottom:14}}>
        <div className="card-title">SIMULATION CONTROLS</div>
        <div style={{display:'flex',gap:20,flexWrap:'wrap',alignItems:'center'}}>
          <div style={{flex:1,minWidth:160}}>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:10,color:'#4a6080',marginBottom:3}}>
              <span>Packets/sec</span><span style={{color:'var(--cyan)'}}>{pktRate}</span>
            </div>
            <input type="range" min="1" max="40" value={pktRate} style={{width:'100%'}} onChange={e=>setPktRate(Number(e.target.value))} disabled={running}/>
          </div>
          <div style={{flex:1,minWidth:160}}>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:10,color:'#4a6080',marginBottom:3}}>
              <span>Attack Probability</span><span style={{color:'var(--orange)'}}>{(attackProb*100).toFixed(0)}%</span>
            </div>
            <input type="range" min="0" max="1" step="0.05" value={attackProb} style={{width:'100%'}} onChange={e=>setAttackProb(Number(e.target.value))} disabled={running}/>
          </div>
          <label style={{display:'flex',alignItems:'center',gap:6,fontSize:11,color:'#4a6080',cursor:'pointer'}}>
            <input type="checkbox" checked={autoBlock} onChange={e=>setAutoBlock(e.target.checked)}/> Auto-Block
          </label>
          <div style={{display:'flex',gap:8}}>
            {!running?<button className="success" onClick={start}>▶ START</button>:<button className="danger" onClick={stop}>⏹ STOP</button>}
            <button onClick={reset}>↺ RESET</button>
          </div>
        </div>
      </div>

      <div className="grid-4" style={{marginBottom:14}}>
        {[
          {v:stats.total,l:'PACKETS',c:'var(--cyan)'},
          {v:stats.attacks,l:'THREATS',c:'var(--red)'},
          {v:stats.blocked,l:'BLOCKED',c:'var(--orange)'},
          {v:stats.total>0?`${(stats.attacks/stats.total*100).toFixed(1)}%`:'0%',l:'ATTACK RATE',c:'var(--purple)'},
        ].map((m,i)=>(
          <div key={i} className="card">
            <div className="metric-val" style={{color:m.c}}>{m.v}</div>
            <div className="metric-lbl">{m.l}</div>
            {running&&<div style={{display:'flex',alignItems:'center',gap:4,marginTop:4}}><div className="live-dot"/><span style={{fontSize:9,color:'var(--red)'}}>LIVE</span></div>}
          </div>
        ))}
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">LIVE TRAFFIC ({running&&<span style={{color:'var(--red)'}}>● RECORDING</span>})</div>
          <LineChart series={[
            {data:history.map(h=>h.normal),color:'#00ff88'},
            {data:history.map(h=>h.attack),color:'#ff2d55'},
          ]} height={120}/>
          <div style={{display:'flex',gap:12,marginTop:4,fontSize:10,color:'#4a6080'}}>
            <span><span style={{color:'#00ff88'}}>■</span> Normal</span>
            <span><span style={{color:'#ff2d55'}}>■</span> Attack</span>
          </div>
        </div>
        <div className="card">
          <div className="card-title">EVENT LOG</div>
          <div className="terminal">
            {[...log].reverse().slice(0,20).map((e,i)=>{
              const c={ALERT:'#ff2d55',BLOCK:'#ff8c00',OK:'#00ff88',INFO:'#00d4ff'}[e.type]||'#4a6080';
              return<div key={i}><span style={{color:'#2a4a6a'}}>{e.ts} </span><span style={{color:c}}>[{e.type}]</span><span style={{color:'#dde6f0'}}> {e.msg}</span></div>;
            })}
            {log.length===0&&<span style={{color:'#2a4a6a'}}>Waiting for packets...</span>}
          </div>
        </div>
      </div>
    </>
  );
}

function AnomalyPage({data}){
  const r2=rng(7);
  const withScores=data.map(d=>({...d,anomaly:d.is_attack?-0.3-r2()*0.5:0.1+r2()*0.4}));
  const threshold=-0.2;
  const anomalies=withScores.filter(d=>d.anomaly<threshold);
  const overlap=anomalies.filter(d=>d.is_attack).length;

  const buckets=Array.from({length:40},(_,i)=>({
    score:-1+i*(1.5/40),
    normal:withScores.filter(d=>!d.is_attack&&d.anomaly>=-1+i*(1.5/40)&&d.anomaly<-1+(i+1)*(1.5/40)).length,
    attack:withScores.filter(d=>d.is_attack&&d.anomaly>=-1+i*(1.5/40)&&d.anomaly<-1+(i+1)*(1.5/40)).length,
  }));

  return(
    <>
      <div className="grid-4" style={{marginBottom:14}}>
        {[
          {v:anomalies.length,l:'ANOMALIES',c:'var(--red)'},
          {v:`${(withScores.reduce((s,d)=>s+d.anomaly,0)/withScores.length).toFixed(3)}`,l:'AVG SCORE',c:'var(--cyan)'},
          {v:`${(overlap/Math.max(anomalies.length,1)*100).toFixed(0)}%`,l:'OVERLAP W/ ATTACKS',c:'var(--green)'},
          {v:threshold,l:'THRESHOLD',c:'var(--yellow)'},
        ].map((m,i)=>(
          <div key={i} className="card">
            <div className="metric-val" style={{color:m.c,fontSize:18}}>{m.v}</div>
            <div className="metric-lbl">{m.l}</div>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">ANOMALY SCORE DISTRIBUTION</div>
          <div style={{display:'flex',alignItems:'flex-end',gap:1,height:120,padding:'0 4px'}}>
            {buckets.map((b,i)=>{
              const max=Math.max(...buckets.map(x=>x.normal+x.attack),1);
              const atk=b.attack/(max)*100;
              const nrm=b.normal/(max)*100;
              const isBelow=b.score<threshold;
              return(
                <div key={i} style={{flex:1,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'flex-end',height:'100%',borderLeft:b.score<threshold+0.04&&b.score>threshold-0.04?'1px solid #ffd60a':'none'}}>
                  {b.attack>0&&<div style={{width:'100%',background:'#ff2d55',opacity:0.8,height:`${atk}%`,minHeight:b.attack>0?1:0}}/>}
                  {b.normal>0&&<div style={{width:'100%',background:'#00ff88',opacity:0.6,height:`${nrm}%`,minHeight:b.normal>0?1:0}}/>}
                </div>
              );
            })}
          </div>
          <div style={{display:'flex',gap:12,marginTop:8,fontSize:10,color:'#4a6080'}}>
            <span><span style={{color:'#00ff88'}}>■</span> Normal</span>
            <span><span style={{color:'#ff2d55'}}>■</span> Attack</span>
            <span><span style={{color:'#ffd60a'}}>|</span> Threshold ({threshold})</span>
          </div>
        </div>

        <div className="card">
          <div className="card-title">ANOMALY RATE BY ATTACK TYPE</div>
          <BarChart
            data={ATTACK_TYPES.map(t=>{
              const typeData=withScores.filter(d=>d.label===t);
              const rate=typeData.filter(d=>d.anomaly<threshold).length/Math.max(typeData.length,1)*100;
              return{label:t,value:Math.round(rate)};
            }).sort((a,b)=>b.value-a.value).slice(0,8)}
            horizontal={true} height={200}
            colorFn={(d)=>d.value>60?'#ff2d55':d.value>30?'#ff8c00':'#00d4ff'}
          />
        </div>
      </div>

      <div className="card">
        <div className="card-title">TOP ANOMALIES</div>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Time</th><th>Src IP</th><th>Type</th><th>Severity</th><th>Anomaly Score</th><th>Risk</th><th>Protocol</th></tr></thead>
            <tbody>
              {anomalies.sort((a,b)=>a.anomaly-b.anomaly).slice(0,20).map((d,i)=>(
                <tr key={i}>
                  <td style={{color:'#4a6080'}}>{d.timestamp.toTimeString().substring(0,8)}</td>
                  <td style={{color:'#ff2d55'}}>{d.src_ip}</td>
                  <td style={{color:COLOR_MAP[d.label]||'#00d4ff'}}>{d.label}</td>
                  <td><span className={`badge badge-${d.sev}`}>{d.sev}</span></td>
                  <td style={{color:'#ffd60a'}}>{d.anomaly.toFixed(4)}</td>
                  <td style={{color:SEV_COLOR[d.sev]}}>{d.risk}</td>
                  <td style={{color:'#4a6080'}}>{d.protocol.toUpperCase()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

function GeoPage({data}){
  const countryAttacks=COUNTRIES.map(c=>{
    const attacks=data.filter(d=>d.country===c&&d.is_attack);
    const crits=attacks.filter(d=>d.sev==='critical').length;
    return{country:c,count:attacks.length,crits,color:crits>10?'#ff2d55':crits>5?'#ff8c00':'#ffd60a'};
  }).sort((a,b)=>b.count-a.count);

  return(
    <>
      <div className="card" style={{marginBottom:14}}>
        <div className="card-title">GLOBAL THREAT MAP</div>
        <WorldMap countryData={countryAttacks}/>
        <div style={{display:'flex',gap:12,marginTop:8,fontSize:10,color:'#4a6080'}}>
          <span><span style={{color:'#ff2d55'}}>●</span> High Critical</span>
          <span><span style={{color:'#ff8c00'}}>●</span> Medium</span>
          <span><span style={{color:'#ffd60a'}}>●</span> Low</span>
          <span style={{marginLeft:'auto'}}>Bubble size = attack count</span>
        </div>
      </div>
      <div className="grid-2">
        <div className="card">
          <div className="card-title">TOP ATTACKING COUNTRIES</div>
          <BarChart data={countryAttacks.slice(0,10).map(d=>({label:d.country,value:d.count}))} horizontal={true} height={200} colorFn={(d,i)=>i===0?'#ff2d55':i<3?'#ff8c00':'#00d4ff'}/>
        </div>
        <div className="card">
          <div className="card-title">COUNTRY DETAILS</div>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Country</th><th>Attacks</th><th>Critical</th><th>Rate</th></tr></thead>
              <tbody>
                {countryAttacks.map((c,i)=>(
                  <tr key={i}>
                    <td style={{color:'#4a6080'}}>{c.country}</td>
                    <td style={{color:c.color}}>{c.count}</td>
                    <td style={{color:'#ff2d55'}}>{c.crits}</td>
                    <td>
                      <div className="mini-bar-track" style={{width:60}}>
                        <div className="mini-bar-fill" style={{width:`${c.count/Math.max(countryAttacks[0].count,1)*100}%`,background:c.color}}/>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}

function ThreatIntelPage({data}){
  const threats=[
    {name:'DoS / DDoS',sev:'critical',icon:'💥',mitre:'T1498',cve:'CVE-2023-1234',desc:'Floods target with requests to exhaust resources.'},
    {name:'SQL Injection',sev:'high',icon:'💉',mitre:'T1190',cve:'CVE-2023-5678',desc:'Malicious SQL injected to manipulate database.'},
    {name:'Port Scan',sev:'medium',icon:'🔭',mitre:'T1046',cve:'N/A',desc:'Systematic enumeration of open ports.'},
    {name:'R2L Attack',sev:'high',icon:'🚪',mitre:'T1078',cve:'CVE-2022-9012',desc:'Unauthorized remote-to-local access.'},
    {name:'U2R Exploit',sev:'critical',icon:'👑',mitre:'T1068',cve:'CVE-2023-4567',desc:'Privilege escalation to root/admin.'},
    {name:'Ransomware',sev:'critical',icon:'🔒',mitre:'T1486',cve:'CVE-2023-2345',desc:'Encrypts victim data and demands ransom.'},
    {name:'MITM',sev:'high',icon:'👁️',mitre:'T1557',cve:'CVE-2023-7890',desc:'Intercepts traffic between two parties.'},
    {name:'Brute Force',sev:'high',icon:'🔨',mitre:'T1110',cve:'N/A',desc:'Systematic credential guessing attack.'},
    {name:'Zero-Day',sev:'critical',icon:'☢️',mitre:'T1203',cve:'CVE-2024-????',desc:'Exploit targeting unknown vulnerabilities.'},
  ];

  const topSrcs=Object.entries(data.filter(d=>d.is_attack).reduce((acc,d)=>{acc[d.src_ip]=(acc[d.src_ip]||0)+1;return acc;},{})).sort((a,b)=>b[1]-a[1]).slice(0,8).map(([ip,c])=>({label:ip,value:c}));

  const timelineData=Array.from({length:24},(_,h)=>{
    const hour=h;
    return{h,count:data.filter(d=>d.is_attack&&d.timestamp.getHours()===hour).length};
  });

  return(
    <>
      <div className="grid-2" style={{marginBottom:14}}>
        <div className="card">
          <div className="card-title">TOP ATTACKING IPs</div>
          <BarChart data={topSrcs} horizontal={true} height={180} colorFn={(_,i)=>i===0?'#ff2d55':i<3?'#ff8c00':'#00d4ff'}/>
        </div>
        <div className="card">
          <div className="card-title">ATTACK TIMELINE (BY HOUR)</div>
          <LineChart series={[{data:timelineData.map(d=>d.count),color:'#ff2d55'}]} height={160}/>
          <div style={{display:'flex',justifyContent:'space-between',fontSize:9,color:'#2a4a6a',marginTop:4}}>
            <span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>23:00</span>
          </div>
        </div>
      </div>

      <div className="card" style={{marginBottom:14}}>
        <div className="card-title">THREAT ENCYCLOPEDIA</div>
        <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:10}}>
          {threats.map((t,i)=>{
            const c=SEV_COLOR[t.sev]||'#00d4ff';
            return(
              <div key={i} style={{background:'var(--bg3)',border:`1px solid ${c}22`,borderLeft:`3px solid ${c}`,borderRadius:8,padding:12}}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
                  <span style={{color:c,fontSize:12}}>{t.name}</span>
                  <span className={`badge badge-${t.sev}`}>{t.sev}</span>
                </div>
                <div style={{fontSize:10,color:'#4a6080',marginBottom:6}}>{t.desc}</div>
                <div style={{fontSize:9,color:'#2a4a6a'}}>
                  MITRE: <span style={{color:c}}>{t.mitre}</span> · CVE: {t.cve}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

function SettingsPage(){
  const [saved,setSaved]=useState(false);
  const [algo,setAlgo]=useState('Random Forest');
  const [thresh,setThresh]=useState(0.75);
  const [modules,setModules]=useState({dpi:true,sig:true,behavior:true,ml:true,geo:false,auto:false,rate:true,ssl:false});

  const rules=[
    {id:'FW-001',name:'Allow SSH Internal',src:'192.168.0.0/16',dest:'*',port:'22',proto:'TCP',action:'ALLOW'},
    {id:'FW-002',name:'Allow HTTPS Out',src:'0.0.0.0/0',dest:'*',port:'443',proto:'TCP',action:'ALLOW'},
    {id:'FW-003',name:'Block Telnet',src:'0.0.0.0/0',dest:'*',port:'23',proto:'TCP',action:'DROP'},
    {id:'FW-004',name:'Block MySQL External',src:'0.0.0.0/0',dest:'10.0.0.50',port:'3306',proto:'TCP',action:'DROP'},
    {id:'FW-005',name:'Allow DNS',src:'0.0.0.0/0',dest:'8.8.8.8',port:'53',proto:'UDP',action:'ALLOW'},
    {id:'FW-006',name:'Block ICMP Flood',src:'0.0.0.0/0',dest:'*',port:'*',proto:'ICMP',action:'RATE-LIMIT'},
  ];

  return(
    <>
      <div className="tab-row">
        <div style={{fontSize:11,color:'var(--cyan)',padding:'4px 8px',fontFamily:'Orbitron,monospace'}}>ENGINE CONFIG</div>
      </div>
      <div className="grid-3">
        <div className="card">
          <div className="card-title">DETECTION ENGINE</div>
          <div style={{marginBottom:10}}>
            <div style={{fontSize:10,color:'#4a6080',marginBottom:4}}>Primary Algorithm</div>
            <select value={algo} onChange={e=>setAlgo(e.target.value)} style={{width:'100%'}}>
              {['Random Forest','Gradient Boosting','Neural Network','Ensemble'].map(a=><option key={a}>{a}</option>)}
            </select>
          </div>
          <div style={{marginBottom:12}}>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:10,color:'#4a6080',marginBottom:3}}>
              <span>Alert Threshold</span><span style={{color:'var(--cyan)'}}>{thresh}</span>
            </div>
            <input type="range" min="0" max="1" step="0.01" value={thresh} style={{width:'100%'}} onChange={e=>setThresh(Number(e.target.value))}/>
          </div>
          <div className="card-title">DETECTION MODULES</div>
          {[['dpi','Deep Packet Inspection'],['sig','Signature Detection'],['behavior','Behavioral Analysis'],['ml','ML Anomaly Detection'],['geo','GeoIP Blocking'],['auto','Auto-Block Attackers'],['rate','Rate Limiting'],['ssl','SSL Inspection']].map(([k,lbl])=>(
            <label key={k} style={{display:'flex',alignItems:'center',gap:8,fontSize:11,color:modules[k]?'var(--cyan)':'#4a6080',marginBottom:6,cursor:'pointer'}}>
              <input type="checkbox" checked={modules[k]} onChange={e=>setModules(m=>({...m,[k]:e.target.checked}))}/>
              {lbl}
            </label>
          ))}
        </div>

        <div className="card">
          <div className="card-title">FIREWALL RULES</div>
          <div className="table-wrap">
            <table>
              <thead><tr><th>ID</th><th>Name</th><th>Port</th><th>Proto</th><th>Action</th></tr></thead>
              <tbody>
                {rules.map((r,i)=>(
                  <tr key={i}>
                    <td style={{color:'#4a6080'}}>{r.id}</td>
                    <td style={{fontSize:10}}>{r.name}</td>
                    <td style={{color:'#4a6080'}}>{r.port}</td>
                    <td style={{color:'#00d4ff'}}>{r.proto}</td>
                    <td><span className={`badge ${r.action==='ALLOW'?'badge-clean':r.action==='DROP'?'badge-critical':'badge-medium'}`}>{r.action}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="card-title">SYSTEM INFO</div>
          {[
            ['IDS Version','NeuralGuard v3.0.0'],['Engine','Python + Scikit-learn'],['Dataset','KDD Cup 99+'],
            ['Models','RF + GBM + MLP + IsoForest'],['Features','18 engineered'],['Best Model','Random Forest'],
            ['Accuracy','94.2%'],['F1 Score','93.9%'],['Attack Classes','12'],['License','Enterprise'],
          ].map(([k,v])=>(
            <div key={k} style={{display:'flex',justifyContent:'space-between',padding:'5px 0',borderBottom:'1px solid rgba(0,212,255,0.06)',fontSize:11}}>
              <span style={{color:'#4a6080'}}>{k}</span><span style={{color:'var(--cyan)'}}>{v}</span>
            </div>
          ))}
          <div style={{marginTop:12}}>
            <div className="card-title">RESOURCE USAGE</div>
            {[['CPU',42,'#00ff88'],['Memory',58,'#00d4ff'],['Disk',31,'#ffd60a'],['Network',76,'#ff8c00'],['ML Load',23,'#b96dff']].map(([lbl,v,c])=>(
              <div key={lbl} style={{marginBottom:8}}>
                <div style={{display:'flex',justifyContent:'space-between',fontSize:10,marginBottom:2}}>
                  <span style={{color:'#4a6080'}}>{lbl}</span><span style={{color:c}}>{v}%</span>
                </div>
                <div className="mini-bar-track"><div className="mini-bar-fill" style={{width:`${v}%`,background:c}}/></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{display:'flex',gap:8,marginTop:8}}>
        <button className="success" onClick={()=>{setSaved(true);setTimeout(()=>setSaved(false),2500);}}>
          {saved?'✓ Saved!':'💾 Save Config'}
        </button>
        <button>🔄 Restart Engine</button>
        <button>📤 Export Report</button>
        <button className="danger">🗑️ Clear Logs</button>
      </div>
    </>
  );
}

function NetworkPage({data}){
  const [sevFilter,setSevFilter]=useState(['critical','high']);
  const attacks=data.filter(d=>d.is_attack&&sevFilter.includes(d.sev));
  const nodes=[];const edges=[];
  const seen=new Set();
  attacks.slice(0,40).forEach(d=>{
    if(!seen.has(d.src_ip)){seen.add(d.src_ip);nodes.push({id:d.src_ip,type:'src',sev:d.sev});}
    if(!seen.has(d.dst_ip)){seen.add(d.dst_ip);nodes.push({id:d.dst_ip,type:'dst',sev:d.sev});}
    edges.push({s:d.src_ip,t:d.dst_ip,sev:d.sev,label:d.label});
  });

  return(
    <>
      <div className="filter-row">
        {['critical','high','medium','low'].map(s=>(
          <label key={s} style={{display:'flex',alignItems:'center',gap:5,fontSize:11,cursor:'pointer',color:sevFilter.includes(s)?SEV_COLOR[s]:'#4a6080'}}>
            <input type="checkbox" checked={sevFilter.includes(s)} onChange={e=>{setSevFilter(f=>e.target.checked?[...f,s]:f.filter(x=>x!==s));}}/>
            {s.toUpperCase()}
          </label>
        ))}
      </div>
      <div className="grid-2">
        <div className="card">
          <div className="card-title">ATTACK NETWORK TOPOLOGY ({nodes.length} nodes, {edges.length} edges)</div>
          <NetworkGraph data={attacks} size={360}/>
          <div style={{display:'flex',gap:12,marginTop:8,fontSize:10,color:'#4a6080'}}>
            <span><span style={{color:'#ff2d55'}}>●</span> Attacker (src)</span>
            <span><span style={{color:'#00d4ff'}}>●</span> Victim (dst)</span>
          </div>
        </div>
        <div className="card">
          <div className="card-title">TOP NODES BY DEGREE</div>
          {nodes.slice(0,12).map((n,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,padding:'5px 0',borderBottom:'1px solid rgba(0,212,255,0.06)',fontSize:11}}>
              <div style={{width:18,height:18,borderRadius:'50%',background:n.type==='src'?'#ff2d55':'#00d4ff',display:'flex',alignItems:'center',justifyContent:'center',fontSize:8,color:'#010912',fontWeight:700}}>{i+1}</div>
              <span style={{flex:1,color:'#4a6080'}}>{n.id}</span>
              <span className={`badge badge-${n.sev}`}>{n.type==='src'?'ATTACKER':'VICTIM'}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

const PAGES=[
  {id:'dashboard',label:'Dashboard',icon:'📡'},
  {id:'live',label:'Live Simulation',icon:'🔴'},
  {id:'traffic',label:'Traffic Analysis',icon:'🔍'},
  {id:'ml',label:'ML Engine',icon:'🤖'},
  {id:'network',label:'Network Graph',icon:'🌐'},
  {id:'geo',label:'GeoIP Threat Map',icon:'🗺️'},
  {id:'threat',label:'Threat Intel',icon:'⚠️'},
  {id:'anomaly',label:'Anomaly Detection',icon:'🔮'},
  {id:'settings',label:'Settings & Rules',icon:'⚙️'},
];

export default function App(){
  const [page,setPage]=useState('dashboard');
  const [time,setTime]=useState(new Date());
  useEffect(()=>{const t=setInterval(()=>setTime(new Date()),1000);return()=>clearInterval(t);},[]);

  const attacks=DATA.filter(d=>d.is_attack);
  const crits=attacks.filter(d=>d.sev==='critical');
  const threatLevel=crits.length/DATA.length>0.05?'CRITICAL':crits.length/DATA.length>0.03?'HIGH':'MEDIUM';
  const tc={CRITICAL:'#ff2d55',HIGH:'#ff8c00',MEDIUM:'#ffd60a'}[threatLevel];

  const currentPage=PAGES.find(p=>p.id===page);

  return(
    <>
      <style>{css}</style>
      <div className="app">
        <div className="sidebar">
          <div className="logo">🛡️ NEURALGUARD</div>
          <div className="logo-sub">v3.0 · ENTERPRISE IDS</div>
          {PAGES.map(p=>(
            <div key={p.id} className={`nav-item${page===p.id?' active':''}`} onClick={()=>setPage(p.id)}>
              <span style={{fontSize:13}}>{p.icon}</span>
              <span>{p.label}</span>
            </div>
          ))}
          <div className="sidebar-footer">
            <div style={{fontSize:9,color:'#1e3a5f',letterSpacing:2,marginBottom:8}}>THREAT LEVEL</div>
            <div style={{fontFamily:'Orbitron,monospace',fontSize:16,color:tc,textAlign:'center',marginBottom:6}}>{threatLevel}</div>
            <div className="mini-bar-track">
              <div className="mini-bar-fill" style={{width:`${crits.length/DATA.length*2000}%`,maxWidth:'100%',background:tc}}/>
            </div>
            <div style={{marginTop:12,fontSize:9,color:'#1e3a5f',letterSpacing:1}}>SYSTEM STATUS</div>
            {[['IDS Engine','ACTIVE','#00ff88'],['ML Models','LOADED','#00ff88'],['Network Tap','LIVE','#00d4ff']].map(([l,v,c])=>(
              <div key={l} style={{display:'flex',justifyContent:'space-between',fontSize:10,padding:'3px 0'}}>
                <span style={{color:'#2a4a6a'}}>{l}</span>
                <span style={{color:c}}><span className="status-dot" style={{background:c}}/>{v}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="main">
          <div className="topbar">
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <span className="topbar-title">NEURALGUARD IDS</span>
              <span style={{fontSize:9,color:'#2a4a6a',letterSpacing:1}}>·</span>
              <span style={{fontSize:11,color:'#4a6080'}}>{currentPage?.label?.toUpperCase()}</span>
            </div>
            <div className="topbar-right">
              <span><span className="status-dot"/>LIVE</span>
              <span style={{color:'#4a6080'}}>{DATA.length} packets · {attacks.length} threats</span>
              <span style={{fontFamily:'Orbitron,monospace',color:'var(--cyan)',fontSize:13}}>{time.toTimeString().substring(0,8)}</span>
            </div>
          </div>

          <div className="content">
            <div className="page-title">{currentPage?.icon} {currentPage?.label}</div>
            {page==='dashboard'&&<DashboardPage data={DATA}/>}
            {page==='live'&&<LiveSimPage/>}
            {page==='traffic'&&<TrafficPage data={DATA}/>}
            {page==='ml'&&<MLPage data={DATA}/>}
            {page==='network'&&<NetworkPage data={DATA}/>}
            {page==='geo'&&<GeoPage data={DATA}/>}
            {page==='threat'&&<ThreatIntelPage data={DATA}/>}
            {page==='anomaly'&&<AnomalyPage data={DATA}/>}
            {page==='settings'&&<SettingsPage/>}
          </div>

          <div style={{padding:'10px 20px',borderTop:'1px solid var(--border)',fontSize:9,color:'#1e3a5f',display:'flex',justifyContent:'space-between'}}>
            <span>NeuralGuard IDS v3.0.0 · RF + GBM + MLP + IsoForest · KDD Cup 99+ Extended</span>
            <span>ENTERPRISE EDITION</span>
          </div>
        </div>
      </div>
    </>
  );
}
