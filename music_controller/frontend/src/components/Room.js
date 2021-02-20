import React, { useEffect, useState } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import SettingsIcon from "@material-ui/icons/Settings";
import { CreateRoomPage } from "./CreateRoomPage";

export function Room(props) {
  const roomCode = props.match.params.roomCode;
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [isHost, setIsHost] = useState(false);
  const [votesToSkip, setVotes] = useState(1);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    getRoomDetails();
  }, []);

  const getRoomDetails = () => {
    fetch(`/api/get-room?code=${roomCode}`)
      .then((resp) => {
        if (!resp.ok) {
          props.leaveRoom();
          props.history.push("/");
        }
        return resp.json();
      })
      .then((data) => {
        setVotes(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
      });
  };

  const leaveButtonPressed = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room", requestOptions).then((resp) => {
      props.leaveRoom();
      props.history.push("/");
    });
  };

  const renderSettings = () => {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            votesToSkip={votesToSkip}
            guestCanPause={guestCanPause}
            roomCode={roomCode}
            updateCallback={() => {
              console.log("Hello World!!");
            }}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" onClick={closeSettings}>
            Close Settings
          </Button>
        </Grid>
      </Grid>
    );
  };

  const settingsButtonPressed = () => {
    setShowSettings(true);
  };

  const closeSettings = () => {
    setShowSettings(false);
  };

  if (showSettings) {
    return renderSettings();
  }
  return (
    <Grid container spacing={1}>
      {isHost ? (
        <Grid item container xs={12} justify="flex-end">
          <Button onClick={settingsButtonPressed}>
            <SettingsIcon aria-describedby="Settings Icon" />
          </Button>
        </Grid>
      ) : null}
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Code: {roomCode}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Votes: {votesToSkip}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Guest Can Pause: {guestCanPause.toString()}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Host: {isHost.toString()}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="secondary"
          onClick={leaveButtonPressed}
        >
          Leave Room
        </Button>
      </Grid>
    </Grid>
  );
}
