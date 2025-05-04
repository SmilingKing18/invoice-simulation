import React, { useState } from 'react';
import API from '../api';

export default function FinalQuestionnaire({ userId }) {
  const [data, setData] = useState({
    q1: '',
    q2: '',
    q3: ''
  });
  const submit = async () => {
    await API.post('/final', { user: userId, final: data });
    alert('Thank you!');
  };
  return (
    <div className="panel">
      <h2>Final Thoughts</h2>
      <textarea placeholder="Would sender title (CEO vs assistant) change behavior?" value={data.q1} onChange={e=>setData({...data, q1:e.target.value})}/>
      <textarea placeholder="Which email felt most persuasive and why?" value={data.q2} onChange={e=>setData({...data, q2:e.target.value})}/>
      <textarea placeholder="Any additional comments?" value={data.q3} onChange={e=>setData({...data, q3:e.target.value})}/>
      <button onClick={submit}>Finish</button>
    </div>
  );
}