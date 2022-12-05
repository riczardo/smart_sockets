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
import zuzycie from "layouts/dashboard2/data/zuzycie";
import napiecie from "layouts/dashboard2/data/napiecie";
import natezenie from "layouts/dashboard2/data/natezenie";
import { useEffect, useRef, useState } from "react";

import CustomDateRangeInputs from "examples/DatePickerCustom";
import DateRangePicker from 'rsuite/DateRangePicker';
import "rsuite/dist/rsuite.css"
import DatePicker from "examples/DatePickerCustom";
import SoftInput from "components/SoftInput";
import Switch from "@mui/material/Switch";
import SoftButton from "components/SoftButton";



function Dashboard() {

  const [darkModeSwitchState, setdarkModeSwitchState] = useState(false);
  const [electricityPriceSwitchState, setelectricityPriceSwitchState] = useState(false);
  const [electricityPriceInputState, setelectricityPriceInputState] = useState(0);
  const [electricityUsageSwitchState, setelectricityUsageSwitchState] = useState(false);
  const [electricityUsageInputState, setelectricityUsageInputState] = useState(0);
  const [powerPriceInputState, setpowerPriceInputState] = useState(0);


  useEffect(() => {
    fetch('http://192.168.30.11:8080/get-settings', {
      method: 'GET',
    })
      .then(results =>results.json())
      .then(settings => {
        console.log(settings)
        setelectricityPriceInputState(settings['priceAlert']['value']);
        setelectricityPriceSwitchState(settings['priceAlert']['on']);
        setelectricityUsageInputState(settings['usageAlert']['value']);
        setelectricityUsageSwitchState(settings['usageAlert']['on']);
        setpowerPriceInputState(settings['electricityPrice'])
        setdarkModeSwitchState['darkMode'];
      })
  }, [])

  const usage_notify = useRef('');
  const price_notify = useRef('');
  const usage_switch = useRef('');
  const price_switch = useRef('');
  const darkmode_switch = useRef('');
  const power_price = useRef('');

  function saveSettings() {
    var settingsJSON = {
      "darkMode": darkmode_switch.current.firstChild.checked,
      "electricityPrice": parseFloat(power_price.current.firstChild.value),
      "priceAlert": 
        {
          "on": price_switch.current.firstChild.checked, 
          "value": parseFloat(price_notify.current.firstChild.value)
        },
      "usageAlert":
        {
          "on": usage_switch.current.firstChild.checked,
          "value": parseFloat(usage_notify.current.firstChild.value)
        }
      }
    console.log(settingsJSON);
    fetch('http://192.168.30.11:8080/set-settings', {
      method: 'POST',
      body: JSON.stringify(settingsJSON)
    })
  }


  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SoftBox py={3}>

        <SoftBox mb={3}>
          <Grid container spacing={3}>
            <Grid item hidden xs={12} md={8}>
              <Switch ref={darkmode_switch} checked={darkModeSwitchState} onChange={e => setdarkModeSwitchState(e.target.checked)}/>
              <SoftTypography
                variant="button"
                fontWeight="regular"
              >
                &nbsp;&nbsp;Dark Mode
              </SoftTypography>
            </Grid>
            <Grid item xs={12} md={8}>
              <Grid container spacing={3}>
                <Grid item xs={4} sm={4} xl={4}>
                  <Switch ref={price_switch} checked={electricityPriceSwitchState} onChange={e => setelectricityPriceSwitchState(e.target.checked)}/>
                  <SoftTypography
                    variant="button"
                    fontWeight="regular"
                  >
                    &nbsp;&nbsp;Powiadom, gdy cena prądu przekroczy
                  </SoftTypography>
                </Grid>
                <Grid item xs={2} sm={2} xl={2}>
                  <SoftInput ref={price_notify} placeholder="w zł" value={electricityPriceInputState} onChange={e => setelectricityPriceInputState(e.target.value)}/>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={8}>
              <Grid container spacing={3}>
                <Grid item xs={4} sm={4} xl={4}>
                  <Switch ref={usage_switch} checked={electricityUsageSwitchState} onChange={e => setelectricityUsageSwitchState(e.target.checked)}/>
                  <SoftTypography
                    variant="button"
                    fontWeight="regular"
                  // onClick={handleSetRememberMe}
                  // sx={{ cursor: "pointer", userSelect: "none" }}
                  >
                    &nbsp;&nbsp;Powiadom, gdy zużycie prądu przekroczy
                  </SoftTypography>
                </Grid>
                <Grid item xs={2} sm={2} xl={2}>
                  <SoftInput ref={usage_notify} placeholder="w kWh" value={electricityUsageInputState} onChange={e => setelectricityUsageInputState(e.target.value)}/>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={8}>
              <Grid container spacing={3}>
                <Grid item xs={4} sm={4} xl={4}>
                  <SoftTypography
                    variant="button"
                    fontWeight="regular"
                  // onClick={handleSetRememberMe}
                  // sx={{ cursor: "pointer", userSelect: "none" }}
                  >
                    Ustaw cenę prądu
                  </SoftTypography>
                </Grid>
                <Grid item xs={2} sm={2} xl={2}>
                  <SoftInput ref={power_price} placeholder="w zł (separator kropka)" value={powerPriceInputState} onChange={e => setpowerPriceInputState(e.target.value)}/>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} md={8}>
              <SoftButton onClick={saveSettings} variant="gradient" color="info" size="large" >Zapisz</SoftButton>
            </Grid>
          </Grid>
        </SoftBox>
      </SoftBox>
    </DashboardLayout>
  );
}

export default Dashboard;
