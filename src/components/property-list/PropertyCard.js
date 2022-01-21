import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
} from "@mui/material";
import React from "react";

export default class PropertyCard extends React.Component {
  constructor(props) {
    super(props);
    const {
      mode,
    } = this.props;

    switch (mode) {
      case 'authority':
        this.approve = this.approve.bind(this);
        this.disapprove = this.disapprove.bind(this);
        this.setPropertyApproval = props.setPropertyApproval.bind(this);
        break;

      case 'buyer':
        break;
    
      default:
        break;
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

  render() {
    const {
      property,
      mode
    } = this.props;

    const approvalStatus = property.approval_status === null ? 'Pending' : Boolean(property.approval_status);

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
            <div>
              Approval: {String(approvalStatus)}
            </div>
        </CardContent>
        {mode === "seller" && (
          <CardActions>
            {/* <Button size="small">Share</Button>
            <Button size="small">Learn More</Button> */}
          </CardActions>
        )}
        {mode === "authority" && property.approval_status === null && (
          <CardActions>
            <Button size="small" onClick={this.disapprove}>Disapprove</Button>
            <Button size="small" onClick={this.approve}>Approve</Button>
          </CardActions>
        )}
      </Card>
    );
  }
}
