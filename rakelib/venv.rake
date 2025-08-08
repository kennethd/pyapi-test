PY3VER = `python3 -c 'import sys; print(".".join([str(c) for c in sys.version_info[0:2]]))'`.strip

task :require_venv do
  if ENV["VIRTUAL_ENV"].nil? or ENV["VIRTUAL_ENV"].empty?
    err("An active virtualenv is required")
    raise RuntimeError
  end
end

task :require_no_active_venv do
  if !ENV["VIRTUAL_ENV"].nil?
    err("Please deactivate your virtualenv first")
    raise RuntimeError
  end
end

task :rmrf_venv do
  sh("rm -rf ./venv* *.egg-info")
end

namespace :venv do
  desc "clean up working dir"
  task :clean do
    pypaths = [
      "./#{APP_MODNAME}",
      "./tests"
    ].join(" ")

    cmds = [
      "find #{pypaths} -name '*.pyc' -exec rm '{}' \\;",
      "find #{pypaths} -path '*/__pycache__' -exec rmdir '{}' \\+",
      "rm -rf ./build ./dist"
    ].join(" && ")

    sh(cmds)
  end

  desc "clean as well as destroy virtualenv"
  task uninstall: [:clean, :rmrf_venv]

  desc "used to maintain the pip-freeze.txt file

  we do not use requirements.txt files for maintaining lists of dependencies
  or for installation tasks; we do integrate the maintenance of a versioned
  pip-freeze.txt file which is intended to make it obvious when dependencies
  are changing, so they can be reviewed in normal course of a code review"
  task :pip_freeze do
    sh(". ./venv#{PY3VER}/bin/activate && pip freeze | grep -v #{APP_PKGNAME} >pip-freeze-#{PY3VER}.txt")
  end

  desc "Create venv & pip install package & dependencies

  dev_mode installs package as an \"editable developer egg\", which means
  rather than install the package into the venv's site-packages modules
  normally, it installs as a sort of symlink, so changes during development
  take effect without needing to reinstall

  dev_mode also installs unite testing and linting related stuff"
  task :install, [:dev_mode] => [:require_no_active_venv, :uninstall] do |t, args|
    editable_mode = args.dev_mode.nil? ? "" : "-e"
    cmds = [
      "python3 -m venv ./venv#{PY3VER}",
      ". ./venv#{PY3VER}/bin/activate",
      "python3 -m pip install -U pip setuptools wheel build",
      "pip install #{editable_mode} ."
    ].join(" && ")
    sh(cmds)

    if !args.dev_mode.nil?
      cmds = [
        ". ./venv#{PY3VER}/bin/activate",
        "pip install .[dev]"
      ].join(" && ")
      sh(cmds)
    end

    cmds = [
      ". ./venv#{PY3VER}/bin/activate",
      "python -c 'from #{APP_MODNAME} import VERSION; print(VERSION)'"
    ].join(" && ")
    installed_version = run_cmd(cmds)
    info("Installed #{APP_MODNAME} version #{installed_version}")
    Rake::Task["venv:install_opts"].invoke
    Rake::Task["venv:pip_freeze"].invoke
  end

  task :install_opts do
    return if !OPT_DEPS

    install_list = OPT_DEPS.map { |opt| ".[#{opt}]" }.join(" ")
    cmds = [
      ". ./venv#{PY3VER}/bin/activate",
      "pip install #{install_list}",
      "deactivate"
    ].join(" && ")
    sh(cmds)
  end

  desc "run tests & linter"
  task :test, [:exit_on_fail, :pdb] do |t, args|
    # invoking :pip_freeze again here to make it difficult to forget that you
    # have installed something during development
    Rake::Task["venv:pip_freeze"].invoke
    # pytest -x, --exitfirst == stop on first test failure
    x = args.exit_on_fail.nil? ? "" : "--exitfirst"
    pdb = args.pdb.nil? ? "" : "--pdb"
    env = "PYTHONDONTWRITEBYTECODE=1"
    opts = "--cov=#{APP_MODNAME} --verbose --showlocals #{x} #{pdb}"
    sh(". ./venv#{PY3VER}/bin/activate && #{env} pytest #{opts} ./tests")
    sh(". ./venv#{PY3VER}/bin/activate && pyflakes ./#{APP_MODNAME}")
  end
end

namespace :app do
  # undocumented to not clutter `rake -T`
  task :edit do
    prune_list = [
      "   -path ./.git",
      "-o -name '*.jpg'",
      "-o -name '*.png'",
      "-o -name '*.pyc'",
      "-o -name .coverage",
      "-o -name .gitattributes",
      "-o -name .gitignore",
      "-o -name .rake_tasks~",
      "-o -name VERSION",
      "-o -name __init__.py",
      "-o -name pysession.py",
      "-o -name pip-freeze*.txt",
      "-o -name requirements*.txt",
      "-o -name tox.ini",
      "-o -path ./*egg-info",
      "-o -path ./.azuredevops",
      "-o -path ./.bash.d",
      "-o -path ./.pytest_cache",
      "-o -path ./build",
      "-o -path ./dist",
      "-o -path ./venv*",
      "-o -path __pycache__"
    ].join(" ")
    cmd = "vim $(find . \\( #{prune_list} \\) -prune -o -type f -print | sort)"
    sh(cmd)
  end
end
