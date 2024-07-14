// import React, { useState } from "react";
// import {
//   Container,
//   TextField,
//   Button,
//   Table,
//   TableBody,
//   TableCell,
//   TableContainer,
//   TableHead,
//   TableRow,
//   Paper,
//   Typography,
//   Box,
//   Stack,
// } from "@mui/material";
// import { TimePicker } from "@mui/x-date-pickers/TimePicker";
// import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
// import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";

// function App() {
//   const [cityUsers, setCityUsers] = useState([
//     { cityName: "", numOfUsers: "" },
//   ]);
//   const [cityTraffic, setCityTraffic] = useState([
//     { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
//   ]);
//   const [timeRangeTraffic, setTimeRangeTraffic] = useState([
//     {
//       startTime: null,
//       endTime: null,
//       city1: "",
//       city2: "",
//       uploadPeak: "",
//       downloadPeak: "",
//     },
//   ]);

//   const handleCityUsersChange = (index, field, value) => {
//     const newCityUsers = [...cityUsers];
//     newCityUsers[index][field] = value;
//     setCityUsers(newCityUsers);
//   };

//   const handleCityTrafficChange = (index, field, value) => {
//     const newCityTraffic = [...cityTraffic];
//     newCityTraffic[index][field] = value;
//     setCityTraffic(newCityTraffic);
//   };

//   const handleTimeRangeTrafficChange = (index, field, value) => {
//     const newTimeRangeTraffic = [...timeRangeTraffic];
//     newTimeRangeTraffic[index][field] = value;
//     setTimeRangeTraffic(newTimeRangeTraffic);
//   };

//   const addCityUserRow = () =>
//     setCityUsers([...cityUsers, { cityName: "", numOfUsers: "" }]);
//   const deleteCityUserRow = () => setCityUsers(cityUsers.slice(0, -1));

//   const addCityTrafficRow = () =>
//     setCityTraffic([
//       ...cityTraffic,
//       { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
//     ]);
//   const deleteCityTrafficRow = () => setCityTraffic(cityTraffic.slice(0, -1));

//   const addTimeRangeTrafficRow = () =>
//     setTimeRangeTraffic([
//       ...timeRangeTraffic,
//       {
//         startTime: null,
//         endTime: null,
//         city1: "",
//         city2: "",
//         uploadPeak: "",
//         downloadPeak: "",
//       },
//     ]);
//   const deleteTimeRangeTrafficRow = () =>
//     setTimeRangeTraffic(timeRangeTraffic.slice(0, -1));

//   const handleSubmit = () => {
//     const cityUsersData = cityUsers.map((row) => ({
//       cityName: row.cityName,
//       numOfUsers: row.numOfUsers,
//     }));
//     const cityTrafficData = cityTraffic.map((row) => ({
//       city1: row.city1,
//       city2: row.city2,
//       uploadPeak: row.uploadPeak,
//       downloadPeak: row.downloadPeak,
//     }));
//     const timeRangeTrafficData = timeRangeTraffic.map((row) => ({
//       startTime: row.startTime ? row.startTime.toISOString() : null,
//       endTime: row.endTime ? row.endTime.toISOString() : null,
//       city1: row.city1,
//       city2: row.city2,
//       uploadPeak: row.uploadPeak,
//       downloadPeak: row.downloadPeak,
//     }));

//     const formData = {
//       cityUsers: cityUsersData,
//       cityTraffic: cityTrafficData,
//       timeRangeTraffic: timeRangeTrafficData,
//     };

//     console.log(formData);

//     fetch("http://127.0.0.1:5000/submit", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(formData),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         console.log("Success:", data);
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//       });

//     // setCityUsers([{ cityName: "", numOfUsers: "" }]);
//     // setCityTraffic([
//     //   { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
//     // ]);
//     // setTimeRangeTraffic([
//     //   {
//     //     startTime: null,
//     //     endTime: null,
//     //     city1: "",
//     //     city2: "",
//     //     uploadPeak: "",
//     //     downloadPeak: "",
//     //   },
//     // ]);
//   };

