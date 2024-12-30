import React from "react";

const PlayerHeader = ({ data }) => {
  return (
    <>
      <div className="player-header--content">
        <img
          alt="img"
          src={data.platformInfo.avatarUrl}
          style={{ height: 100, width: 100, display: "block" }}
        />
        <h4 className="player-header__name">
          {data.platformInfo.platformUserHandle}
        </h4>
      </div>
      <div className="player-header--content">
        <img
          alt="img"
          src={data.overview.seasonRewardLevel.metadata.iconUrl}
          style={{ height: 100, width: 100, display: "block" }}
        />
        <h3 className="player-header__name">
          {data.overview.seasonRewardLevel.metadata.rankName} Rewards
        </h3>
      </div>
    </>
  );
};

export default PlayerHeader;
