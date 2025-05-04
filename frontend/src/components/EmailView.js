import React, { useEffect, useState } from 'react';
import API from '../api';
import Questionnaire from './Questionnaire';

// Mock emails with behavior types and amounts
const emails = [
  { type: 'scarcity', text: 'Invoice #1: ... details ...', amount: 700 },
  { type: 'social_proof', text: 'Invoice #2: ... details ...', amount: 800 },
  { type: 'authority', text: 'Invoice #3: ... details ...', amount: 900 },
  { type: 'framing', text: 'Invoice #4: ... details ...', amount: 950 }
];

export default function EmailView({ userId, week, emailIndex, onNext }) {
  const email = emails[emailIndex];
  const [step, setStep] = useState('view');
  const handleChoice = async choice => {
    await API.post('/email', { user: userId, week, emailIndex, behaviorType: email.type, amount: email.amount, choice, timestamp: new Date() });
    setStep('q');
  };
  const handleComplete = async questions => {
    await API.post('/response', { user: userId, week, emailIndex, questions });
    onNext();
  };

  if (step === 'view') return (
    <div className="panel email-panel">
      <h3>Week {week}, Email {emailIndex+1}</h3>
      <div className="email-box">
        <p>{email.text}</p>
        <p>Amount: {email.amount}€</p>
      </div>
      <div className="btn-row">
        <button onClick={() => handleChoice('pay')}>Pay now</button>
        <button onClick={() => handleChoice('wait')}>Wait a week</button>
      </div>
    </div>
  );
  return <Questionnaire onSubmit={handleComplete} />;
}