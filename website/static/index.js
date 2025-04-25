function deleteNote(noteId) {
    fetch('delete-note', {
        method: 'DELETE',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = '/';
    });
}