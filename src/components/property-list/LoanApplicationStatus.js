import React from "react";
import PropTypes from 'prop-types';
import {
  Typography,
} from "@mui/material";

class LoanApplicationStatus extends React.Component {
  render() {
    const { block } = this.props;
    const permitApplication = block['PermitApplication'];
    const bankApproval = block['BankApproval'];
    const buyerBlock = block['BuyerBlock'];
    const saleFinalisationBlock = block['SaleFinalisationBlock'];

    if (saleFinalisationBlock) {
      return <Typography
        variant="body2"
        color="text.secondary"
      >{saleFinalisationBlock.approved ? 'Approved by Seller' : 'Rejected by Seller'}</Typography>;
    }

    if (bankApproval) {
      return <Typography
        variant="body2"
        color="text.secondary"
      >{bankApproval.approval_status ? 'Approved by Lender' : 'Rejected by Lender'}</Typography>;
    }

    return <Typography variant="body2" color="text.secondary">Pending</Typography>;
  }
}

LoanApplicationStatus.propTypes = {
  block: PropTypes.object.isRequired,
};

export default LoanApplicationStatus;