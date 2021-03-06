import React from "react";
import { render } from "react-dom";
import CssBaseline from '@mui/material/CssBaseline';
import { TopBar } from './top-bar';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {
  PropertyList,
  Authorisation,
  Buyers,
  Bank,
} from './property-list';

const lightTheme = createTheme({
  palette: {
    background: {
      default: "#EEE"
    }
  }
});

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      roleId: ROLE_ID,
    };
  }

  render() {
    const { roleId } = this.state;

    return (
      <React.StrictMode>
        <ThemeProvider theme={lightTheme}>
          <CssBaseline />
          <TopBar />
          {roleId === 1 && <PropertyList></PropertyList>}
          {roleId === 2 && <Authorisation></Authorisation>}
          {roleId === 3 && <Buyers></Buyers>}
          {roleId === 4 && <Bank></Bank>}
        </ThemeProvider>
      </React.StrictMode>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);