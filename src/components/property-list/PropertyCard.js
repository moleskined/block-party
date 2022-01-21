import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
} from "@mui/material";
import React from "react";
import axios from "axios";


export default class PropertyCard extends React.Component {
  constructor(props) {
    super(props);
    const {
      mode,
    } = this.props;

    if (mode === 'authority') {
      this.approve = this.approve.bind(this);
      this.disapprove = this.disapprove.bind(this);
    }
  }

  approve(e) {
    e.preventDefault();
    const { property } = this.props;
    this.setPropertyApproval(property.hash, property.property_address, true);
  }

  disapprove(e) {
    e.preventDefault();
    const { property } = this.props;
    this.setPropertyApproval(property.hash, property.property_address, false);
  }

  setPropertyApproval(id, propertyAddress, approved) {
    const payload = {
      id,
      approved,
      property_address: propertyAddress,
    };

    axios.put(`/api/permit-application/${id}/authority`, payload).then(res => { ;
      console.log(res.data);
    });
  }

  render() {
    const {
      property,
      mode
    } = this.props;

    return (
      <Card>
        <CardMedia
          component="img"
          height="140"
          image="/static/img/smol.jpeg"
        ></CardMedia>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">{property.property_address}</Typography>
          <Typography variant="body2" color="text.secondary">
            {property.timestamp}
            {property.seller_details}
            {property.seller_licence_number}
          </Typography>
        </CardContent>
        {mode === "seller" && (
          <CardActions>
            {/* <Button size="small">Share</Button>
            <Button size="small">Learn More</Button> */}
          </CardActions>
        )}
        {mode === "authority" && (
          <CardActions>
            <Button size="small" onClick={this.disapprove}>Disapprove</Button>
            <Button size="small" onClick={this.approve}>Approve</Button>
          </CardActions>
        )}
      </Card>
    );
  }
}
