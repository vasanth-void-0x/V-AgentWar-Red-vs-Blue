'use client';
import { useEffect, useState } from 'react';
import './style.css';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [state, setState] = useState({round:0,status:'IDLE',red_score:0,blue_score:0,vcore:'OFFLINE',red:'READY',blue:'READY'});
  const [events, setEvents] = useState([]);
  const refresh = async () => { try { const r=await fetch(`${API}/api/state`); setState(await r.json()); } catch {} };
  useEffect(()=>{ refresh(); },[]);
  const start = async () => { const r=await fetch(`${API}/api/battle/start`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({rounds:1})}); const d=await r.json(); setState(d.state); setEvents(d.events||[]); };
  const reset = async () => { const r=await fetch(`${API}/api/battle/reset`,{method:'POST'}); setState(await r.json()); setEvents([]); };

  return <main className="shell">
    <header><div><b>V-AGENTWAR</b><span> RED vs BLUE</span></div><small>POWERED BY V-CORE</small></header>
    <section className="arena">
      <div className="glow red"></div><div className="glow blue"></div>
      <div className="agent redCard"><h2>RED AGENT</h2><strong>{state.red}</strong><p>ADAPTIVE ADVERSARY</p></div>
      <div className="core"><div className="chip"><span>V</span></div><h1>V-CORE</h1><p>DUAL INTELLIGENCE ENGINE</p><b>{state.vcore}</b></div>
      <div className="agent blueCard"><h2>BLUE AGENT</h2><strong>{state.blue}</strong><p>ADAPTIVE DEFENDER</p></div>
    </section>
    <section className="score"><div><b>{state.red_score}</b><span>RED</span></div><div className="round"><span>ROUND {String(state.round).padStart(2,'0')}</span><button onClick={start}>START BATTLE</button><button onClick={reset}>RESET</button></div><div><b>{state.blue_score}</b><span>BLUE</span></div></section>
    <section className="panels"><div className="panel"><h3>LIVE BATTLE EVENTS</h3>{events.slice(-7).reverse().map((e,i)=><p key={i}><b>{e.actor}</b> — {e.message}</p>)}</div><div className="panel"><h3>RANGE STATUS</h3><p>V-Core: {state.vcore}</p><p>Battle: {state.status}</p><p>Memory rounds: {state.memory?.length||0}</p></div></section>
  </main>;
}
