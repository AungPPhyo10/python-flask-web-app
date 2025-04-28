function deleteNote(noteId) {
    fetch('delete-note', {
        method: 'DELETE',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = '/notes';
    }).catch((error) => {
        alert('Error deleting note: ' + error);
        console.error('Error deleting note:', error);
    });
}