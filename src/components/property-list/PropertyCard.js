import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
} from "@mui/material";
import React from "react";

export class PropertyCard extends React.Component {
  render() {
    const { property } = this.props;

    return (
      <Card>
        <CardMedia
          component="img"
          height="140"
          image="/static/img/smol.jpeg"
        ></CardMedia>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">{ property.property_address }</Typography>
          <Typography variant="body2" color="text.secondary">
            { property.timestamp }
            { property.seller_details }
            { property.seller_licence_number }
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Share</Button>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>
    );
  }
}
