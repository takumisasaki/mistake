import './App.css';
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

import { Header } from "./components/Header";
import { Home } from "./components/Home";
import { Login } from "./components/Login";
import { UserContext } from "./components/UserContext";
import { DisplayUsername } from "./components/DisplayUsername";
import  {Signup} from "./components/Signup"

export function LoginButton() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  }

  return <button onClick={handleLoginClick}>Login</button>;
}

function App() {
  const [user, setUser] = useState(null);

  return (
    <div className="App">
      <Router> 
        <UserContext.Provider value={{ user, setUser }}>
          <Header />
          {user && <p>Welcome, {user}</p>}
          <DisplayUsername />
        </UserContext.Provider>
        <Home />
        {/* <Signup /> */}
      </ Router>
    </div>
  );
}

export default App;