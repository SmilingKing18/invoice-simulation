import React, { useState } from 'react';

const questions = [
  'How urgent did you feel the email was?',
  'How emotionally aroused did you feel?',
  'How persuasive was the email?',
  'How much did you trust the sender?'
];

export default function Questionnaire({ onSubmit }) {
  const [answers, setAnswers] = useState([1,1,1,1]);
  const submit = () => onSubmit(answers);
  return (
    <div className="panel">
      {questions.map((q,i) => (
        <div key={i} className="q-row">
          <p>{q}</p>
          <div className="scale">
            {[1,2,3,4,5].map(n => (
              <span key={n} className={answers[i]===n?'dot selected':'dot'} onClick={() => {
                const a = [...answers]; a[i] = n; setAnswers(a);
              }}>{n}</span>
            ))}
          </div>
        </div>
      ))}
      <button onClick={submit}>Submit</button>
    </div>
  );
}