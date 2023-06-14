import { UserContext } from "./UserContext";
import React, { useState, useContext } from "react";

export const LogoutButton = () => {
    const { setUser } = useContext(UserContext);

    const getCookie = (name) => {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

    const csrftoken = getCookie('csrftoken');
  
    const handleLogoutClick = () => {
      fetch("http://localhost:8000/mistake/logout/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
      })
      .then(response => {
        if (response.ok) {
          setUser(null);
        } else {
          console.error('Logout failed');
        }
      });
    }
  
    return <button onClick={handleLogoutClick}>Logout</button>;
  }
  