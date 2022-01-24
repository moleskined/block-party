import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Step,
  StepLabel,
  Stepper,
  Alert,
  RadioGroup,
  Radio,
  FormControlLabel,
} from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";
import React from "react";
import { Component } from "react";

const DEFAULT_STATE = {
  property: null,
  activeStep: 0,
  showing: false,
  validationResult: null,
  formDetails: null,
};

const APPROVAL_STEPS = [
  'Validate Blockchain',
  'Approve or Reject Deal',
];

const textFieldStyle = { mt: 2 };

class CompleteDeal extends Component {
  constructor(props) {
    super(props);
    this.state = { ...DEFAULT_STATE };
    this.handleFormNextStep = this.handleFormNextStep.bind(this);
    this.validateBlock = this.validateBlock.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleCloseDialogue = this.handleCloseDialogue.bind(this);
  }

  handleFormNextStep(e) {
    e.preventDefault();
    const { activeStep, formDetails } = this.state;
    const { block, handleClose } = this.props;
    const b = { ...block?.BankApproval || {} };

    if (activeStep === APPROVAL_STEPS.length - 1) {
      // Clean up after window closes
      return handleClose({ block, formDetails }).then(() => new Promise(resolve => {
        setTimeout(() => {
          this.setState({ ...DEFAULT_STATE });
          resolve();
        }, 250);
      }));
    }

    this.setState({ activeStep: activeStep + 1 });
  }

  handleCloseDialogue() {
    const { handleClose } = this.props;
    // Clean up after window closes
    return handleClose().then(() => new Promise(resolve => {
      setTimeout(() => {
        this.setState({ ...DEFAULT_STATE });
        resolve();
      }, 250);
    }));
  }

  handleChange(e) {
    const formDetails = { ...this.state.formDetails };
    const target = e.target;
    const key = target.id || target.name;
    formDetails[key] = target.value;
    this.setState({ formDetails });
  }

  validateBlock(block) {
    const url = '/api/v2/check_block/bank_approval';
    const hash = block.hash;

    return axios.get(`${url}/${hash}`).then(response => {
      const { log, passed } = response.data;
      this.setState({ validationResult: { log, passed } })
    });
  }

  getDialogDetails(index) {
    const { block } = this.props;
    const { validationResult } = this.state;
    const color = validationResult?.passed ? 'lime' : 'red';
    const b = { ...block?.BankApproval || {} };

    if (index === 0) {
      return <>
        <DialogContentText gutterBottom>
          Before proceeding with finalisation, we need to validate the integrity of the Loan Application Status Block.
        </DialogContentText>
        <div style={{}}><pre style={{ padding: 4, color, fontSize: 'smaller', backgroundColor: '#000', height: '15rem', overflow: 'auto' }}>
          {validationResult?.log.map((l, i) => `${l}\n`)}
        </pre></div>
        <Button onClick={() => this.validateBlock(b)}>Validate…</Button>
      </>
    }

    return <>
      {validationResult?.passed && <Alert severity="success">Loan Application Status Block validated</Alert>}
      {validationResult?.passed === false && <Alert severity="error">Loan Application Status Block invalid</Alert>}
      <br />
      <Box style={{
        display: 'flex',
        justifyContent: 'center',
      }}>
        <RadioGroup
          row
          aria-label="Approve Deal"
          name="approved"
          onChange={this.handleChange}
        >
          <FormControlLabel labelPlacement="top" value="1" control={<Radio required={true} sx={{
            '& .MuiSvgIcon-root': {
              fontSize: 28,
            },
          }} />} label="Approve" />
          <FormControlLabel labelPlacement="top" value="0" control={<Radio required={true} sx={{
            '& .MuiSvgIcon-root': {
              fontSize: 28,
            },
          }} />} label="Reject" />
        </RadioGroup>
      </Box>
    </>
  }

  render() {
    const { showing } = this.props;
    const {
      activeStep,
      validationResult,
      formDetails,
    } = this.state;

    return <Dialog open={showing}>
      <DialogTitle>Finalise Deal</DialogTitle>
      <Box
        component="form"
        autoComplete="off"
        onSubmit={this.handleFormNextStep}
      >
        <DialogContent>
          <Stepper activeStep={activeStep}>
            {APPROVAL_STEPS.map(label => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
          <br />
          {this.getDialogDetails(activeStep)}
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={this.handleCloseDialogue}>
            Cancel
          </Button>
          <Button type="submit" disabled={!validationResult}>
            {activeStep < APPROVAL_STEPS.length - 1 ? 'Next' : 'Submit'}
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  }
}

export default CompleteDeal;