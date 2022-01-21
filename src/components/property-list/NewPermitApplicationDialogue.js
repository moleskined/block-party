import React from "react";
import PropTypes from 'prop-types';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  StepLabel,
  Stepper,
  Step,
  DialogContentText,
  TextField,
  ListItem,
  List,
  ListItemText,
} from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";

const PERMIT_APPLICATION_CREATION_STEPS = [
  'Enter Property Details',
  'Upload Building Design',
  'Confirm',
];

const DEFAULT_STATE = {
  activeStep: 0,
  formData: {},
};

class NewPermitApplicationDialogue extends React.Component {
  constructor(props) {
    super(props);
    const { handleNewPropertyClose } = props;
    const activeStep = 0;

    this.state = { ...DEFAULT_STATE };

    this.handleNewPropertyClose = handleNewPropertyClose.bind(this);
    this.handleFormNextStep = this.handleFormNextStep.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    const formData = { ...this.state.formData };
    const target = e.target;

    if (target.files) {
      formData[target.id] = target.files[0];
      this.setState({ formData });
      return;
    }

    formData[target.id] = target.value;
    this.setState({ formData });
  }

  getStep() {
    const { activeStep, formData } = this.state;
    const textFieldStyle = { mt: 2 };
    const contentTextStyle = {  };
    const accept = 'application/pdf';

    const steps = [
      <React.Fragment>
        <DialogContentText sx={{ ...contentTextStyle }} gutterBottom>
          Please enter the details of the property you with to sell:
        </DialogContentText>
        <TextField inputProps={{ maxLength: 256 }} onChange={this.handleChange} id="propertyAddress" label="Property Address" required fullWidth sx={{ ...textFieldStyle }}></TextField>
        <TextField inputProps={{ maxLength: 256 }} onChange={this.handleChange} id="sellerDetails" label="Owner/Vendor Details" required fullWidth sx={{ ...textFieldStyle }}></TextField>
        <TextField inputProps={{ maxLength: 23 }} onChange={this.handleChange} id="sellerLicenceNumber" label="Seller Licence Number" required sx={{ ...textFieldStyle }}></TextField>
      </React.Fragment>,

      <React.Fragment>
        <DialogContentText sx={{ ...contentTextStyle }} gutterBottom>
          Please upload a copy of the floor-plans (PDF format only):
        </DialogContentText>
        <Box>
          <Button
            variant="contained"
            component="label"
          >
            {formData.buildingDesign ? formData.buildingDesign.name : 'Upload File'}
            <div style={{ overflow: 'hidden', width: '1px', height: '1px' }}>
              <input
                accept={accept}
                type="file"
                required
                id="buildingDesign"
                onChange={this.handleChange}
              ></input>
            </div>
          </Button>
        </Box>
      </React.Fragment>,

      <React.Fragment>
        <DialogContentText sx={{ ...contentTextStyle }} gutterBottom>
          Please confirm the new permit application:
        </DialogContentText>
        <List>
          <ListItem>
            <ListItemText primary={'Property Address'} secondary={formData?.propertyAddress}></ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText primary={'Owner/Vendor Details'} secondary={formData?.sellerDetails}></ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText primary={'Seller Licence Number'} secondary={formData?.sellerLicenceNumber}></ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText primary={'Building Design'} secondary={formData?.buildingDesign?.name}></ListItemText>
          </ListItem>
        </List>
      </React.Fragment>
    ];
    return steps[activeStep];
  }

  handleFormNextStep(e) {
    e.preventDefault();
    const { activeStep, formData } = this.state;

    if (activeStep === PERMIT_APPLICATION_CREATION_STEPS.length - 1) {
      const {
        propertyAddress,
        sellerDetails,
        sellerLicenceNumber,
        buildingDesign,
      } = formData;

      const url = '/api/permit-application';
      const config = {
        headers: {
          'content-type': 'multipart/form-data',
        },
      };
      const f = new FormData();
      f.append('file', buildingDesign);
      f.append('fileName', buildingDesign.name);
      f.append('propertyAddress', propertyAddress);
      f.append('sellerDetails', sellerDetails);
      f.append('sellerLicenceNumber', sellerLicenceNumber);

      axios.post(url, f, config).then((response) => {
        return this.handleNewPropertyClose();
      });
    }

    this.setState({ activeStep: activeStep + 1 });
  }

  componentDidUpdate(prevProps) {
    const { showAddNewPropertyDialogue } = this.props;

    // Need to reset the modal on close. The timeout is there to prevent the modal resetting before transition fx finish
    if (showAddNewPropertyDialogue !== prevProps.showAddNewPropertyDialogue && !showAddNewPropertyDialogue) {
      setTimeout(() => {
        this.setState({ ...DEFAULT_STATE });
      }, 500);
    }
  }

  render() {
    const { showAddNewPropertyDialogue } = this.props;
    const { activeStep } = this.state;

    return (
      <Dialog
        open={showAddNewPropertyDialogue}
      >
        <DialogTitle>Create Permit Application</DialogTitle>
        <Box
          component="form"
          autoComplete="off"
          onSubmit={this.handleFormNextStep}
        >
          <DialogContent>
            <Stepper activeStep={activeStep}>
              {PERMIT_APPLICATION_CREATION_STEPS.map(label => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
            <br />
            {this.getStep()}
          </DialogContent>
          <DialogActions>
            <Button autoFocus onClick={this.handleNewPropertyClose}>
              Cancel
            </Button>
            <Button type="submit">
              { activeStep < PERMIT_APPLICATION_CREATION_STEPS.length - 1 ? 'Next' : 'Submit' }
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    );
  }
}

NewPermitApplicationDialogue.propTypes = {
  showAddNewPropertyDialogue: PropTypes.bool.isRequired,
  handleNewPropertyClose: PropTypes.func.isRequired,
  onSubmitProperty: PropTypes.func.isRequired,
};

export default NewPermitApplicationDialogue;