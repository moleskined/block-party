import React from "react";
import { Component } from "react";
import {
  Box, Container, TableContainer, Paper, Table, TableHead, TableRow, TableCell, TableBody,
  IconButton, Button, Dialog, DialogTitle, DialogContent, DialogActions, DialogContentText, Stepper, Step, StepLabel,
  List,
  ListItem,
  ListItemText,
  TextField,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Divider,
} from "@mui/material";
import axios from "axios";
import { buildChain } from "../utils";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import moment from "moment";
import Alert from '@mui/material/Alert';

const DEFAULT_STATE = {
  applications: [],
  application: null,
  activeStep: 0,
  showing: false,
  validationResult: null,
  formDetails: null,
};

const APPROVAL_STEPS = [
  'Validate Blockchain',
  'Approve or Reject Loan',
];

const textFieldStyle = { mt: 2 };

class Bank extends Component {
  constructor(props) {
    super(props);
    this.state = { ...DEFAULT_STATE };
    this.handleFormNextStep = this.handleFormNextStep.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.validateBlock = this.validateBlock.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    this.loadProps();
  }

  loadProps() {
    const url = '/api/v2/loan_applications';
    axios.get(url).then(response => {
      const data = [...response.data];
      const applications = data.map(d => buildChain(d))
      this.setState({ applications })
    })
  }

  handleFormNextStep(e) {
    e.preventDefault();
    const { activeStep, formDetails, application } = this.state;
    const block = application.BuyerBlock;

    if (activeStep === APPROVAL_STEPS.length - 1) {
      return axios.put(`/api/v2/loan_applications/${block.hash}`, formDetails)
        .then(response => console.log(response.data))
        .finally(this.handleClose());
    }

    this.setState({ activeStep: activeStep + 1 });
  }

  handleClose() {
    this.setState({
      showing: false,
    });

    this.loadProps();

    setTimeout(() => {
      this.setState({
        application: null,
        activeStep: 0,
        validationResult: null,
        formDetails: null,
      });
    }, 250);
  }

  handleChange(e) {
    const formDetails = { ...this.state.formDetails };
    const target = e.target;
    const key = target.id || target.name;
    formDetails[key] = target.value;
    this.setState({ formDetails });
  }

  validateBlock(block) {
    const url = '/api/v2/check_block/authority';
    const hash = block.hash;

    return axios.get(`${url}/${hash}`).then(response => {
      const { log, passed } = response.data;
      this.setState({ validationResult: { log, passed } })
    });
  }

  getDialogDetails(index) {
    const { application, validationResult } = this.state;
    const block = { ...application?.AuthorisationBlock || {} };
    const color = validationResult?.passed ? 'lime' : 'red';
    const components = [
      <>
        <DialogContentText gutterBottom>
          Before proceeding with approval, we need to validate the integrity of the Authority Block.
        </DialogContentText>
        <div style={{}}><pre style={{ padding: 4, color, fontSize: 'smaller', backgroundColor: '#000', height: '15rem', overflow: 'auto' }}>
          {validationResult?.log.map((l, i) => `${l}\n`)}
        </pre></div>
        <Button onClick={() => this.validateBlock(block)}>Validate…</Button>
      </>,
      <>
        {validationResult?.passed && <Alert severity="success">Authority block validated</Alert>}
        {validationResult?.passed === false && <Alert severity="error">Authority block invalid</Alert>}

        <TextField
          id="full_name"
          label="Full Name"
          inputProps={{ maxLength: 256 }}
          onChange={this.handleChange}
          InputProps={{
            readOnly: false,
            required: true,
          }}
          fullWidth sx={{ ...textFieldStyle }}
          defaultValue={application?.BuyerBlock.full_name}
        ></TextField>
        <TextField
          id="current_address"
          label="Current Address"
          inputProps={{ maxLength: 256 }}
          onChange={this.handleChange}
          InputProps={{
            readOnly: false,
            required: true,
          }}
          fullWidth sx={{ ...textFieldStyle }}
          defaultValue={application?.BuyerBlock.current_address}
        ></TextField>
        <TextField
          id="contact_number"
          label="Contact Number"
          inputProps={{ maxLength: 50 }}
          onChange={this.handleChange}
          InputProps={{
            readOnly: false,
            required: true,
          }}
          sx={{ ...textFieldStyle, mr: 2, mb: 4 }}
          defaultValue={application?.BuyerBlock.contact_number}
        ></TextField>
        <TextField
          id="dob"
          label="Date of Birth"
          onChange={this.handleChange}
          InputProps={{
            readOnly: false,
            required: true,
          }}
          sx={{ ...textFieldStyle, mr: 2, mb: 4 }}
          type="date"
          InputLabelProps={{ shrink: true }}
          defaultValue={moment(application?.BuyerBlock.dob).format('YYYY-MM-DD')}
        ></TextField>

        <Box style={{
          display: 'flex',
          justifyContent: 'center',
        }}>
          <RadioGroup
            row
            aria-label="Approve Loan"
            name="approval_status"
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
      </>,
    ];
    return components[index];
  }

