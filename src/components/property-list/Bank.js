import React from "react";
import { Component } from "react";
import { Box, Container, TableContainer, Paper, Table, TableHead, TableRow, TableCell, TableBody, IconButton, Button } from "@mui/material";
import axios from "axios";
import { buildChain } from "../utils";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import moment from "moment";

const DEFAULT_STATE = {
  applications: [],
};

class Bank extends Component {
  constructor(props) {
    super(props);
    this.state = { ...DEFAULT_STATE };
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

  render() {
    const { applications } = this.state;

    return (
      
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
                    Property Wishing to Purchase
                  </TableCell>
                  <TableCell>
                    Borrower Annual Income
                  </TableCell>
                  <TableCell>
                    Requested Loan Amount
                  </TableCell>
                  <TableCell>
                    Permit Status
                  </TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {applications.map((a, i) => (
                  <TableRow
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
                    <TableCell>
                      {a.AuthorisationBlock.approval_status && 'Approved' || 'Not Approved'}
                    </TableCell>
                    <TableCell>
                      <Button>Verify…</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
    );
  }
}

export default Bank;