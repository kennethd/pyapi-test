def pyapp_read_version(version_file)
  maj, min, rev = File.read(version_file).strip.split('.')
  return maj.to_i, min.to_i, rev.to_i
end

def pyapp_write_version(version_file, maj, min, rev)
  ver = "#{maj}.#{min}.#{rev}"
  File.write(version_file, ver)
end

namespace :pkg do
  task :touch_version do
    sh("touch #{VERSION_FILE}")
  end

  desc "bump major version part of MAJ.MIN.REV version string & tag repo"
  task :bumpmaj, [:tag_message] => ['git:assert_clean', 'pkg:touch_version'] do |t, args|
    STDERR.puts "#{t.name} #{args.tag_message}"
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    pyapp_write_version(VERSION_FILE, maj + 1, 0, 0)
    Rake::Task['pkg:tagver'].invoke
    Rake::Task['pkg:showver'].invoke
  end

  desc "bump minor version part of MAJ.MIN.REV version string & tag repo"
  task :bumpmin, [:tag_message] => ['git:assert_clean', 'pkg:touch_version'] do |t, args|
    STDERR.puts "#{t.name} #{args.tag_message}"
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    pyapp_write_version(VERSION_FILE, maj, min + 1, 0)
    Rake::Task['pkg:tagver'].invoke
    Rake::Task['pkg:showver'].invoke
  end

  desc "bump revision part of MAJ.MIN.REV version string & tag repo"
  task :bumprev, [:tag_message] => ['git:assert_clean', 'pkg:touch_version'] do |t, args|
    STDERR.puts "#{t.name} #{args.tag_message}"
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    pyapp_write_version(VERSION_FILE, maj, min, rev + 1)
    Rake::Task['pkg:tagver'].invoke
    Rake::Task['pkg:showver'].invoke
  end

  desc "print package version"
  task :showver => [:touch_version] do |t|
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    STDOUT.puts "#{maj}.#{min}.#{rev}"
  end

  # please do not invoke this task manually as part of your regular workflow,
  # this task is designed to be invoked by the :bump* tasks above, each of
  # which depend on git:assert_clean to assure isolation of version-bump commits
  task :tagver, [:tag_message] do |t, args|
    STDERR.puts "#{t.name} #{args.tag_message}"
    maj, min, rev = pyapp_read_version(VERSION_FILE)
    tag = "v#{maj}.#{min}.#{rev}"
    msg = "bump pkg version #{tag}"
    Rake::Task['git:commit_all'].invoke(msg)
    Rake::Task['git:tag'].invoke(tag)
    Rake::Task['git:push_tags'].invoke
  end
end

