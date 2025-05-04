import React, { useState } from 'react';
import Demographics from './components/Demographics';
import Rules from './components/Rules';
import EmailView from './components/EmailView';
import FinalQuestionnaire from './components/FinalQuestionnaire';

function App() {
  const [stage, setStage] = useState('demographics');
  const [userId, setUserId] = useState(null);
  const [week, setWeek] = useState(1);
  const [emailIndex, setEmailIndex] = useState(0);

  const next = () => {
    if (stage === 'demographics') setStage('rules');
    else if (stage === 'rules') setStage('emails');
    else if (stage === 'emails') {
      // advance email
      if (emailIndex < 3) setEmailIndex(emailIndex + 1);
      else if (week < 3) { setEmailIndex(0); setWeek(week + 1); }
      else setStage('final');
    }
  };

  return (
    <div className="app-container">
      {stage === 'demographics' && <Demographics onNext={(id) => { setUserId(id); next(); }} />}
      {stage === 'rules' && <Rules onNext={next} />}
      {stage === 'emails' && <EmailView userId={userId} week={week} emailIndex={emailIndex} onNext={next} />}
      {stage === 'final' && <FinalQuestionnaire userId={userId} />}
    </div>
  );
}

export default App;