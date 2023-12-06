from app_config.configure import get_application

task_management_system = get_application()

if __name__ == "__main__":
    task_management_system.run(host='0.0.0.0', port=4000, fast=True)
