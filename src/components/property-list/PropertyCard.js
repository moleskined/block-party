import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
  TextField,
  IconButton,
} from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import AssignmentIcon from '@mui/icons-material/Assignment';
import DownloadIcon from '@mui/icons-material/Download';

export default class PropertyCard extends React.Component {
  constructor(props) {
    super(props);
    const {
      mode,
    } = this.props;

    this.downloadPdf = this.downloadPdf.bind(this);

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

  downloadPdf(block) {
    window.location = `/api/v2/permit_applications/${block.hash}/pdf`;
  }

  render() {
    const {
      mode,
      property,
    } = this.props;

    // const approvalStatus = property.approval_status === null ? 'Pending' : Boolean(property.approval_status);
    const permitApplication = property['PermitApplication'];
    const bankApproval = property['BankApproval'];
    const buyerBlock = property['BuyerBlock'];

    return (
      <Card>
        <CardMedia
          component="img"
          height="140"
          image="/static/img/smol.jpeg"
        ></CardMedia>
        <CardContent>
          <Box sx={{ display: 'flex' }}>
            <Box sx={{ flexGrow: 1 }}>
              <Typography gutterBottom variant="h5" component="h2" style={{ minHeight: '4rem' }}>
                {permitApplication.property_address}
              </Typography>
            </Box>
            <Box>
              <IconButton aria-label="Download building plans" onClick={() => this.downloadPdf(permitApplication)}>
                <DownloadIcon></DownloadIcon>
              </IconButton>
            </Box>

          </Box>

          {mode === 'buyer' && <><Typography variant="subtitle1">Loan Application ID</Typography>
            <Typography variant="body2" color="text.secondary" component="div">
              <Box style={{ display: 'flex', alignItems: 'center' }}>
                <Box>
                  <IconButton disabled={buyerBlock == null} onClick={() => navigator.clipboard.writeText(buyerBlock?.hash)} aria-label="Copy to cliboard">
                    <AssignmentIcon></AssignmentIcon>
                  </IconButton>
                </Box>
                <Box style={{ textOverflow: 'ellipsis', overflow: 'hidden' }}>{buyerBlock?.hash || 'Available after application'}</Box>
              </Box>
            </Typography>
            {
              buyerBlock && <>
                <Typography variant="subtitle1">Loan Application Status</Typography>
                {bankApproval ? <>
                  <Typography variant="body2" color="text.secondary">{bankApproval.approval_status ? 'Approved by Lender' : 'Rejected by Lender'}</Typography>
                </> : <>
                  <Typography variant="body2" color="text.secondary">Pending</Typography>
                </>}
              </>
            }
          </>}

          {mode === 'seller' && <><Typography variant="subtitle1">Permit Application ID</Typography>
            <Typography variant="body2" color="text.secondary" component="div">
              <Box style={{ display: 'flex', alignItems: 'center' }}>
                <Box>
                  <IconButton onClick={() => navigator.clipboard.writeText(permitApplication.hash)} aria-label="Copy to cliboard">
                    <AssignmentIcon></AssignmentIcon>
                  </IconButton>
                </Box>
                <Box style={{ textOverflow: 'ellipsis', overflow: 'hidden' }}>{permitApplication.hash}</Box>
              </Box>
            </Typography>
            <Typography variant="subtitle1">Loan Application Status</Typography>
            {bankApproval ? <>
              <Typography variant="body2" color="text.secondary">{bankApproval.approval_status ? 'Approved by Lender' : 'Rejected by Lender'}</Typography>
            </> : <>
              <Typography variant="body2" color="text.secondary">Pending</Typography>
            </>}
          </>}


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
              disabled={property.BuyerBlock && true}
            >Apply</Button>
          </CardActions>
        )}
      </Card>
    );
  }
}
