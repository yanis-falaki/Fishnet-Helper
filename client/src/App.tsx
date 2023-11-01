import React, {useState, useEffect} from 'react';
import { Header } from './components/Header';
import ChatContainer from './components/ChatContainer';

const App: React.FC = () => {
  return (
    <div className="flex flex-col text-center">
      <Header title='Fishnet Documentation ChatBot'/>
      <ChatContainer/>
    </div>
  );
}

export default App;
