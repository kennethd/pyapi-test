def git_current_branch()
  return run_cmd("git branch --show-current")
end

def git_current_hash()
  return run_cmd("git rev-parse --short HEAD")
end

def git_newest_tag()
  hash = run_cmd("git rev-list --tags --max-count=1")
  return run_cmd("git describe --tags '#{hash}'")
end

def git_remote_rev(repo, branch)
  return run_cmd("git ls-remote #{repo} #{branch} | cut -f1")
end

namespace :git do
  # This task fails if there are uncommitted changes to working dir
  task :assert_clean do |t|
    STDERR.puts t.name
    stdout = run_cmd("git status --short --untracked-files=no")
    unless stdout.to_s.strip.empty?
      fail("It appears you have uncommitted changes:\n\n#{stdout}\n\n")
    end
  end

  desc "does git pull --rebase in a manner consistent with never having merge commits"
  task :up, [:remote, :branch] do |t, args|
    # by default uses whatever you've --set-upstream-to=highball/master
    args.with_defaults(:remote => "", :branch => "")
    run_cmd("git pull --rebase --autostash #{args.remote} #{args.branch}")
  end

  desc "create tar.gz distribution of working dir

  fails if there are uncommitted changes to working dir

  resulting file does not include git history, etc. see git:tar_workdir

  :branch   default is current branch
  :dest     directory to write archive to; default ./build"
  task :archive, [:branch, :dest] => [:assert_clean] do |t, args|
    args.with_defaults(:branch => "current", :dest => "./build")
    STDERR.puts "#{t.name} #{args.branch} #{args.dest}"
    if args.branch == "current"
      branch = git_current_branch
    else
      branch = args.branch
    end
    repo_name = File.basename(Rake.original_dir)
    FileUtils.mkdir args.dest unless Dir.exist?(args.dest)
    STDERR.puts "#{t.name} #{repo_name} #{args.branch}->#{branch} #{args.dest}"
    sh([
      "git archive",
      "--format tar.gz",
      "--output #{args.dest}/#{repo_name}-#{branch.sub('/', '-').downcase}.tar.gz",
      branch
    ].join(" "))
  end

#  desc "create tar.gz file of remote repo
#
#  :repo     url or path to repo
#  :branch   default is 'master'
#  :dest     directory to write archive to; default ./build"
  task :archive_remote, [:repo, :branch, :dest] do |t, args|
    args.with_defaults(:branch => "master", :dest => "./build")
    raise ArgumentError, ":repo is required" if args.repo.nil?
    repo_name = File.basename(args.repo).sub(/\.git$/, '')
    FileUtils.mkdir args.dest unless Dir.exist?(args.dest)
    STDERR.puts "t.name #{repo_name} #{args.repo} #{args.branch} #{args.dest}"
    sh([
      "git archive",
      "--remote=#{args.repo}",
      "--format tar.gz",
      "--output #{args.dest}/#{repo_name}-#{args.branch.downcase}.tar.gz",
      args.branch
    ].join(" "))
  end

#  desc "copy single file from remote repo to local path"
  task :cp, [:repo, :branch, :remote_path, :local_path] do |t, args|
    raise ArgumentError, ":repo is required" if args.repo.nil?
    raise ArgumentError, ":branch is required" if args.branch.nil?
    raise ArgumentError, ":remote_path is required" if args.remote_path.nil?
    raise ArgumentError, ":local_path is required" if args.local_path.nil?
    STDERR.puts "#{t.name} #{args.repo} #{args.branch} #{args.remote_path} -> #{args.local_path}"
    # git archive --format=tar --remote=$GIT_REPO master requirements.txt \
    #     | tar -x --to-stdout >./build/branch.requirements.txt
    sh([
      "git archive",
      "--remote '#{args.repo}'",
      "--format tar",
      "'#{args.branch}'",
      "'#{args.remote_path}'",
      "| tar -x --to-stdout",
      ">'#{args.local_path}'",
    ].join(" "))
  end

  # please do not use this as part of your everyday workflow to make commits,
  # this exists to allow the pyapp:tagver task to control flow of events when
  # bumping a version & creating a new tag, commit & push
  task :commit_all, [:commit_message] do |t, args|
    STDERR.puts "#{t.name} #{args.commit_message}"
    raise ArgumentError, ":commit_message required" if args.commit_message.nil?
    run_cmd("git commit -a -m \"#{args.commit_message}\"")
  end
  # :push_tags is partner of :commit_all in support for pyapp:tagver
  task :push_tags do |t|
    STDERR.puts t.name
    run_cmd("git push --tags")
  end

  # git:tag is needed by version management tasks
  task :tag, [:tag_name, :tag_message] do |t, args|
    raise ArgumentError, ":tag_name required" if args.tag_name.nil?
    STDERR.puts "#{t.name} #{args.tag_name} #{args.tag_message}"
    # annotated or lightweight?
    # https://git-scm.com/book/en/v2/Git-Basics-Tagging
    annotated = args.tag_message.nil? ? "" : "-a"
    message = args.tag_message.nil? ? "" : "-m \"#{args.tag_message}\""
    run_cmd("git tag #{annotated} #{args.tag_name} #{message}")
  end

#  desc "list git tags"
  task :list_tags do |t|
    STDERR.puts t.name
    sh("git tag -n --sort=committerdate")
  end
end
