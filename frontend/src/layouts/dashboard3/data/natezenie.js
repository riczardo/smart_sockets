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
// const [counter1, setCounter1] = useState("1000");

// useEffect(() => {
//   fetch('http://127.0.0.1:5000/number', {
//       method: 'GET',
//   })
//   .then(results => results.json())
//   .then(number => setCounter1(number))

//   const newCounter1 = 3;
//   setCounter1(newCounter1);


// }, [])


const natezenie = {
  labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  datasets: [
    {
      label: "Mobile apps",
      color: "info",
      data: [123, 123, 300, 332, 545, 250, 222, 230, 500],
    },
    {
      label: "Websites",
      color: "dark",
      data: [30, 90, 40, 232, 290, 290, 234, 230, 673],
    },
  ],
};

export default natezenie;
