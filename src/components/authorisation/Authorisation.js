import React from "react";
import {
  Container,
  Grid,
  Box,
} from "@mui/material";
import axios from "axios";
import { PropertyCard } from "../property-card";

export default class Authorisation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      properties: [],
    };
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
    });
  }

  render() {
    const {
      properties,
    } = this.state;

    return (
      <Container>
        <Box sx={{ my: 2 }}>
          <Grid container spacing={2}>
            {
              [...properties].map((p, i) => (
                <Grid key={i} item xs={12} sm={6} md={4}>
                  <PropertyCard
                    property={p}
                    mode="authority"
                  ></PropertyCard>
                </Grid>))
            }
          </Grid>
        </Box>
      </Container>
    );
  }
}