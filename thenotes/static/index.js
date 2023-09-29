function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');
  const toggleSwitch = document.querySelector('.toggle-switch');
  toggleSwitch.style.transform = body.classList.contains('dark-mode') ?
  'translateX(30px)' : 'translateX(0)';
}

function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const utcTimestamps = document.querySelectorAll('.note-date[data-utc]');
    utcTimestamps.forEach(function (element) {
        const utcString = element.getAttribute('data-utc');
        const utcDate = new Date(utcString);
        const localDateString = utcDate.toLocaleString();
        element.textContent = `Created on: ${localDateString}`;
    });
});