//   return (
//     <LocalizationProvider dateAdapter={AdapterDateFns}>
//       <Container>
//         <Typography variant="h4" gutterBottom>
//           City Users
//         </Typography>
//         <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
//           <Table>
//             <TableHead>
//               <TableRow>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   City
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Number of Users
//                 </TableCell>
//               </TableRow>
//             </TableHead>
//             <TableBody>
//               {cityUsers.map((row, index) => (
//                 <TableRow key={index}>
//                   <TableCell>
//                     <TextField
//                       value={row.cityName}
//                       onChange={(e) =>
//                         handleCityUsersChange(index, "cityName", e.target.value)
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       type="number"
//                       value={row.numOfUsers}
//                       onChange={(e) =>
//                         handleCityUsersChange(
//                           index,
//                           "numOfUsers",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                 </TableRow>
//               ))}
//             </TableBody>
//           </Table>
//         </TableContainer>
//         <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
//           <Button
//             variant="contained"
//             color="primary"
//             onClick={addCityUserRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Add Row
//           </Button>
//           <Button
//             variant="outlined"
//             color="secondary"
//             onClick={deleteCityUserRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Delete Last Row
//           </Button>
//         </Stack>

//         <Typography variant="h4" gutterBottom>
//           City Traffic
//         </Typography>
//         <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
//           <Table>
//             <TableHead>
//               <TableRow>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   City 1
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   City 2
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Upload Peak
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Download Peak
//                 </TableCell>
//               </TableRow>
//             </TableHead>
//             <TableBody>
//               {cityTraffic.map((row, index) => (
//                 <TableRow key={index}>
//                   <TableCell>
//                     <TextField
//                       value={row.city1}
//                       onChange={(e) =>
//                         handleCityTrafficChange(index, "city1", e.target.value)
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       value={row.city2}
//                       onChange={(e) =>
//                         handleCityTrafficChange(index, "city2", e.target.value)
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       type="number"
//                       value={row.uploadPeak}
//                       onChange={(e) =>
//                         handleCityTrafficChange(
//                           index,
//                           "uploadPeak",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       type="number"
//                       value={row.downloadPeak}
//                       onChange={(e) =>
//                         handleCityTrafficChange(
//                           index,
//                           "downloadPeak",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                 </TableRow>
//               ))}
//             </TableBody>
//           </Table>
//         </TableContainer>
//         <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
//           <Button
//             variant="contained"
//             color="primary"
//             onClick={addCityTrafficRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Add Row
//           </Button>
//           <Button
//             variant="outlined"
//             color="secondary"
//             onClick={deleteCityTrafficRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Delete Last Row
//           </Button>
//         </Stack>

//         <Typography variant="h4" gutterBottom>
//           Time Range Traffic
//         </Typography>
//         <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
//           <Table>
//             <TableHead>
//               <TableRow>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Start Time
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   End Time
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   City 1
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   City 2
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Upload Peak
//                 </TableCell>
//                 <TableCell
//                   align="center"
//                   sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
//                 >
//                   Download Peak
//                 </TableCell>
//               </TableRow>
//             </TableHead>
//             <TableBody>
//               {timeRangeTraffic.map((row, index) => (
//                 <TableRow key={index}>
//                   <TableCell>
//                     <TimePicker
//                       value={row.startTime}
//                       onChange={(value) =>
//                         handleTimeRangeTrafficChange(index, "startTime", value)
//                       }
//                       renderInput={(params) => (
//                         <TextField {...params} fullWidth variant="outlined" />
//                       )}
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TimePicker
//                       value={row.endTime}
//                       onChange={(value) =>
//                         handleTimeRangeTrafficChange(index, "endTime", value)
//                       }
//                       renderInput={(params) => (
//                         <TextField {...params} fullWidth variant="outlined" />
//                       )}
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       value={row.city1}
//                       onChange={(e) =>
//                         handleTimeRangeTrafficChange(
//                           index,
//                           "city1",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       value={row.city2}
//                       onChange={(e) =>
//                         handleTimeRangeTrafficChange(
//                           index,
//                           "city2",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       type="number"
//                       value={row.uploadPeak}
//                       onChange={(e) =>
//                         handleTimeRangeTrafficChange(
//                           index,
//                           "uploadPeak",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                   <TableCell>
//                     <TextField
//                       type="number"
//                       value={row.downloadPeak}
//                       onChange={(e) =>
//                         handleTimeRangeTrafficChange(
//                           index,
//                           "downloadPeak",
//                           e.target.value
//                         )
//                       }
//                       fullWidth
//                       variant="outlined"
//                     />
//                   </TableCell>
//                 </TableRow>
//               ))}
//             </TableBody>
//           </Table>
//         </TableContainer>
//         <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
//           <Button
//             variant="contained"
//             color="primary"
//             onClick={addTimeRangeTrafficRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Add Row
//           </Button>
//           <Button
//             variant="outlined"
//             color="secondary"
//             onClick={deleteTimeRangeTrafficRow}
//             sx={{ marginBottom: 4 }}
//           >
//             Delete Last Row
//           </Button>
//         </Stack>

