import threading
import time

class TaskScheduler:
    def __init__(self):
        self.tasks = []  # List to hold task information
        self.running = True  # Flag to control task execution

    def add_task(self, task_function, interval_seconds):
        """Add a task to the scheduler."""
        task = {
            'function': task_function,
            'interval': interval_seconds,
            'last_run': time.time()  # Track when the task was last run
        }
        self.tasks.append(task)

    def remove_task(self, task_function):
        """Remove a task from the scheduler by its function."""
        self.tasks = [task for task in self.tasks if task['function'] != task_function]

    def run_task(self, task):
        """Run the task and wait for the next interval."""
        while self.running:
            current_time = time.time()
            # If the interval has passed since last run, execute the task
            if current_time - task['last_run'] >= task['interval']:
                task['function']()  # Execute the task
                task['last_run'] = current_time  # Update last run time
            time.sleep(1)  # Sleep for a second before checking again

    def start(self):
        """Start all tasks in separate threads."""
        for task in self.tasks:
            thread = threading.Thread(target=self.run_task, args=(task,))
            thread.daemon = True  # Daemonize the thread so it exits when the main program exits
            thread.start()

    def stop(self):
        """Stop the scheduler."""
        self.running = False


# Sample tasks to be executed
def task1():
    print("Executing Task 1: Task is running every 5 seconds")

def task2():
    print("Executing Task 2: Task is running every 3 seconds")

def task3():
    print("Executing Task 3: Task is running every 7 seconds")

# Main program to run the scheduler
if __name__ == "__main__":
    scheduler = TaskScheduler()

    # Adding tasks with different intervals
    scheduler.add_task(task1, 5)  # Run task1 every 5 seconds
    scheduler.add_task(task2, 3)  # Run task2 every 3 seconds
    scheduler.add_task(task3, 7)  # Run task3 every 7 seconds

    # Start the task scheduler
    scheduler.start()

    # Keep the program running to allow tasks to execute
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler is stopping...")
        scheduler.stop()
