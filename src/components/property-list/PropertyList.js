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
import PropertyCard from "./PropertyCard";
import { buildChain } from "../utils";
import CompleteDeal from "./CompleteDeal";

class PropertyList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showAddNewPropertyDialogue: false,
      showAddNewPropertyFab: true,
      properties: [],
      showing: false, 
      property: null,
    };

    this.handleNewPropertyClick = this.handleNewPropertyClick.bind(this);
    this.handleNewPropertyClose = this.handleNewPropertyClose.bind(this);
    this.showCompleteDeal = this.showCompleteDeal.bind(this);
    this.closeCompleteDetail = this.closeCompleteDetail.bind(this);
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
    const url = '/api/v2/permit_applications';
    return axios.get(url).then(response => {
      const data = [...response.data];
      const properties = data.map(d => buildChain(d))
      this.setState({ properties })
    })
  }

  showCompleteDeal(property) {
    this.setState({ showing: true, property });
  }

  closeCompleteDetail(response) {
    this.setState({ showing: false });

    if (response) {
      console.log(response);
    }

    return this.loadPropertiest();
  }

  render() {
    const {
      showAddNewPropertyDialogue,
      showAddNewPropertyFab,
      properties,
      showing,
      property,
    } = this.state;

    return (
      <>
        <CompleteDeal
          showing={showing}
          block={property}
          handleClose={this.closeCompleteDetail}
        ></CompleteDeal>
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
                      finaliseDeal={this.showCompleteDeal}
                    ></PropertyCard>
                  </Grid>))
              }
            </Grid>
          </Box>
        </Container>
      </>
    );
  }
}

export default PropertyList;
