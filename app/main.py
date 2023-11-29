from config.config import get_application

Task_manager_app = get_application()

if __name__ == "__main__":
    Task_manager_app.run(host='0.0.0.0', port=4000, fast=True)
