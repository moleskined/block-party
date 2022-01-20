import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardMedia,
  Container,
  Fab,
  Grid,
  Typography,
} from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import AddIcon from '@mui/icons-material/Add';
import NewPermitApplicationDialogue from "./NewPermitApplicationDialogue";

const DummyCard = () => (<Card>
  <CardMedia></CardMedia>
  <CardContent>
    <Typography gutterBottom variant="h5" component="div">71 Augustine Street</Typography>
    <Typography variant="body2" color="text.secondary">
      Lizards are a widespread group of squamate reptiles, with over 6,000
      species, ranging across all continents except Antarctica
    </Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Share</Button>
    <Button size="small">Learn More</Button>
  </CardActions>
</Card>);

class PropertyList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showAddNewPropertyDialogue: false,
      showAddNewPropertyFab: true,
    };

    this.handleNewPropertyClick = this.handleNewPropertyClick.bind(this);
    this.handleNewPropertyClose = this.handleNewPropertyClose.bind(this);
  }

  handleNewPropertyClick() {
    this.setState(prev => ({
      ...prev,
      showAddNewPropertyDialogue: true,
    }));
  }

  handleNewPropertyClose() {
    this.setState(prev => ({
      ...prev,
      showAddNewPropertyDialogue: false,
    }));
  }

  render() {
    const {
      showAddNewPropertyDialogue,
      showAddNewPropertyFab,
    } = this.state;

    return (
      <Container>
        <NewPermitApplicationDialogue
          showAddNewPropertyDialogue={showAddNewPropertyDialogue}
          handleNewPropertyClose={this.handleNewPropertyClose}
          onSubmitProperty={props => { console.log(props); }}
        ></NewPermitApplicationDialogue>
        <Box sx={{ my: 2 }}>
          {
            showAddNewPropertyFab && (
              <Fab
                color="primary"
                aria-label="add"
                sx={{ position: 'fixed', bottom: 16, right: 16 }}
                onClick={this.handleNewPropertyClick}
              >
                <AddIcon />
              </Fab>
            )
          }
          <Grid container spacing={2}>
            {
              [...new Array(0)].map(() => (
                <Grid item xs={12} sm={6} md={4}>
                  <DummyCard></DummyCard>
                </Grid>))
            }
          </Grid>
        </Box>
      </Container>
    );
  }
}

export default PropertyList;