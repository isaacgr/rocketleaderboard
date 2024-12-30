import React from "react";
import { ApolloProvider } from "@apollo/client/react";
import { ApolloClient, InMemoryCache } from "@apollo/client";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Players from "./components/Players";
import Sessions from "./components/Sessions";
import "./App.css";

const client = new ApolloClient({
  uri: "/graphql",
  cache: new InMemoryCache()
});

const App = () => {
  return (
    <ApolloProvider client={client}>
      <Router>
        <div className="container">
          <h1 className="title">Ball Buddies Leaderboard</h1>
          <Route exact path="/" component={Players}></Route>
          <Route path="/:playerId" component={Sessions}></Route>
        </div>
      </Router>
    </ApolloProvider>
  );
};

export default App;
