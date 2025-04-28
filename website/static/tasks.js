function deleteTask(taskId) {
    fetch('/tasks/delete', {
        method: 'DELETE',
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        window.location.href = '/tasks';
    }).catch((error) => {
        alert('Error deleting task: ' + error);
        console.error('Error deleting task:', error);
    });
}

function updateTask(taskId, title, description) {
    document.getElementById('modal-task-id').value = taskId;
    document.getElementById('modal-task-title').value = title;
    document.getElementById('modal-task-description').value = description;
  
    $('#updateTaskModal').modal('show');
}

function submitUpdate() {
    const taskId = document.getElementById('modal-task-id').value;
    const title = document.getElementById('modal-task-title').value;
    const description = document.getElementById('modal-task-description').value;

    fetch('/tasks/update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        taskId: taskId,
        title: title,
        description: description
      })
    })
    .then((_res) => {
        console.log('Task updated successfully!');
        window.location.href = '/tasks';
    })
    .catch((error) => {
        alert('Error deleting task: ' + error);
        console.error('Error deleting task:', error);
    });
}