//         <Box textAlign="center" mt={4}>
//           <Button variant="contained" color="primary" onClick={handleSubmit}>
//             Submit
//           </Button>
//         </Box>
//       </Container>
//     </LocalizationProvider>
//   );
// }

// export default App;

import React, { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Stack,
} from "@mui/material";
import { TimePicker } from "@mui/x-date-pickers/TimePicker";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";

function App() {
  const [cityUsers, setCityUsers] = useState([
    { cityName: "", numOfUsers: "" },
  ]);
  const [cityTraffic, setCityTraffic] = useState([
    { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
  ]);
  const [timeRangeTraffic, setTimeRangeTraffic] = useState([
    {
      startTime: null,
      endTime: null,
      city1: "",
      city2: "",
      uploadPeak: "",
      downloadPeak: "",
    },
  ]);
  const [networkGraph, setNetworkGraph] = useState(null); // State to store the base64 string

  const handleCityUsersChange = (index, field, value) => {
    const newCityUsers = [...cityUsers];
    newCityUsers[index][field] = value;
    setCityUsers(newCityUsers);
  };

  const handleCityTrafficChange = (index, field, value) => {
    const newCityTraffic = [...cityTraffic];
    newCityTraffic[index][field] = value;
    setCityTraffic(newCityTraffic);
  };

  const handleTimeRangeTrafficChange = (index, field, value) => {
    const newTimeRangeTraffic = [...timeRangeTraffic];
    newTimeRangeTraffic[index][field] = value;
    setTimeRangeTraffic(newTimeRangeTraffic);
  };

  const addCityUserRow = () =>
    setCityUsers([...cityUsers, { cityName: "", numOfUsers: "" }]);
  const deleteCityUserRow = () => setCityUsers(cityUsers.slice(0, -1));

  const addCityTrafficRow = () =>
    setCityTraffic([
      ...cityTraffic,
      { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
    ]);
  const deleteCityTrafficRow = () => setCityTraffic(cityTraffic.slice(0, -1));

  const addTimeRangeTrafficRow = () =>
    setTimeRangeTraffic([
      ...timeRangeTraffic,
      {
        startTime: null,
        endTime: null,
        city1: "",
        city2: "",
        uploadPeak: "",
        downloadPeak: "",
      },
    ]);
  const deleteTimeRangeTrafficRow = () =>
    setTimeRangeTraffic(timeRangeTraffic.slice(0, -1));

  const handleSubmit = () => {
    const cityUsersData = cityUsers.map((row) => ({
      cityName: row.cityName,
      numOfUsers: row.numOfUsers,
    }));
    const cityTrafficData = cityTraffic.map((row) => ({
      city1: row.city1,
      city2: row.city2,
      uploadPeak: row.uploadPeak,
      downloadPeak: row.downloadPeak,
    }));
    const timeRangeTrafficData = timeRangeTraffic.map((row) => ({
      startTime: row.startTime ? row.startTime.toISOString() : null,
      endTime: row.endTime ? row.endTime.toISOString() : null,
      city1: row.city1,
      city2: row.city2,
      uploadPeak: row.uploadPeak,
      downloadPeak: row.downloadPeak,
    }));

    const formData = {
      cityUsers: cityUsersData,
      cityTraffic: cityTrafficData,
      timeRangeTraffic: timeRangeTrafficData,
    };

    console.log(formData);

    fetch("http://127.0.0.1:5000/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setNetworkGraph(data.network_graph); // Set the base64 string to state
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    // setCityUsers([{ cityName: "", numOfUsers: "" }]);
    // setCityTraffic([
    //   { city1: "", city2: "", uploadPeak: "", downloadPeak: "" },
    // ]);
    // setTimeRangeTraffic([
    //   {
    //     startTime: null,
    //     endTime: null,
    //     city1: "",
    //     city2: "",
    //     uploadPeak: "",
    //     downloadPeak: "",
    //   },
    // ]);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Container>
        <Typography variant="h4" gutterBottom>
          City Users
        </Typography>
        <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  City
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Number of Users
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cityUsers.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <TextField
                      value={row.cityName}
                      onChange={(e) =>
                        handleCityUsersChange(index, "cityName", e.target.value)
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={row.numOfUsers}
                      onChange={(e) =>
                        handleCityUsersChange(
                          index,
                          "numOfUsers",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
          <Button
            variant="contained"
            color="primary"
            onClick={addCityUserRow}
            sx={{ marginBottom: 4 }}
          >
            Add Row
          </Button>
          <Button
            variant="outlined"
            color="secondary"
            onClick={deleteCityUserRow}
            sx={{ marginBottom: 4 }}
          >
            Delete Last Row
          </Button>
        </Stack>

        <Typography variant="h4" gutterBottom>
          City Traffic
        </Typography>
        <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  City 1
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  City 2
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Upload Peak
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Download Peak
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cityTraffic.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <TextField
                      value={row.city1}
                      onChange={(e) =>
                        handleCityTrafficChange(index, "city1", e.target.value)
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      value={row.city2}
                      onChange={(e) =>
                        handleCityTrafficChange(index, "city2", e.target.value)
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={row.uploadPeak}
                      onChange={(e) =>
                        handleCityTrafficChange(
                          index,
                          "uploadPeak",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={row.downloadPeak}
                      onChange={(e) =>
                        handleCityTrafficChange(
                          index,
                          "downloadPeak",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
          <Button
            variant="contained"
            color="primary"
            onClick={addCityTrafficRow}
            sx={{ marginBottom: 4 }}
          >
            Add Row
          </Button>
          <Button
            variant="outlined"
            color="secondary"
            onClick={deleteCityTrafficRow}
            sx={{ marginBottom: 4 }}
          >
            Delete Last Row
          </Button>
        </Stack>

        <Typography variant="h4" gutterBottom>
          Time Range Traffic
        </Typography>
        <TableContainer component={Paper} sx={{ marginBottom: 4 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Start Time
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  End Time
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  City 1
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  City 2
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Upload Peak
                </TableCell>
                <TableCell
                  align="center"
                  sx={{ fontWeight: "bold", fontSize: "1.2rem" }}
                >
                  Download Peak
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {timeRangeTraffic.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <TimePicker
                      value={row.startTime}
                      onChange={(value) =>
                        handleTimeRangeTrafficChange(index, "startTime", value)
                      }
                      renderInput={(params) => (
                        <TextField {...params} fullWidth variant="outlined" />
                      )}
                    />
                  </TableCell>
                  <TableCell>
                    <TimePicker
                      value={row.endTime}
                      onChange={(value) =>
                        handleTimeRangeTrafficChange(index, "endTime", value)
                      }
                      renderInput={(params) => (
                        <TextField {...params} fullWidth variant="outlined" />
                      )}
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      value={row.city1}
                      onChange={(e) =>
                        handleTimeRangeTrafficChange(
                          index,
                          "city1",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      value={row.city2}
                      onChange={(e) =>
                        handleTimeRangeTrafficChange(
                          index,
                          "city2",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={row.uploadPeak}
                      onChange={(e) =>
                        handleTimeRangeTrafficChange(
                          index,
                          "uploadPeak",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      type="number"
                      value={row.downloadPeak}
                      onChange={(e) =>
                        handleTimeRangeTrafficChange(
                          index,
                          "downloadPeak",
                          e.target.value
                        )
                      }
                      fullWidth
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
          <Button
            variant="contained"
            color="primary"
            onClick={addTimeRangeTrafficRow}
            sx={{ marginBottom: 4 }}
          >
            Add Row
          </Button>
          <Button
            variant="outlined"
            color="secondary"
            onClick={deleteTimeRangeTrafficRow}
            sx={{ marginBottom: 4 }}
          >
            Delete Last Row
          </Button>
        </Stack>

        <Box textAlign="center" mt={4}>
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </Box>

        {networkGraph && (
          <Box textAlign="center" mt={4}>
            <Typography variant="h5" gutterBottom>
              Network Graph
            </Typography>
            <img
              src={`data:image/png;base64,${networkGraph}`}
              alt="Network Graph"
              style={{ maxWidth: "100%", height: "auto" }}
            />
          </Box>
        )}
      </Container>
    </LocalizationProvider>
  );
}

export default App;
