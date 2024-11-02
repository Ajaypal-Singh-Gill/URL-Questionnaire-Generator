import React from "react";
import { Provider } from "react-redux";
import store from "./redux/store";
import Questionnaire from "./components/Questionnaire";

const App = () => {
  return (
    <Provider store={store}>
      <div className="App">
        <Questionnaire />
      </div>
    </Provider>
  );
};

export default App;
