/**
=========================================================
* Soft UI Dashboard React - v4.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Grid from "@mui/material/Grid";
import Icon from "@mui/material/Icon";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";

// Soft UI Dashboard React examples
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
import ReportsBarChart from "examples/Charts/BarCharts/ReportsBarChart";
import GradientLineChart from "examples/Charts/LineCharts/GradientLineChart";


// Soft UI Dashboard React base styles
import typography from "assets/theme/base/typography";

// Dashboard layout components
import BuildByDevelopers from "layouts/dashboard2/components/BuildByDevelopers";
import WorkWithTheRockets from "layouts/dashboard2/components/WorkWithTheRockets";
import Projects from "layouts/dashboard2/components/Projects";
import OrderOverview from "layouts/dashboard2/components/OrderOverview";

// Data
import reportsBarChartData from "layouts/dashboard2/data/reportsBarChartData";
// import zuzycie from "layouts/dashboard2/data/zuzycie";
import napiecie from "layouts/dashboard2/data/napiecie";
import natezenie from "layouts/dashboard2/data/natezenie";
import { useEffect, useRef, useState } from "react";

import CustomDateRangeInputs from "examples/DatePickerCustom";
import DateRangePicker from 'rsuite/DateRangePicker';
import "rsuite/dist/rsuite.css"
import DatePicker from "examples/DatePickerCustom";
import SoftInput from "components/SoftInput";
import SoftButton from "components/SoftButton";
import { CheckPicker } from 'rsuite';



function Dashboard() {
  const { size } = typography;
  const { chart, items } = reportsBarChartData;
  const [counter, setCounter] = useState(" ");
  const options = {
    maxDate: new Date(),
    mode: 'range',
    altInputClass: 'hide',
    dateFormat: 'M d Y',
    minDate: new Date('01-01-2018'),

    // THIS `wrap` option is required when using external elements!
    // https://flatpickr.js.org/examples/#flatpickr-external-elements
    wrap: true,
  }

  const devices = ['Urządzenie 1', 'Urządzenie 2'].map(
    item => ({ label: item, value: item })
  );


  // useEffect(() => {
  //   fetch('http://127.0.0.1:5000/number', {
  //     method: 'GET',
  //   })
  //     .then(results => results.json())
  //     .then(number => setCounter(number))

  //   // const newCounter = 3;
  //   // setCounter(newCounter);


  // }, [])

  function arrayToDate(array) {
    var arrayDate = []
    for(let i = 0; i < array.length; i++) {
      var date = new Date(array[i]*1).toLocaleString();
      arrayDate.push(date);
    }
    return arrayDate
  }


  const [predictions, setPredictions] = useState(0);
  const [predictionsDate, setPredictionsDate] = useState(0);

  useEffect(() => {
    fetch('http://192.168.30.11:8080/api/frontend_req1', {
      method: 'POST',
    })
      .then(results => results.json())
      .then(number => setPredictions(number))

  }, [])

  const zuzycie = {
    labels: arrayToDate(Object.keys(predictions)),
    datasets: [
      {
        label: "Predykcja",
        color: "dark",
        data: Object.values(predictions),
      },
    ],
  };


  function generateChart(dateRange) {
    var now = new Date()
    var usageChartTime = {
      "devices": [value],
      "start": 1667322265.5519633, // Date.parse(dateRange[0]) + 86400000 - Date.parse(dateRange[0]) % 86400000 + now.getTimezoneOffset() * 60000,
      "end": 1667322285.5477865 // Date.parse(dateRange[1]) + 2 * 86400000 - Date.parse(dateRange[1]) % 86400000 + now.getTimezoneOffset() * 60000
    }
    console.log(usageChartTime);
    fetch('http://192.168.30.11:8080/api/frontend_req1', {
      method: 'POST',
      body: JSON.stringify(usageChartTime)
    })
      .then(results => results.json())
      .then(number => {
        console.log(number);
        setPredictions(number);
      })
  }


  const picker = useRef();
  const [value, setValue] = useState([]);

  const handleChange = value => {
    setValue(value);
    console.log(value);
  };

  const handleCheckAll = () => {
    setValue(['Urządzenie 1', 'Urządzenie 2']);
    console.log(value);
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SoftBox py={3}>
        <SoftBox alignItems="center" mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={2.1}>
              <DateRangePicker onChange={generateChart} size="lg" placeholder="Wybierz zakres..." style={{ width: 300 }} />
            </Grid>
            <Grid item xs={12} md={6}>
              <CheckPicker onLoad={handleCheckAll} onChange={handleChange} defaultValue={handleCheckAll} value={value} ref={picker} data={devices} size="lg" placeholder="Wybierz urządzenia..." searchable={false} style={{ width: 300 }} />
            </Grid>
          </Grid>
        </SoftBox>

        <SoftBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <GradientLineChart
                title="Ilość zużytego prądu"
                height="20.25rem"
                chart={zuzycie}
              />
            </Grid>
            <Grid item xs={12} md={8}>
              <GradientLineChart
                title="Napięcie prądu"
                height="20.25rem"
                chart={napiecie}
              />
            </Grid>
            <Grid item xs={12} md={8}>
              <GradientLineChart
                title="Natężenie prądu"
                height="20.25rem"
                chart={natezenie}
              />
            </Grid>
          </Grid>
        </SoftBox>
      </SoftBox>
    </DashboardLayout>
  );
}

export default Dashboard;
