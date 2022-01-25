import React from "react";
import {
  Container,
  Grid,
  Box,
} from "@mui/material";
import axios from "axios";
import PropertyCard from "./PropertyCard";
import { buildChain } from "../utils";

const URL = '/api/v2/permit-application';

export default class Authorisation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      properties: [],
    };

    this.setPropertyApproval = this.setPropertyApproval.bind(this);
  }

  componentDidMount() {
    this.loadProperties();
  }

  loadProperties() {
    const url = '/api/v2/permit_applications';
    axios.get(url).then(response => {
      const data = [...response.data];
      const properties = data.map(d => buildChain(d))
      this.setState({ properties })
    })
  }

  setPropertyApproval(id, propertyAddress, approved) {
    const payload = {
      id,
      approved,
      property_address: propertyAddress,
    };

    axios.put(`${URL}/${id}/authority`, payload).then(res => {
      console.log(res.data);
      return this.loadProperties();
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
                    setPropertyApproval={this.setPropertyApproval}
                  ></PropertyCard>
                </Grid>))
            }
          </Grid>
        </Box>
      </Container>
    );
  }
}