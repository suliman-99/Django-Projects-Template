import os

def delete_migration_files():
    # Get all app directories in the project
    apps_dir = os.path.join(os.getcwd())
    app_dirs = [d for d in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, d))]

    # Delete migration files from each app directory
    for app_dir in app_dirs:
        migration_dir = os.path.join(apps_dir, app_dir, 'migrations')
        try:
            migration_files = [f for f in os.listdir(migration_dir) if f.endswith('.py') and f != '__init__.py']
            for file in migration_files:
                os.remove(os.path.join(migration_dir, file))
            # Remove the migration directory if it's empty
            if not os.listdir(migration_dir):
                os.rmdir(migration_dir)
        except:
            pass

if __name__ == '__main__':
    delete_migration_files()
