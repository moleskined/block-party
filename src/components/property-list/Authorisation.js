import React from "react";
import {
  Container,
  Grid,
  Box,
} from "@mui/material";
import axios from "axios";
import PropertyCard from "./PropertyCard";

const URL = '/api/permit-application';

export default class Authorisation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      properties: [],
    };
  }

  componentDidMount() {
    this.loadProperties();
  }

  loadProperties() {
    const config = {};
    axios.get(URL).then(response => {
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