document.addEventListener("DOMContentLoaded", function () {
  const audioPlayers = document.querySelectorAll(".audio-player");
  let currentSongIndex = 0;

  function playNextSong() {
    // Move to the next song
    currentSongIndex = (currentSongIndex + 1) % audioPlayers.length;

    // Play the next song
    audioPlayers[currentSongIndex].play();
  }

  // Add event listeners to play the next song when the current one can play through
  audioPlayers.forEach(function (audioPlayer) {
    audioPlayer.addEventListener("canplaythrough", playNextSong);
  });

  // Start playing the first song
  audioPlayers[currentSongIndex].play();
});
