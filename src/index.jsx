import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader'; // required
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import injectTapEventPlugin from 'react-tap-event-plugin';

import App from './components/App';

import './index.scss';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

function renderApp() {
  // We now render `<AppContainer>` instead of our App component.
  ReactDOM.render(
    <AppContainer>
      <MuiThemeProvider>
        <App />
      </MuiThemeProvider>
    </AppContainer>,
    document.getElementById('main')
  );
}

renderApp(); // Renders App on init

if (module.hot) {
  // Renders App every time a change in code happens.
  module.hot.accept('./components/App.jsx', renderApp);
}
