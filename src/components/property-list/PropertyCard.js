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
        this.setPropertyApproval = this.props.setPropertyApproval.bind(this);
        break;

      case 'buyer':
        this.apply = this.props.apply.bind(this);
        break;

      default:
        break;
    }
  }

  approve(e) {
    e.preventDefault();
    const { property } = this.props;
    const permitApplication = property['PermitApplication'];
    this.setPropertyApproval(permitApplication.hash, permitApplication.property_address, true);
  }

  disapprove(e) {
    e.preventDefault();
    const { property } = this.props;
    const permitApplication = property['PermitApplication'];
    this.setPropertyApproval(permitApplication.hash, permitApplication.property_address, false);
  }

  render() {
    const {
      mode,
      property,
    } = this.props;

    // const approvalStatus = property.approval_status === null ? 'Pending' : Boolean(property.approval_status);
    const permitApplication = property['PermitApplication'];

    return (
      <Card>
        <CardMedia
          component="img"
          height="140"
          image="/static/img/smol.jpeg"
        ></CardMedia>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">{permitApplication.property_address}PermitApplication</Typography>
          <Typography variant="body2" color="text.secondary">
            {permitApplication.timestamp}PermitApplication
            {permitApplication.seller_details}PermitApplication
            {permitApplication.seller_licence_number}PermitApplication
          </Typography>
          <div>
            %APPROVAL STATUS%
            {/* Approval: {String(approvalStatus)} */}
          </div>
        </CardContent>
        {mode === "seller" && (
          <CardActions>
            {/* <Button size="small">Share</Button>
            <Button size="small">Learn More</Button> */}
          </CardActions>
        )}
        {mode === "authority" && !property['AuthorisationBlock'] && (
          <CardActions>
            <Button size="small" onClick={this.disapprove}>Disapprove</Button>
            <Button size="small" onClick={this.approve}>Approve</Button>
          </CardActions>
        )}
        {mode === 'buyer' && (
          <CardActions>
            <Button
              size="small"
              onClick={this.apply}
              disabled={ property.BuyerBlock }
            >Apply</Button> | STATUS OF BANK APPROVAL | STATUS OF SELLER APPROVAL
          </CardActions>
        )}
      </Card>
    );
  }
}
