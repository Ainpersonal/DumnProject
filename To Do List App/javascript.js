document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const TaskList = document.getElementById('task-list');
    const emptyImage = document.querySelector('.empty-image');
    const todosContainer = document.querySelector('.todos-container');
    const progressBar = document.getElementById('progress');
    const progressNumbers = document.getElementById('numbers');

    const toggleEmptyState = () => {
        emptyImage.style.display = TaskList.children.length === 0 ? 'block' : 'none';
        todosContainer.style.width = TaskList.children.length > 0 ? '100%' : '50%';
    };

    const updateProgress = () => {
        const totalTasks = TaskList.children.length; 
        const completedTasks = TaskList.querySelectorAll('.checkbox:checked').length;
        progressBar.style.width = totalTasks ? `${(completedTasks / totalTasks) * 100}%` : '0%';
        progressNumbers.textContent = `${completedTasks} / ${totalTasks}`;
    };

    const addTask = (text, completed = false) => {
        const taskText = text || taskInput.value.trim();
        if (!taskText) return;

        const li = document.createElement('li');
        li.innerHTML = `
            <input type="checkbox" class="checkbox" ${completed ? 'checked' : ''} />
            <span>${taskText}</span>
            <div class="task-buttons">
                <button class="edit-btn"><i class="fa-solid fa-pen"></i></button>
                <button class="delete-btn"><i class="fa-solid fa-trash"></i></button>
            </div>`;

        const checkbox = li.querySelector('.checkbox');
        const editBtn = li.querySelector('.edit-btn');
        const deleteBtn = li.querySelector('.delete-btn');

        if (completed) {
            li.classList.add('completed');
            editBtn.disabled = true;
            editBtn.style.opacity = '0.5';
            editBtn.style.pointerEvents = 'none';
        }

        checkbox.addEventListener('change', () => {
            const isChecked = checkbox.checked;
            li.classList.toggle('completed', isChecked);
            editBtn.disabled = isChecked;
            editBtn.style.opacity = isChecked ? '0.5' : '1';
            editBtn.style.pointerEvents = isChecked ? 'none' : 'auto';
            updateProgress();
        });

        editBtn.addEventListener('click', () => {
            if (!checkbox.checked) {
                li.classList.add('fall');
                li.addEventListener('transitionend', () => {
                    li.remove();
                    toggleEmptyState();
                    updateProgress();
                });
                taskInput.value = li.querySelector('span').textContent;
            }
        });

        // --- ANIMASI DELETE ---
        deleteBtn.addEventListener('click', () => {
            li.classList.add('fall');
            li.addEventListener('transitionend', () => {
                li.remove();
                toggleEmptyState();
                updateProgress();
            });
        });

        TaskList.appendChild(li);
        taskInput.value = '';
        toggleEmptyState();
        updateProgress();
    };

    addTaskBtn.addEventListener('click', (e) => {
        e.preventDefault();
        addTask();
    });

    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addTask();
        }
    });
});