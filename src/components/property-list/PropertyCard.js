import {
  Button,
  Card,
  CardActions,
  CardContent, Typography,
  CardMedia,
  TextField,
  IconButton,
  Tooltip,
} from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import AssignmentIcon from '@mui/icons-material/Assignment';
import DownloadIcon from '@mui/icons-material/Download';
import LoanApplicationStatus from "./LoanApplicationStatus";

export default class PropertyCard extends React.Component {
  constructor(props) {
    super(props);
    const {
      mode,
      finaliseDeal,
    } = this.props;
    this.state = {
      showing: false,
      block: null,
    };

    this.downloadPdf = this.downloadPdf.bind(this);
    this.finaliseDeal = finaliseDeal || function () { };

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
    const {
      showing,
      block,
    } = this.state;

    const permitApplication = property['PermitApplication'];
    const bankApproval = property['BankApproval'];
    const buyerBlock = property['BuyerBlock'];
    const saleFinalisationBlock = property['SaleFinalisationBlock'];

    return (
      <>
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
                <Tooltip title="Download building plans">
                  <IconButton aria-label="Download building plans" onClick={() => this.downloadPdf(permitApplication)}>
                    <DownloadIcon></DownloadIcon>
                  </IconButton>
                </Tooltip>
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
                  <LoanApplicationStatus
                    block={property}
                  ></LoanApplicationStatus>
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
              <LoanApplicationStatus
                block={property}
              ></LoanApplicationStatus>
            </>}


          </CardContent>
          {mode === "seller" && bankApproval && !saleFinalisationBlock && (
            <CardActions>
              <Button
                size="small"
                onClick={() => this.finaliseDeal(property)}
                disabled={!bankApproval.approval_status}
              >Verify &amp; Complete…</Button>
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
        </Card></>
    );
  }
}
