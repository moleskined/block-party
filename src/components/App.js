import React from "react";
import { render } from "react-dom";
import CssBaseline from '@mui/material/CssBaseline';
import { PropertyList } from './property-list';
import { TopBar } from './top-bar';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const lightTheme = createTheme({
  palette: {
    background: {
      default: "#EEE"
    }
  }
});

class App extends React.Component {
  render() {
    return (
      <React.StrictMode>
        <ThemeProvider theme={lightTheme}>
          <CssBaseline />
          <TopBar />
          <PropertyList></PropertyList>
        </ThemeProvider>
      </React.StrictMode>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);