  render() {
    const {
      applications,
      application,
      activeStep,
      showing,
      validationResult,
    } = this.state;

    return (
      <>
        <Dialog open={showing}>
          <DialogTitle>Approve Loan Application</DialogTitle>
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
              <Button autoFocus onClick={this.handleClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={!validationResult}>
                {activeStep < APPROVAL_STEPS.length - 1 ? 'Next' : 'Submit'}
              </Button>
            </DialogActions>
          </Box>
        </Dialog>

        <Box sx={{ my: 2, mx: 2 }}>
          <TableContainer component={Paper}>
            <Table aria-label="Loan applications">
              <TableHead>
                <TableRow>
                  <TableCell>
                    Date
                  </TableCell>
                  <TableCell>
                    Borrower
                  </TableCell>
                  <TableCell>
                    Current Address
                  </TableCell>
                  <TableCell>
                    Contact #
                  </TableCell>
                  <TableCell>
                    DoB
                  </TableCell>
                  <TableCell>
                    Purchasing
                  </TableCell>
                  <TableCell>
                    Loan
                  </TableCell>
                  <TableCell>
                    Income
                  </TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {applications.map((a, i) => {
                  const bankApproval = a['BankApproval'];

                  return <TableRow
                    key={i}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell>{moment(a['BuyerBlock'].timestamp).format('L')}</TableCell>
                    <TableCell>{a['BuyerBlock'].full_name}</TableCell>
                    <TableCell>{a['BuyerBlock'].current_address}</TableCell>
                    <TableCell>{a['BuyerBlock'].contact_number}</TableCell>
                    <TableCell>{moment(a['BuyerBlock'].dob).format('L')}</TableCell>
                    <TableCell>{a['BuyerBlock'].property_address}</TableCell>
                    <TableCell>{new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' }).format(a['BuyerBlock'].loan_amount)}</TableCell>
                    <TableCell>{new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' }).format(a['BuyerBlock'].annual_income)}</TableCell>
                    {!bankApproval && <>
                      <TableCell>
                        <Button onClick={() => this.setState({
                          application: a, showing: true, validationResult: null, formDetails: {
                            full_name: a['BuyerBlock'].full_name,
                            current_address: a['BuyerBlock'].current_address,
                            contact_number: a['BuyerBlock'].contact_number,
                            dob: moment(a['BuyerBlock'].dob).format('YYYY-MM-DD'),
                          }
                        })}>Verify…</Button>
                      </TableCell>
                    </>}
                    {bankApproval && <>
                      <TableCell>
                        { bankApproval.approval_status ? 'Approved' : 'Rejected' }
                      </TableCell>
                    </>}
                  </TableRow>
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </>
    );
  }
}

export default Bank;