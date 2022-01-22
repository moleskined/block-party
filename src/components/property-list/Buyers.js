import React from "react";
import {
  Container,
  Grid,
  Box,
} from "@mui/material";
import axios from "axios";
import PropertyCard from "./PropertyCard";
import { buildChain } from "../utils";
import BuyersApplicationForm from "./BuyersApplicationForm";

class Buyers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      properties: [],
      showing: null,
    };

    this.apply = this.apply.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  componentDidMount() {
    this.loadProps();
  }

  loadProps() {
    const url = '/api/v2/permit_applications/available-for-purchase';
    axios.get(url).then(response => {
      const data = [...response.data];
      const properties = data.map(d => buildChain(d))
      this.setState({ properties })
    })
  }

  apply(property) {
    this.setState({ showing: property });
  }

  handleClose() {
    this.setState({ showing: null });
  }

  onSubmit(buyerDetails) {
    const url = `/api/v2/buyer_applications/${buyerDetails.previous_hash}`;
    const payload = { ...buyerDetails };
    axios.post(url, payload).then(response => {
      const data = response.data;
      console.log(data);
    }).finally(() => {
      this.setState({ showing: null });
      return this.loadProps();
    });
  }

  render() {
    const {
      properties,
      showing,
    } = this.state;
    
    return (
      <Container>
        <BuyersApplicationForm
          showing={showing}
          handleClose={this.handleClose}
          onSubmit={this.onSubmit}
        ></BuyersApplicationForm>
        <Box sx={{ my: 2 }}>
          <Grid container spacing={2}>
            {
              [...properties].map((p, i) => (
                <Grid key={i} item xs={12} sm={6} md={4}>
                  <PropertyCard
                    property={p}
                    mode="buyer"
                    apply={() => this.apply(p)}
                  ></PropertyCard>
                </Grid>))
            }
          </Grid>
        </Box>
      </Container>
    );
  }
}

export default Buyers;