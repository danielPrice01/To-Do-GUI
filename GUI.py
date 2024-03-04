import customtkinter

# importance, hours, calculated priority
tasks_dictionary = {}


def load_tasks():
    global tasks_dictionary
    tasks_dictionary = {}

    with open("current_list", "r") as file_r:
        tasks_list = file_r.read().splitlines()

    for item in tasks_list:
        item_data = item.strip(" ").split(",")
        name = item_data[0]
        # importance, hours, priority
        data_points = item_data[1:]
        tasks_dictionary[name] = data_points


def sort_tasks():
    global tasks_dictionary

    for task in tasks_dictionary:
        tasks_dictionary[task][2] = int(float(tasks_dictionary[task][0]) / float(tasks_dictionary[task][1]))

    # Sort the dictionary based on the value at index 2 (priority)
    sorted_tasks = sorted(tasks_dictionary.items(), key=lambda x: x[1][2], reverse=True)
    for i, (task, _) in enumerate(sorted_tasks, start=1):
        tasks_dictionary[task][2] = i

    with open("current_list", "w") as file_w:
        for task_name, task_data in sorted_tasks:
            [importance, hours, priority] = task_data
            file_w.write(f"{task_name},{importance},{hours}, {priority}\n")


def add_tasks_to_dict(name, importance, hours):
    global tasks_dictionary

    if name not in tasks_dictionary:
        tasks_dictionary[name] = [importance, hours, "0"]

    sort_tasks()


def edit_tasks_in_dict(name, importance, hours):
    global tasks_dictionary

    if name in tasks_dictionary:
        del tasks_dictionary[name]
        add_tasks_to_dict(name, importance, hours)

    sort_tasks()


def remove_tasks_in_dict(name):
    global tasks_dictionary

    if name in tasks_dictionary:
        del tasks_dictionary[name]

    sort_tasks()


