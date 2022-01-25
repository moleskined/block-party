import { AppBar, IconButton, Toolbar, Typography } from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import MenuIcon from '@mui/icons-material/Menu';
import Button from '@mui/material/Button';

class TopBar extends React.Component {
  render() {
    return (
      <React.Fragment>
        <AppBar position="fixed">
          <Toolbar>
            {/* <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton> */}
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Properties
            </Typography>
            <Button color="inherit" onClick={() => window.location='/logout'}>Logoff</Button>
          </Toolbar>
        </AppBar>
        <Toolbar />
      </React.Fragment>
    );
  }
}

export default TopBar;