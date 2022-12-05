import React, { useRef, useState } from "react";
// import "./style.css";
import Flatpickr from 'react-flatpickr'
import 'flatpickr/dist/themes/material_blue.css'
import SoftInput from "components/SoftInput";
import SoftButton from "components/SoftButton";


function DatePicker() {
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

  // const [date, setDate] = useState(new Date());

  // const onChange = date => {
  //   setDate(date);
  // }

    return (
      <Flatpickr
      data-input
      options={options}
    >
      {/* Button and input should be the children of flatpickr * /}
      {/* as per the official flatpickr.js example above */}

      {/* toggle butotn should have `data-toggle` attribute */}
      <SoftButton data-toggle>Wybierz zakres</SoftButton>

      {/* input field should have `data-input` attribute */}
      <input type="text" placeholder="Select Date.."  data-input />
      <SoftInput placeholder="Select Date.." data-input/>
      
    </Flatpickr>
    );
  // }
}

// DatePicker.defaultProps = {
//   maxDate: new Date(),
//   mode: 'range',
//   altInputClass: 'hide',
//   dateFormat: 'M d Y',
//   minDate: new Date('01-01-2018'),
// };

// DatePicker.propTypes = {
//   maxDate: PropTypes.instanceOf(Date),
//   mode: propTypes.string,
//   altInputClass: propTypes.string,
//   dateFormat: propTypes.string,
//   minDate: PropTypes.instanceOf(Date),
// };


export default DatePicker;
