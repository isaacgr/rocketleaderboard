import React from "react";
import Player from "./Player";

const ballBuddies = [
  "76561197995010826",
  "76561198016163269",
  "76561197996271106"
];

const Players = () => {
  return (
    <div className="players-list">
      {ballBuddies.map((id) => {
        return <Player key={id} playerId={id} />;
      })}
    </div>
  );
};

export default Players;
