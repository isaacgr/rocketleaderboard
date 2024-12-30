import React, { Fragment } from "react";
import { useQuery, gql } from "@apollo/client";
import moment from "moment";
import PlayerHeader from "./PlayerHeader";
import Overview from "./Overview";

const SESSIONS_QUERY = gql`
  query SessionQuery($id: String!) {
    sessions(id: $id) {
      metadata {
        startDate {
          value
        }
        endDate {
          value
        }
      }
      matches {
        metadata {
          playlist
          result
          dateCollected {
            value
          }
        }
        stats {
          goals {
            value
            displayName
            displayValue
          }
          assists {
            value
            displayName
            displayValue
          }
          saves {
            value
            displayName
            displayValue
          }
          shots {
            value
            displayName
            displayValue
          }
          matchesPlayed {
            value
            displayName
            displayValue
          }
          wins {
            value
            displayName
            displayValue
          }
        }
      }
    }
  }
`;

const Sessions = (props) => {
  const { loading, error, data } = useQuery(SESSIONS_QUERY, {
    variables: { id: props.match.params.playerId },
    fetchPolicy: "no-cache"
  });
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
    <div className="sessions-card card card-body mb-3">
      <div className="player-header card-header">
        <PlayerHeader data={props.location.state} />
      </div>
      <div className="player-header">
        <h4 lassName="player-header__name">Recent Matches</h4>
      </div>
      {data.sessions.map((session) => {
        return (
          <div
            key={Math.random().toString()}
            className="sessions-overview playlist-stats"
          >
            <h4 className="note">
              {moment(session.metadata.endDate.value).format("LLL")}
            </h4>
            {session.matches
              .filter(
                (match) =>
                  match.stats.wins.value || match.stats.matchesPlayed.value
              )
              .map((match) => {
                return (
                  <Fragment key={Math.random().toString()}>
                    <Overview
                      overview={match.stats}
                      header={match.metadata.playlist}
                    />
                  </Fragment>
                );
              })}
          </div>
        );
      })}
    </div>
  );
};

export default Sessions;
