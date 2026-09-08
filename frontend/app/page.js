'use client';
import { useEffect, useMemo, useState } from 'react';
import './style.css';

const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
const WS=process.env.NEXT_PUBLIC_WS_URL||API.replace(/^http/,'ws')+'/ws/events';
const initial={round:0,status:'IDLE',red_score:0,blue_score:0,vcore:'OFFLINE',red:'READY',blue:'READY',memory:[]};
const redMods=[['LLM','STRATEGY'],['RAG','KNOWLEDGE'],['MCP','TOOLS'],['MEMORY','CONTEXT']];
const blueMods=[['POLICY','ENGINE'],['JUDGE','EVALUATOR'],['TELEMETRY','ANALYSIS'],['TOOLS','DEFENSE']];

export default function Home(){
 const [state,setState]=useState(initial),[events,setEvents]=useState([]),[connected,setConnected]=useState(false),[busy,setBusy]=useState(false);
 const ingest=p=>{if(!p)return;if(p.data)setState(p.data);setEvents(v=>[...v,p].slice(-40));};
 useEffect(()=>{fetch(`${API}/api/state`).then(r=>r.ok?r.json():Promise.reject()).then(setState).catch(()=>{});let s;try{s=new WebSocket(WS);s.onopen=()=>setConnected(true);s.onclose=()=>setConnected(false);s.onerror=()=>setConnected(false);s.onmessage=e=>{try{ingest(JSON.parse(e.data))}catch{}}}catch{}return()=>s?.close()},[]);
 const start=async()=>{setBusy(true);try{const r=await fetch(`${API}/api/battle/start`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({rounds:1})});const d=await r.json();setState(d.state||d)}finally{setBusy(false)}};
 const reset=async()=>{setBusy(true);try{const r=await fetch(`${API}/api/battle/reset`,{method:'POST'});setState(await r.json());setEvents([])}finally{setBusy(false)}};
 const logs=useMemo(()=>events.slice(-5).reverse().map((e,i)=>({id:i,type:(e.type||'EVENT').replaceAll('_',' ').toUpperCase(),text:e.message||(e.data?.status?`Battle ${e.data.status} · Round ${e.data.round??0}`:'V-Core state updated')})),[events]);
 return <main className="shell">
  <div className="energy redEnergy"/><div className="energy blueEnergy"/><div className="circuitField"/>
  <header className="topbar"><div className="brand"><b>V-AGENTWAR</b><span>RED <i>VS</i> BLUE</span></div><nav><span className="active">DASHBOARD</span><span>BATTLES</span><span>AGENTS</span><span>KNOWLEDGE</span></nav><div className="topStatus"><span className={connected?'dot online':'dot'}/>{connected?'SYSTEM ONLINE':'BACKEND OFFLINE'}<small>POWERED BY V-CORE</small></div></header>
  <section className="warStage">
   <aside className="moduleRail leftRail">{redMods.map(([a,b])=><div className="module redModule" key={a}><span className="moduleIcon">◇</span><div><b>{a}</b><small>{b}</small></div><i>●</i></div>)}</aside>
   <article className="agentCard redCard"><span className="eyebrow">OFFENSIVE INTELLIGENCE</span><h2>RED AGENT</h2><strong>{state.red||'READY'}</strong><p>ADAPTIVE ADVERSARY</p><div className="strategy"><small>LIVE STRATEGY</small><b>{state.status==='IDLE'?'Awaiting battle authorization':'Controlled attack simulation active'}</b></div><div className="meter"><i style={{width:`${Math.min(100,state.red_score||0)}%`}}/></div><div className="stats"><span><b>{state.red_score||0}</b> SCORE</span><span><b>{state.round||0}</b> ROUNDS</span></div></article>
   <div className="coreWrap"><div className="orbit orbitOne"/><div className="orbit orbitTwo"/><div className="chip"><div className="chipGrid"/><span>V</span><small>CORE</small></div><h1>V-CORE</h1><p>DUAL INTELLIGENCE ENGINE</p><b className="coreState">{state.vcore||'OFFLINE'}</b><div className="coreMeta"><span>PLAN</span><span>OBSERVE</span><span>ADAPT</span><span>MEMORY</span></div></div>
   <article className="agentCard blueCard"><span className="eyebrow">DEFENSIVE INTELLIGENCE</span><h2>BLUE AGENT</h2><strong>{state.blue||'READY'}</strong><p>ADAPTIVE DEFENDER</p><div className="strategy"><small>LIVE STRATEGY</small><b>{state.status==='IDLE'?'Monitoring cyber range':'Telemetry analysis and response active'}</b></div><div className="meter"><i style={{width:`${Math.min(100,state.blue_score||0)}%`}}/></div><div className="stats"><span><b>{state.blue_score||0}</b> SCORE</span><span><b>{state.memory?.length||0}</b> MEMORY</span></div></article>
   <aside className="moduleRail rightRail">{blueMods.map(([a,b])=><div className="module blueModule" key={a}><span className="moduleIcon">◇</span><div><b>{a}</b><small>{b}</small></div><i>●</i></div>)}</aside>
  </section>
  <section className="scorebar"><div className="teamScore redScore"><b>{state.red_score||0}</b><span>RED SCORE</span></div><div className="battleControl"><span className="round">ROUND {String(state.round||0).padStart(2,'0')}</span><small>{state.status||'IDLE'}</small><div><button disabled={busy} onClick={start}>{busy?'PROCESSING':'START BATTLE'}</button><button className="ghost" disabled={busy} onClick={reset}>RESET</button></div></div><div className="teamScore blueScore"><b>{state.blue_score||0}</b><span>BLUE SCORE</span></div></section>
  <section className="bottomGrid"><div className="glassPanel eventPanel"><div className="panelTitle"><h3>LIVE BATTLE LOG</h3><span>{connected?'STREAMING':'WAITING'}</span></div>{logs.length?logs.map(x=><p key={x.id}><b>{x.type}</b><span>{x.text}</span></p>):<div className="empty">No battle events yet. Start an isolated controlled round.</div>}</div><div className="glassPanel statusPanel"><div className="panelTitle"><h3>V-CORE STATUS</h3><span>SAFE MODE</span></div><dl><div><dt>Engine</dt><dd>{state.vcore||'OFFLINE'}</dd></div><div><dt>Battle</dt><dd>{state.status||'IDLE'}</dd></div><div><dt>Memory</dt><dd>{state.memory?.length||0} rounds</dd></div><div><dt>Link</dt><dd>{connected?'WebSocket':'REST fallback'}</dd></div></dl></div></section>
  <footer>V-AGENTWAR // RED VS BLUE <span>AI AGENTS · ADAPT · DEFEND · EVOLVE</span></footer>
 </main>
}