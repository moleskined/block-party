import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
} from "@mui/material";
import React from "react";

export default class PropertyCard extends React.Component {
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
            <Button size="small">Share</Button>
            <Button size="small">Learn More</Button>
          </CardActions>
        )}
        {mode === "authority" && (
          <CardActions>
            <Button size="small">Disapprove</Button>
            <Button size="small">Approve</Button>
          </CardActions>
        )}
      </Card>
    );
  }
}
