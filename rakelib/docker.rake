def propagate_env_vars
  PROPAGATE_VARS.map { |v| ENV[v].nil? ? "" : "--env #{v}=\"#{ENV[v]}\"" }
    .reject { |v| v.empty? }
    .join(" ")
end

def resolve_docker_tag(args_tag)
  # if args.tag was provided, use it, else use env var #{DOCKER_ENV_CUSTOM_TAG}
  tag = (args_tag.nil? or args_tag.empty?) ? ENV[DOCKER_ENV_CUSTOM_TAG] : "#{args_tag}"
  # if neither of those provided a tag value, read VERSION_FILE & use that
  if tag.nil? or tag.empty?
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    tag = "#{maj}.#{min}.#{rev}"
  end
  tag
end

namespace :docker do
  task :require_linux do 
    unames = run_cmd("uname -s")
    if unames != "Linux"
      err("This task requires Linux")
      abort
    end
  end


  #not used for this project#desc "build #{DOCKER_REPO_NAME} image"
  task :build, [:tag] => ["docker:require_linux","git:archive"] do |t, args|
    git_branch = git_current_branch
    tag = resolve_docker_tag(args.tag)
    build_date = Date.today.strftime("%Y-%m-%d")
    cmd = [
      "docker build",
      "--force-rm",  # always remove intermediate containers
      "--no-cache",
      # "--progress plain",
      # --build-arg will not persist in container, but may be referenced in Dockerfile
      "--build-arg PY3VER=#{PY3VER}",
      "--build-arg ARCHIVE_FILE=uh-libs-#{git_branch.sub("/", "-").downcase}.tar.gz",
      "--build-arg #{DOCKER_ENV_VERSION}=#{tag}",
      "--build-arg #{DOCKER_ENV_BUILD_DATE}=#{build_date}",
      "--tag #{DOCKER_REPO_NAME}:#{tag}",
      "."
    ].join(" ")
    sh(cmd)
    Rake::Task["docker:rmi_untagged"].invoke
    Rake::Task["docker:sysinfo"].invoke
  end

  desc "shutdown & remove #{DOCKER_CONTAINER_NAME} container & remove #{DOCKER_REPO_NAME} image"
  task :clean, [:rm_volume] do |t, args|
    # `docker rm -f` exits 0 even if container is not running
    sh("docker rm -f #{DOCKER_CONTAINER_NAME}")
    tag = resolve_docker_tag(nil)
    # ditto `docker rmi -f` exits 0 even if image doesn't exist
    sh("docker rmi -f #{DOCKER_REPO_NAME}:#{tag}")
    sh("docker rmi -f #{DOCKER_REGISTRY}/#{DOCKER_REPO_NAME}:#{tag}")
    if !args.rm_volume.nil? && defined?(DOCKER_VOLUME_NAME) && !DOCKER_VOLUME_NAME.nil?
      sh("docker volume rm -f #{DOCKER_VOLUME_NAME}")
    end
  end

  task :rmi_untagged do |t|
    iids = run_cmd("docker image ls | grep '^<none>' | awk '{print $3;}'")
    warn "iids to rm:\n#{iids}"
    if !iids.nil?
      iids.each_line do |iid|
        sh("docker rmi #{iid.strip} || echo 'could not remove #{iid.strip}; may be in use'")
      end
    end
  end

  desc "reclaim space from old docker objects  WARNING: Destroys things

  There is a risk of data loss if it exists on volumes associated with unused
  containers or obsoleted images."
  task :clean_all do
    sh("docker system df")
    sh("docker container prune -f")
    Rake::Task["docker:rmi_untagged"].invoke
    Rake::Task["docker:sysinfo"].invoke
  end

  desc "display info about docker objects on system"
  task :sysinfo do
    docker_root_dir = run_cmd("docker info 2>/dev/null | grep 'Docker Root Dir' | cut -d: -f2")
    sh("df -h #{docker_root_dir} && echo || echo")
    sh("docker system df -v && echo")
    sh("docker system df    && echo")  # no -v shows "reclaimable"
    # for swarms#sh("echo SERVICES: && docker service ls")
  end
end
