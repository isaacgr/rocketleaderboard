const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLSchema,
  GraphQLInt
} = require("graphql");

const { PlayerType, SessionsList, SegmentList } = require("./types");

const axios = require("axios");

const RootQuery = new GraphQLObjectType({
  name: "RootQueryType",
  fields: {
    player: {
      type: PlayerType,
      description: "Retrieve lifetime stats for a player",
      args: {
        id: { type: GraphQLString }
      },
      resolve(parent, args) {
        return axios
          .get(`http://127.0.0.1:8080/player?id=${args.id}`)
          .then((res) => res.data.data);
      }
    },
    segments: {
      type: SegmentList,
      description:
        "Retrieve a players stats in each playlist for a given season",
      args: {
        id: { type: GraphQLString },
        season: { type: GraphQLInt }
      },
      resolve(parent, args) {
        return axios
          .get(
            `http://127.0.0.1:8080/playlist?id=${args.id}&season=${args.season}`
          )
          .then((res) => res.data.data);
      }
    },
    sessions: {
      type: SessionsList,
      description: "Retreive stats for recent matches",
      args: {
        id: { type: GraphQLString }
      },
      resolve(parent, args) {
        return axios
          .get(`http://127.0.0.1:8080/sessions?id=${args.id}`)
          .then((res) => res.data.data.items.slice(0, 10));
      }
    }
  }
});

module.exports = new GraphQLSchema({
  query: RootQuery
});
