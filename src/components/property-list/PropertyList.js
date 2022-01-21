import {
  CardMedia,
  Container,
  Fab,
  Grid,
} from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import AddIcon from '@mui/icons-material/Add';
import NewPermitApplicationDialogue from "./NewPermitApplicationDialogue";
import axios from "axios";
import { PropertyCard } from "../property-card";

class PropertyList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showAddNewPropertyDialogue: false,
      showAddNewPropertyFab: true,
      properties: [],
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
    this.loadPropertiest();
  }

  componentDidMount() {
    this.loadPropertiest();
  }

  loadPropertiest() {
    const url = '/api/permit-application';
    const config = {};
    axios.get(url).then(response => {
      const properties = [...response.data];
      this.setState({ properties })
    })
  }

  render() {
    const {
      showAddNewPropertyDialogue,
      showAddNewPropertyFab,
      properties,
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
              [...properties].map((p, i) => (
                <Grid key={i} item xs={12} sm={6} md={4}>
                  <PropertyCard
                    property={p}
                    mode="seller"
                  ></PropertyCard>
                </Grid>))
            }
          </Grid>
        </Box>
      </Container>
    );
  }
}

export default PropertyList;