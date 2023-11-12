# ----- Prefix -----
docker_prefix := 'docker compose -f development.yml --env-file .env'
python_docker_prefix := 'docker compose -f development.yml --env-file .env run --no-deps --rm app'
python_docker_with_deps_prefix := 'docker compose -f development.yml --env-file .env run --rm app'

# ---- Docker compose checking ------
compose_running_services := `docker compose -f development.yml ps --services --filter "status=running"`
compose_services := `docker compose -f development.yml ps --services -a`
compose_all_services := if compose_services == "" { "There're no services running" } else { compose_services }


# ----- Colors -----
green := if os_family() == "unix" { `tput -Txterm setaf 2` } else { "" }
yellow := if os_family() == "unix" { `tput -Txterm setaf 3` } else { "" }
reset := if os_family() == "unix" { `tput -Txterm sgr0` } else { "" }


# ----- Just Commands -----
# List available commands
@_default:
  just -l

@_info_msg message:
  echo "{{ yellow }}[!]{{ reset }} {{ message }}..."

@_success_msg message:
  echo "{{ green }}[+]{{ reset }} {{ message }}\n"

@_check_compose_is_running:
  {{ if compose_running_services != compose_all_services { error("Docker compose are not running. Please run `just start` before running this command.") } else {""} }}

# ----- Formatting -----

# Format HTML source code with djLint
@format_html:
  just _info_msg "Formatting HTML using djLint"
  {{ python_docker_prefix }} djlint . --reformat --quiet
  just _success_msg "HTML formatted with djLint successfully!"

# Format Python source code with Black
@format_python:
  just _info_msg "Formatting Python source code using Black"
  {{ python_docker_prefix }} black .
  just _success_msg "Python source code formatted with Black successfully!"

# Format Python imports with isort
@format_python_imports:
  just _info_msg "Formatting Python imports using isort"
  {{ python_docker_prefix }} isort .
  just _success_msg "Python imports formatted with isort successfully!"

# Format everything
format: format_python format_python_imports format_html

# ----- Linting -----

# Lint Python source code with Black and Ruff
@lint_python:
  just _info_msg "Linting Python source code using Black"
  {{ python_docker_prefix }} black . --check
  just _success_msg "Python source code linted with Black successfully!"

  just _info_msg "Linting Python source code using Ruff"
  {{ python_docker_prefix }} ruff .
  just _success_msg "Python source code linted with Ruff successfully!"

# Lint Python imports with isort
@lint_python_imports:
  just _info_msg "Linting Python imports using isort"
  {{ python_docker_prefix }} isort --check-only --diff .
  just _success_msg "Python imports linted with isort successfully!"

# Scan Python source code with Bandit for security issues
@lint_python_security:
  just _info_msg "Scanning Python source code for security issues using Bandit"
  {{ python_docker_prefix }} bandit -c pyproject.toml -r .
  just _success_msg "Python source code scanned with Bandit successfully! (No issues found)"

# Check for missing Django database model migrations
@lint_django_migrations:
  just _info_msg "Checking for missing Django database model migrations"
  just _check_compose_is_running
  {{ python_docker_with_deps_prefix }} python3 ./manage.py makemigrations --check --dry-run
  just _success_msg "No missing Django database model migrations found!"

# Lint HTML source code with djLint
@lint_html:
  just _info_msg "Linting HTML using djLint"
  {{ python_docker_prefix }} djlint . --lint
  just _success_msg "HTML linted with djLint successfully!"

# Lint everything
lint: lint_python lint_python_imports lint_python_security lint_html

# ----- Testing -----

# Run the Django test runner without coverage
@test +FLAGS="":
  just _info_msg "Running the Django test runner (pytest)"
  just _check_compose_is_running
  {{ python_docker_prefix }} pytest {{ FLAGS }}

# Run all the basics tools for a safe commit
precommit: format lint test


# ----- Docker ------

# Start all Docker containers
@start DETACH_FLAG="":
  {{ if DETACH_FLAG == "" {""} else if DETACH_FLAG == "-d" {""} else { error("Only '-d' flag is allowed for this recipe.") } }}
  {{ docker_prefix }} up --build  {{ DETACH_FLAG }}

# Stop all Docker containers
@stop:
  {{ docker_prefix }} down

# Run the Django development server
@runserver:
  just _check_compose_is_running
  {{ docker_prefix }} exec -it app runserver

# Run a shell into the Django container
@shell:
  just _check_compose_is_running
  {{ docker_prefix }} exec -it app bash
