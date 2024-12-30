import React, { useState, useEffect } from "react";
import { useQuery, gql } from "@apollo/client";
import TotalMatches from "./TotalMatches";

const SEGMENTS_QUERY = gql`
  query SeasonQuery($id: String!, $season: Int!) {
    segments(id: $id, season: $season) {
      type
      metadata {
        name
      }
      stats {
        tier {
          metadata {
            name
          }
        }
        division {
          metadata {
            name
          }
        }
        matchesPlayed {
          value
        }
        winStreak {
          value
        }
        rating {
          value
        }
      }
    }
  }
`;

const validPlaylists = [
  "Ranked Duel 1v1",
  "Ranked Doubles 2v2",
  "Ranked Standard 3v3",
  "Hoops",
  "Tournament Matches"
];

const Segments = ({ playerId, season }) => {
  const { loading, error, data } = useQuery(SEGMENTS_QUERY, {
    variables: { id: playerId, season: parseInt(season) },
    fetchPolicy: "no-cache"
  });
  const [matches, setMatches] = useState(0);
  useEffect(() => {
    if (!data) {
      return;
    }
    setMatches(0);
    data.segments
      .filter((playlist) => {
        const name = playlist.metadata.name;
        if (validPlaylists.includes(name)) {
          return true;
        }
        return false;
      })
      .forEach((playlist) => {
        Object.keys(playlist.stats)
          .filter((stat) => {
            if (stat === "__typename") {
              return false;
            }
            return true;
          })
          .forEach((stat) => {
            if (stat === "matchesPlayed") {
              setMatches((prevState) => prevState + playlist.stats[stat].value);
            }
          });
      });
  }, [data]);
  if (loading) return <h2 className="sub-title">Loading...</h2>;
  if (error) {
    console.log(error);
    return (
      <h2 className="sub-title" id="error">{`Error: ${error.message}`}</h2>
    );
  }
  if (data.length === 0) {
    return (
      <h2 className="sub-title" id="error">
        No data
      </h2>
    );
  }
  return (
    <>
      <TotalMatches totalMatches={matches} />
      {data.segments
        .filter((playlist) => {
          const name = playlist.metadata.name;
          if (validPlaylists.includes(name)) {
            return true;
          }
          return false;
        })
        .map((playlist) => {
          return (
            <div key={playlist.metadata.name} className="playlist-stats">
              <h3 className="sub-title">{playlist.metadata.name}</h3>
              <table className="stats__table">
                {Object.keys(playlist.stats)
                  .filter((stat) => {
                    if (stat === "__typename") {
                      return false;
                    }
                    return true;
                  })
                  .map((stat) => {
                    return (
                      <tbody
                        key={
                          playerId +
                          playlist.metadata.name +
                          (playlist.stats[stat].metadata
                            ? playlist.stats[stat].metadata.name
                            : playlist.stats[stat].value)
                        }
                      >
                        <tr>
                          <td>{stat.toUpperCase()}</td>
                          <td>
                            {playlist.stats[stat].metadata
                              ? playlist.stats[stat].metadata.name
                              : playlist.stats[stat].value}
                          </td>
                        </tr>
                      </tbody>
                    );
                  })}
              </table>
            </div>
          );
        })}
    </>
  );
};

export default Segments;
