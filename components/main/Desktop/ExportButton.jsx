import React, { useContext } from 'react';
import Button from '@mui/material/Button';
import PropTypes from 'proptypes';
import { connect } from 'react-redux';
import JSZip from 'jszip';
import Papa from 'papaparse';
import { saveAs } from 'file-saver';
import DbContext from '@db/DbContext';
import ddbh from '@utils/duckDbHelpers.js';
import { isEmpty } from '@utils';
import requestTypes from '../../../data/requestTypes';

// export button main function
function ExportButton({ filters }) {
  const { conn } = useContext(DbContext);

  // creation zip file
  const downloadZip = async csvContent => {
    const zip = new JSZip();
    zip.file('NeighborhoodData.csv', csvContent);

    const content = await zip.generateAsync({ type: 'blob' });
    saveAs(content, '311Data.zip');
  };

  // data to add into zip file, queries then add results
  const getDataToExport = async () => {
    // define request status filter variable to reuse variable
    let requestStatusFilter = '';

    if (filters.requestStatus.open === true && filters.requestStatus.closed === false) {
      // Only open is true, get all open requests
      // query = `SELECT * FROM requests WHERE Status='Open';`;
      requestStatusFilter = 'Open';
    } else if (filters.requestStatus.closed === true && filters.requestStatus.open === false) {
      // Only closed is true, get all closed requests
      // query = `SELECT * FROM requests WHERE Status='Closed';`;
      requestStatusFilter = 'Closed';
    }

    const formattedRequestTypes = requestTypes
      .filter(item => filters.requestTypes[item.typeId])
      .map(v => `'${v.typeName}'`)
      .join(', ');

    // // in the case user chooses one neighborhood or all are selected + dates and status
    const query = `select * from requests where CreatedDate >= '${filters.startDate}' AND
    CreatedDate < '${filters.endDate}'${requestStatusFilter !== ''
      ? ` AND Status='${requestStatusFilter}'` : ''}
    ${filters.councilId !== null
        ? ` AND NC='${filters.councilId}'` : ''} AND RequestType IN (${formattedRequestTypes});`;

    const dataToExport = await conn.query(query);
    const results = ddbh.getTableData(dataToExport);

    if (!isEmpty(results)) {
      // results chosen to csv
      const csvContent = Papa.unparse(results);
      downloadZip(csvContent);
    } else {
      window.alert('No 311 data available within the selected filters. Please adjust your filters and try again.');
    }
  };

  // action upon clicking
  const handleExport = () => {
    getDataToExport(filters);
  };

  return (
    <Button variant="contained" onClick={handleExport}>
      Export
    </Button>

  );
}

const mapStateToProps = state => ({
  filters: state.filters,
});

export default connect(mapStateToProps)(ExportButton);

ExportButton.propTypes = {
  filters: PropTypes.shape({
    startDate: PropTypes.string,
    endDate: PropTypes.string,
    councilId: PropTypes.number,
    requestStatus: PropTypes.shape({
      open: PropTypes.bool,
      closed: PropTypes.bool,
    }),
    requestTypes: PropTypes.objectOf(PropTypes.bool),
  }).isRequired,
};
