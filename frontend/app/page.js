'use client';
import { useEffect, useMemo, useState } from 'react';
import './style.css';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS = process.env.NEXT_PUBLIC_WS_URL || API.replace(/^http/, 'ws') + '/ws/events';
const initial = {round:0,status:'IDLE',red_score:0,blue_score:0,vcore:'OFFLINE',red:'READY',blue:'READY',memory:[]};

export default function Home() {
  const [state,setState] = useState(initial);
  const [events,setEvents] = useState([]);
  const [connected,setConnected] = useState(false);
  const [busy,setBusy] = useState(false);

  const ingest = (payload) => {
    if (!payload) return;
    if (payload.data) setState(payload.data);
    setEvents(prev => [...prev, payload].slice(-40));
  };

  useEffect(() => {
    fetch(`${API}/api/state`).then(r=>r.ok?r.json():Promise.reject()).then(setState).catch(()=>{});
    let socket;
    try {
      socket = new WebSocket(WS);
      socket.onopen = () => setConnected(true);
      socket.onclose = () => setConnected(false);
      socket.onerror = () => setConnected(false);
      socket.onmessage = e => { try { ingest(JSON.parse(e.data)); } catch {} };
    } catch {}
    return () => socket?.close();
  }, []);

  const start = async () => {
    setBusy(true);
    try {
      const r=await fetch(`${API}/api/battle/start`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({rounds:1})});
      const d=await r.json(); setState(d.state || d);
      if (d.rounds) setEvents(prev=>[...prev,{type:'battle_response',data:d.state}].slice(-40));
    } finally { setBusy(false); }
  };
  const reset = async () => {
    setBusy(true);
    try { const r=await fetch(`${API}/api/battle/reset`,{method:'POST'}); setState(await r.json()); setEvents([]); }
    finally { setBusy(false); }
  };

  const logLines = useMemo(() => events.slice(-8).reverse().map((e,i)=>({
    id:i,
    type:(e.type || 'EVENT').replaceAll('_',' ').toUpperCase(),
    text:e.message || (e.data?.status ? `Battle ${e.data.status} · Round ${e.data.round ?? 0}` : 'V-Core state updated')
  })),[events]);

  return <main className="shell">
    <div className="ambient redAmbient"/><div className="ambient blueAmbient"/>
    <header className="topbar">
      <div className="brand"><b>V-AGENTWAR</b><span>RED <i>VS</i> BLUE</span></div>
      <div className="topStatus"><span className={connected?'dot online':'dot'}/>{connected?'LIVE LINK':'LOCAL / OFFLINE'}<small>POWERED BY V-CORE</small></div>
    </header>

    <section className="arena">
      <article className="agentCard redCard"><span className="eyebrow">OFFENSIVE NODE</span><h2>RED AGENT</h2><strong>{state.red || 'READY'}</strong><p>ADAPTIVE ADVERSARY</p><div className="meter"><i style={{width:`${Math.min(100,state.red_score||0)}%`}}/></div></article>

      <div className="coreWrap">
        <div className="orbit orbitOne"/><div className="orbit orbitTwo"/>
        <div className="chip"><div className="chipGrid"/><span>V</span><small>CORE</small></div>
        <h1>V-CORE</h1><p>DUAL INTELLIGENCE ENGINE</p><b className="coreState">{state.vcore || 'OFFLINE'}</b>
        <div className="coreMeta"><span>RAG</span><span>MCP</span><span>MEMORY</span><span>JUDGE</span></div>
      </div>

      <article className="agentCard blueCard"><span className="eyebrow">DEFENSIVE NODE</span><h2>BLUE AGENT</h2><strong>{state.blue || 'READY'}</strong><p>ADAPTIVE DEFENDER</p><div className="meter"><i style={{width:`${Math.min(100,state.blue_score||0)}%`}}/></div></article>
    </section>

    <section className="scorebar">
      <div className="teamScore redScore"><b>{state.red_score || 0}</b><span>RED SCORE</span></div>
      <div className="battleControl"><span className="round">ROUND {String(state.round||0).padStart(2,'0')}</span><small>{state.status || 'IDLE'}</small><div><button disabled={busy} onClick={start}>{busy?'PROCESSING':'START BATTLE'}</button><button className="ghost" disabled={busy} onClick={reset}>RESET</button></div></div>
      <div className="teamScore blueScore"><b>{state.blue_score || 0}</b><span>BLUE SCORE</span></div>
    </section>

    <section className="bottomGrid">
      <div className="glassPanel eventPanel"><div className="panelTitle"><h3>LIVE BATTLE EVENTS</h3><span>{connected?'STREAMING':'WAITING'}</span></div>{logLines.length?logLines.map(x=><p key={x.id}><b>{x.type}</b><span>{x.text}</span></p>):<div className="empty">No battle events yet. Start a controlled round.</div>}</div>
      <div className="glassPanel statusPanel"><div className="panelTitle"><h3>RANGE STATUS</h3><span>SAFE MODE</span></div><dl><div><dt>V-Core</dt><dd>{state.vcore||'OFFLINE'}</dd></div><div><dt>Battle</dt><dd>{state.status||'IDLE'}</dd></div><div><dt>Memory</dt><dd>{state.memory?.length||0} rounds</dd></div><div><dt>Transport</dt><dd>{connected?'WebSocket':'REST fallback'}</dd></div></dl></div>
    </section>
    <footer>V-AGENTWAR // ADAPTIVE MULTI-AGENT CYBER RANGE <span>AUTHORIZED ISOLATED SIMULATION</span></footer>
  </main>;
}