class ToDoListApp:
    def __init__(self):
        # Initializes the To-Do List application, setting up the main GUI window and initial state.
        # Loads the current tasks and sets the color theme.
        self.app = customtkinter.CTk()
        self.app.geometry("500x600")
        self.app.title("To Do List")

        self.can_add_tasks = False
        self.can_edit_tasks = "disabled"
        self.can_remove_tasks = False

        self.background_color = "blue"
        self.light_blue = "#1f69a5"
        self.dark_blue = "#144870"

        self.add_button_color = self.light_blue
        self.edit_button_color = self.light_blue
        self.remove_button_color = self.light_blue

        self.load_current_tasks()

        self.tasks_to_be_removed = []
        self.task_to_be_added = {}

        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme(self.background_color)  # Themes: blue (default), dark-blue, green

    def add_tasks(self):
        # Handles the Add Tasks button functionality.
        # Toggles between adding tasks and displaying the current tasks.
        if self.can_edit_tasks == "disabled" and not self.can_remove_tasks:
            self.can_add_tasks = not self.can_add_tasks

            if self.can_add_tasks:
                self.add_button_color = self.dark_blue

                self.load_edit_screen("Add Task")

            elif not self.can_add_tasks:
                self.add_button_color = self.light_blue
                self.load_current_tasks()

    def edit_tasks(self):
        # Handles the Edit Tasks button functionality.
        # Toggles between enabling and disabling the ability to edit tasks.
        if not self.can_add_tasks and not self.can_remove_tasks:
            if self.can_edit_tasks == "disabled":
                self.can_edit_tasks = "normal"
                self.edit_button_color = self.dark_blue
            elif self.can_edit_tasks == "normal":
                self.can_edit_tasks = "disabled"
                self.edit_button_color = self.light_blue

            self.load_current_tasks()

        else:
            self.can_edit_tasks = "disabled"
            self.edit_button_color = self.light_blue

    def remove_tasks(self):
        # Handles the Remove Tasks button functionality.
        # Toggles between selecting and deselecting tasks for removal.
        if not self.can_add_tasks and self.can_edit_tasks == "disabled":
            self.can_remove_tasks = not self.can_remove_tasks

            if self.can_remove_tasks:
                self.remove_button_color = self.dark_blue
            elif not self.can_remove_tasks:
                self.remove_button_color = self.light_blue

            self.load_current_tasks()

    def back_to_previous_state(self):
        # should only fully reset for add tasks
        # for edit tasks, go back to the edit screen, reset all checkboxes
        self.reset_default_state()
        self.load_current_tasks()

    def save_state(self):
        # if add_tasks then add the task
        # if edit_tasks then edit the task
        # if remove_tasks then remove the tasks
        global tasks_dictionary

        if self.can_add_tasks:
            added_task_name = list(self.task_to_be_added.keys())[0]
            added_task_details = self.task_to_be_added[added_task_name]
            add_tasks_to_dict(added_task_name, added_task_details[0], added_task_details[1])

        elif self.can_edit_tasks == "normal":
            added_task_name = list(self.task_to_be_added.keys())[0]
            added_task_details = self.task_to_be_added[added_task_name]
            edit_tasks_in_dict(added_task_name, added_task_details[0], added_task_details[1])

        elif self.can_remove_tasks:
            for remove_task in self.tasks_to_be_removed:
                remove_tasks_in_dict(remove_task)

        self.reset_default_state()
        self.load_current_tasks()

    def reset_checkbox(self):
        # Resets the checkboxes in the Remove Tasks screen.
        self.load_current_tasks()

    def reset_default_state(self):
        # Resets the application to its default state.
        self.can_add_tasks = False
        self.can_edit_tasks = "disabled"
        self.can_remove_tasks = False

        self.background_color = "blue"
        self.light_blue = "#1f69a5"
        self.dark_blue = "#144870"

        self.add_button_color = self.light_blue
        self.edit_button_color = self.light_blue
        self.remove_button_color = self.light_blue

    def clear_canvas(self):
        # Clears all widgets from the GUI canvas.
        for widget in self.app.winfo_children():
            widget.destroy()

    def load_edit_screen(self,
                         action_performed,
                         task_description="Please Entire a Task Description",
                         importance="1",
                         hours_to_complete="1"):

        # Loads the screen for adding, editing, or removing tasks.
        # Displays input fields and buttons based on the chosen action.
        # Logic for handling user input and saving changes is implemented in the inner_save_state function.
        self.clear_canvas()
        self.task_to_be_added = {}
        self.tasks_to_be_removed = []

        title = customtkinter.CTkLabel(self.app, text=action_performed, font=("Arial", 32), compound="center")
        title.pack(pady=10)

        if action_performed != "Remove Tasks":
            # task detail changers

            textbox = customtkinter.CTkTextbox(self.app, width=300, height=300)
            textbox.insert("0.0", task_description)
            textbox.configure(state="normal")
            textbox.pack(pady=10)

            importance_frame = customtkinter.CTkFrame(self.app, width=300, height=50)
            importance_frame.pack(pady=10)

            importance_label = customtkinter.CTkLabel(importance_frame, text="Importance:",
                                                      font=("Arial", 16), width=145)
            importance_label.pack(side="left")

            importance_space_frame = customtkinter.CTkFrame(importance_frame, width=10, height=0)
            importance_space_frame.pack(side="left")

            importance_options = [str(i) for i in range(1, 11)]
            importance_menu = customtkinter.CTkOptionMenu(importance_frame,
                                                          values=importance_options, width=145, height=25)
            importance_menu.set(importance)
            importance_menu.pack(side="left")

            hours_frame = customtkinter.CTkFrame(self.app, width=300, height=50)
            hours_frame.pack(pady=10)

            hours_label = customtkinter.CTkLabel(hours_frame, text="Hours to Complete:", font=("Arial", 16), width=145)
            hours_label.pack(side="left")

            hours_space_frame = customtkinter.CTkFrame(hours_frame, width=10, height=0)
            hours_space_frame.pack(side="left")

            hours_entry = customtkinter.CTkEntry(hours_frame, placeholder_text=hours_to_complete, width=145)
            hours_entry.pack(side="left")

        button_frame = customtkinter.CTkFrame(self.app, width=200, height=50)
        button_frame.pack(pady=30, side="bottom")

        back_button = customtkinter.CTkButton(button_frame, text="Back", command=self.back_to_previous_state)
        back_button.pack(side="left")

        button_space_frame = customtkinter.CTkFrame(button_frame, width=5, height=0)
        button_space_frame.pack(side="left")

        if action_performed == "Remove Tasks":
            reset_button = customtkinter.CTkButton(button_frame, text="Reset", command=self.reset_checkbox)
            reset_button.pack(side="left")

            button_space_frame2 = customtkinter.CTkFrame(button_frame, width=5, height=0)
            button_space_frame2.pack(side="left")

        def inner_save_state():
            if action_performed != "Remove Tasks":
                added_task_name = textbox.get("0.0", "end").strip("\n")
                added_task_importance = importance_menu.get()

                if hours_entry.get() != "":
                    added_task_hours = hours_entry.get()
                else:
                    added_task_hours = hours_to_complete

                self.task_to_be_added[added_task_name] = [added_task_importance, added_task_hours]

            self.save_state()

        save_button = customtkinter.CTkButton(button_frame, text="Save", command=inner_save_state)
        save_button.pack(side="left")

    def load_current_tasks(self):
        # Loads the main screen with the list of current tasks.
        # Allows the user to interact with checkboxes for editing or removing tasks.
        # Logic for checkbox functionality and navigation to edit or remove screens is implemented here.
        global tasks_dictionary

        self.clear_canvas()
        self.tasks_to_be_removed = []

        title = customtkinter.CTkLabel(self.app, text="To Do List", font=("Arial", 32), compound="center")
        title.pack(pady=10)

        button_frame = customtkinter.CTkFrame(self.app, width=200, height=50)
        button_frame.pack()

        add_button = customtkinter.CTkButton(button_frame, text="Add", command=self.add_tasks,
                                             fg_color=self.add_button_color)
        add_button.pack(side="left")

        space_frame1 = customtkinter.CTkFrame(button_frame, width=5, height=0)
        space_frame1.pack(side="left")

        edit_button = customtkinter.CTkButton(button_frame, text="Edit", command=self.edit_tasks,
                                              fg_color=self.edit_button_color)
        edit_button.pack(side="left")

        space_frame2 = customtkinter.CTkFrame(button_frame, width=5, height=0)
        space_frame2.pack(side="left")

        remove_button = customtkinter.CTkButton(button_frame, text="Remove", command=self.remove_tasks,
                                                fg_color=self.remove_button_color)
        remove_button.pack(side="left")

        space_frame2 = customtkinter.CTkFrame(self.app, width=5, height=0)
        space_frame2.pack(pady=10)

        if self.can_remove_tasks:
            button_frame = customtkinter.CTkFrame(self.app, width=200, height=50)
            button_frame.pack(pady=30, side="bottom")

            reset_button = customtkinter.CTkButton(button_frame, text="Reset", command=self.reset_checkbox)
            reset_button.pack(side="left")

            button_space_frame = customtkinter.CTkFrame(button_frame, width=5, height=0)
            button_space_frame.pack(side="left")

            save_button = customtkinter.CTkButton(button_frame, text="Save", command=self.save_state)
            save_button.pack(side="left")

        for task in tasks_dictionary.keys():
            textbox_frame = customtkinter.CTkFrame(self.app, width=200, height=50)
            textbox_frame.pack()

            # Define a function that generates the command for each checkbox
            def edit_checkbox_command(curr_task=task):
                return lambda: self.load_edit_screen(
                    "Edit Task", curr_task, tasks_dictionary[curr_task][0],
                    tasks_dictionary[curr_task][1])

            def remove_checkbox_command(curr_task=task):
                return lambda: self.tasks_to_be_removed.append(curr_task)

            if self.can_edit_tasks == "normal":
                # task_description, importance, hours_to_complete
                checkbox = customtkinter.CTkCheckBox(textbox_frame, text="", width=5, command=edit_checkbox_command())
                checkbox.pack(side="left")
            elif self.can_remove_tasks:
                checkbox = customtkinter.CTkCheckBox(textbox_frame, text="", width=5, command=remove_checkbox_command())
                checkbox.pack(side="left")

            if len(task) / 20 < 1:
                textbox_height = 25 * 1
            else:
                textbox_height = 25 * round(len(task) / 50 + 1)

            textbox = customtkinter.CTkTextbox(textbox_frame, width=300, height=textbox_height)
            textbox.insert("0.0", task)
            textbox.configure(state=str(self.can_edit_tasks))
            textbox.pack()

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    load_tasks()
    sort_tasks()
    todo_app = ToDoListApp()
    todo_app.run()
