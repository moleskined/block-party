import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Box, Button, TextField, InputAdornment } from "@mui/material";
import React from "react";
import { Component } from "react";
import PropTypes from 'prop-types';

const DEFAULT_STATE = {
  buyerDetails: {},
};


const textFieldStyle = { mt: 2 };

class BuyersApplicationForm extends Component {
  constructor(props) {
    super(props);
    const { showing } = this.props;
    this.state = {
      ...DEFAULT_STATE,
    };
    this.handleOnSubmit = this.handleOnSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidUpdate(prevProps) {
    const { showing } = this.props;
    if (showing !== prevProps.showing) {
      this.setState({
        buyerDetails: {
          property_address: showing?.AuthorisationBlock.property_address,
          previous_hash: showing?.AuthorisationBlock.hash,
        },
      });
    }
  }

  handleOnSubmit(e) {
    e.preventDefault();
    const { onSubmit } = this.props;
    const { buyerDetails } = this.state;
    onSubmit(buyerDetails);
  }

  handleChange(e) {
    const buyerDetails = { ...this.state.buyerDetails };
    const target = e.target;
    buyerDetails[target.id] = target.value;
    this.setState({ buyerDetails });
  }

  render() {
    const {
      showing,
      handleClose,
    } = this.props;
    const {
      buyerDetails,
    } = this.state;

    return (
      <Dialog
        open={showing && true || false}
      >
        <DialogTitle>Please Enter Your Details</DialogTitle>
        <Box
          component="form"
          autoComplete="off"
          onSubmit={this.handleOnSubmit}
        >
          <DialogContent>
            <DialogContentText component="h3" variant="subtitle2">
              Personal Details
            </DialogContentText>

            <TextField
              id="full_name"
              label="Full Name"
              inputProps={{ maxLength: 256 }}
              onChange={this.handleChange}
              required
              fullWidth sx={{ ...textFieldStyle }}
            ></TextField>

            <TextField
              id="current_address"
              label="Current Address"
              inputProps={{ maxLength: 256 }}
              onChange={this.handleChange}
              required
              fullWidth sx={{ ...textFieldStyle }}
            ></TextField>

            <TextField
              id="dob"
              label="Date of Birth"
              onChange={this.handleChange}
              required
              sx={{ ...textFieldStyle, mr: 2 }}
              type="date"
              InputLabelProps={{shrink: true}}
            ></TextField>

            <TextField
              id="contact_number"
              label="Contact Number"
              inputProps={{ maxLength: 50 }}
              onChange={this.handleChange}
              required
              sx={{ ...textFieldStyle }}
            ></TextField>

            <DialogContentText component="h3" variant="subtitle2" sx={{mt: 3}}>
              Employment Details
            </DialogContentText>

            <TextField
              id="employer_name"
              label="Employer Name"
              inputProps={{ maxLength: 256 }}
              onChange={this.handleChange}
              required
              fullWidth sx={{ ...textFieldStyle }}
            ></TextField>

            {/* annual_income */}
            <TextField
              id="annual_income"
              label="Annual Income"
              InputProps={{
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
              }}
              onChange={this.handleChange}
              required
              sx={{ ...textFieldStyle }}
              type="number"
            ></TextField>

            <DialogContentText component="h3" variant="subtitle2" sx={{mt: 3}}>
              Purchase Details
            </DialogContentText>

            <TextField
              id="property_address"
              label="Property Address"
              inputProps={{ maxLength: 256 }}
              onChange={this.handleChange}
              InputProps={{
                readOnly: true,
                required: true,
              }}
              fullWidth sx={{ ...textFieldStyle }}
              defaultValue={buyerDetails.property_address}
            ></TextField>

            <TextField
              id="loan_amount"
              label="Loan Amount"
              InputProps={{
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
              }}
              onChange={this.handleChange}
              required
              sx={{ ...textFieldStyle }}
              type="number"
            ></TextField>

          </DialogContent>
          <DialogActions>
            <Button
              autoFocus
              onClick={handleClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
            >
              Submit
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    );
  }
}

BuyersApplicationForm.propTypes = {
  handleClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  propertyAddress: PropTypes.string,
};

export default BuyersApplicationForm;