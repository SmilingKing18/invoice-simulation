import React, { useState } from 'react';
import API from '../api';

export default function Demographics({ onNext }) {
  const [data, setData] = useState({ age: '', gender: '', education: '', location: '' });
  const submit = async () => {
    const res = await API.post('/user', data);
    onNext(res.data.userId);
  };
  return (
    <div className="panel">
      <h2>Demographics</h2>
      <input placeholder="Age" value={data.age} onChange={e => setData({...data, age: e.target.value})}/>
      <input placeholder="Gender" value={data.gender} onChange={e => setData({...data, gender: e.target.value})}/>
      <input placeholder="Education" value={data.education} onChange={e => setData({...data, education: e.target.value})}/>
      <input placeholder="Location" value={data.location} onChange={e => setData({...data, location: e.target.value})}/>
      <button onClick={submit}>Next</button>
    </div>
  );
}