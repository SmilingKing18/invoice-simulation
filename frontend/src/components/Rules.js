import React from 'react';
export default function Rules({ onNext }) {
  return (
    <div className="panel">
      <h2>THE RULES</h2>
      <div className="rules-box">
        <p>You start with 1000€.</p>
        <p>4 emails per week for 3 weeks.</p>
        <p>Each email asks to pay part of an invoice (amount exceeds budget if you pay all).</p>
        <p>At bottom: "Pay now" or "Wait a week".</p>
        <p>After each: questionnaire on urgency, arousal, persuasion, trust (1-5).</p>
        <p>Week 2 & 3 adapt based on prior payments.</p>
        <p>Final questionnaire at end.</p>
      </div>
      <button onClick={onNext}>Start</button>
    </div>
  );
}