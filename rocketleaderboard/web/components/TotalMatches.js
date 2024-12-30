import React from "react";

export default function TotalMatches({ totalMatches }) {
  return (
    <div className="playlist-stats">
      <h3 className="sub-title">MATCHES THIS SEASON</h3>
      <table className="stats__table">
        <tbody key="total-matches">
          <tr>
            <td>TOTAL</td>
            <td>{totalMatches}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
