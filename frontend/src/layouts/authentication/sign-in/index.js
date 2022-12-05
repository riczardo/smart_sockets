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

import { useState, useRef } from "react";

// react-router-dom components
import { Link, useNavigate } from "react-router-dom";

// @mui material components
import Switch from "@mui/material/Switch";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import SoftInput from "components/SoftInput";
import SoftButton from "components/SoftButton";

// Authentication layout components
import CoverLayout from "layouts/authentication/components/CoverLayout";

// Images
import curved9 from "assets/images/login1.jpg";

function SignIn() {
  const [rememberMe, setRememberMe] = useState(true);

  const handleSetRememberMe = () => setRememberMe(!rememberMe);

  const redirect = useNavigate();


  // const [passwordState, setpasswordState] = useState(false);
  // const [usernameState, setusernameState] = useState(0);
  // const [emailState, setemailState] = useState(0);

  const username = useRef('');
  const password = useRef('');


  function sendCredentials() {
    fetch('http://127.0.0.1:5000/sign-in', {
      method: 'POST',
      body: JSON.stringify({"username": username.current.firstChild.value, "password": password.current.firstChild.value})
    }).then(results => results.json())
    .then(login => {
      if (login === true) {
        redirect("/podsumowanie");
      } else {
        redirect("/authentication/sign-up");
        redirect("/authentication/sign-in");
      }
    })
  }

  return (
    <CoverLayout
      title="Zaloguj"
      description="Wpisz nazwę użytkownika i hasło"
      image={curved9}
    >
      <SoftBox component="form" role="form">
        <SoftBox mb={2}>
          <SoftBox mb={1} ml={0.5}>
            <SoftTypography component="label" variant="caption" fontWeight="bold">
              Login
            </SoftTypography>
          </SoftBox>
          <SoftInput ref={username} type="login" placeholder="Login" />
        </SoftBox>
        <SoftBox mb={2}>
          <SoftBox mb={1} ml={0.5}>
            <SoftTypography component="label" variant="caption" fontWeight="bold">
              Hasło
            </SoftTypography>
          </SoftBox>
          <SoftInput ref={password} type="password" placeholder="Hasło" />
        </SoftBox>
        <SoftBox mt={4} mb={1}>
          <SoftButton onClick={sendCredentials} variant="gradient" color="info" fullWidth>
            zaloguj
          </SoftButton>
        </SoftBox>
        <SoftBox mt={3} textAlign="center">
          <SoftTypography variant="button" color="text" fontWeight="regular">
            Nie masz konta?{" "}
            <SoftTypography
              component={Link}
              to="/authentication/sign-up"
              variant="button"
              color="info"
              fontWeight="medium"
              textGradient
            >
              Zarejestruj się
            </SoftTypography>
          </SoftTypography>
        </SoftBox>
      </SoftBox>
    </CoverLayout>
  );
}

export default SignIn;
