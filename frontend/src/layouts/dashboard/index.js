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
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import SoftButton from "components/SoftButton";
import SoftInput from "components/SoftInput";

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
import BuildByDevelopers from "layouts/dashboard/components/BuildByDevelopers";
import WorkWithTheRockets from "layouts/dashboard/components/WorkWithTheRockets";
import Projects from "layouts/dashboard/components/Projects";
import OrderOverview from "layouts/dashboard/components/OrderOverview";

// Data
import reportsBarChartData from "layouts/dashboard/data/reportsBarChartData";
import gradientLineChartData from "layouts/dashboard/data/gradientLineChartData";
import { useEffect, useState } from "react";
import Select from 'react-select'
import { SelectPicker } from 'rsuite';

function Dashboard() {
  const { size } = typography;
  const { chart, items } = reportsBarChartData;
  const [counter, setCounter] = useState(" ");
  const options = [
    { value: 'day', label: 'Dzień' },
    { value: 'week', label: 'Tydzień' },
    { value: 'month', label: 'Miesiąc' },
    { value: 'year', label: 'Rok' }
  ]

  useEffect(() => {
    fetch('http://192.168.30.11:8080/number', {
      method: 'POST',
      body: JSON.stringify({"span": "month"})
    })
      .then(results => results.json())
      .then(number => setCounter(number))
  }, [])

  function reload(selectPicker) {
    fetch('http://192.168.30.11:8080/number', {
      method: 'POST',
      body: JSON.stringify(selectPicker === null ? {"span": "month"} : {"span": selectPicker})
    })
      .then(results => results.json())
      .then(number => setCounter(number))
    console.log(selectPicker);
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SoftBox py={3}>
        <SoftBox alignItems="center" mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} xl={3}>
              <SelectPicker defaultValue='month' data={options} onChange={reload} size="lg" label="Okres" placeholder="Wybierz okres..." searchable={false} style={{ width: 300 }} />
            </Grid>
          </Grid>
        </SoftBox>
        <SoftBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Cena zużytego prądu" }}
                count={`${counter["usedPrice"]} zł`}
                icon={{ color: "info", component: "paid" }}
              />
            </Grid>
            <Grid item xs={12} sm={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Predykcja ceny miesięcznej" }}
                count={`${counter["monthlyPrediction"]} zł`}
                icon={{ color: "info", component: "paid" }}
              />
            </Grid>
            <Grid item xs={12} sm={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "Ilość zużytego prądu" }}
                count={`${counter["usedAmount"]} kWh`}
                icon={{
                  color: "info",
                  component: "paid",
                }}
              />
            </Grid>
          </Grid>
        </SoftBox>
      </SoftBox>
      {/* <Footer /> */}
    </DashboardLayout>
  );
}

export default Dashboard;
