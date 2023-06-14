import React, { useContext } from "react";
import { UserContext } from "./UserContext";

export const DisplayUsername = () => {
  const { user } = useContext(UserContext);
  return (
    <div>
      {user ? `Hello, ${user}!` : "You are not logged in."}
    </div>
  );
};
