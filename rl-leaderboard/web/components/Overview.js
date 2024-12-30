import React from "react";

export default function Overview({ overview, header, classNames }) {
  return (
    <table className={`${classNames || ""} stats__table`}>
      {header ? (
        <tbody>
          <tr>
            <th colspan="2">{header}</th>
          </tr>
        </tbody>
      ) : (
        ""
      )}
      {Object.keys(overview)
        .filter((stat) => {
          if (stat === "__typename" || stat === "seasonRewardLevel") {
            return false;
          }
          return true;
        })
        .map((stat) => {
          return (
            <tbody key={overview[stat].value}>
              <tr>
                <td>{overview[stat].displayName.toUpperCase()}</td>
                <td>{overview[stat].displayValue}</td>
              </tr>
            </tbody>
          );
        })}
    </table>
  );
}
