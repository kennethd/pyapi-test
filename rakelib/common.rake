require 'date'
require 'open3'
require 'tmpdir'

RESET = "\e[0m"
BOLD  = "\e[1m"
BLINK = "\e[5m"
BGBLK = "\e[40m"
BGBLU = "\e[44m"
BGCYN = "\e[46m"
BGGRN = "\e[42m"
BGRED = "\e[41m"
BGMAG = "\e[45m"
BGWHT = "\e[47m"
BGYEL = "\e[43m"
FGBLK = "\e[30m"
FGBLU = "\e[34m"
FGCYN = "\e[36m"
FGGRN = "\e[32m"
FGRED = "\e[31m"
FGMAG = "\e[35m"
FGWHT = "\e[37m"
FGYEL = "\e[33m"

def run_cmd(cmd)
  # run cmd in subshell & return STDOUT
  # fails if command exits with non-zero status
  # if command produces output on STDERR, echos cmd STDERR to current STDERR
  # if you want to see the streaming output of the commands, use sh() instead
  info("run_cmd: #{cmd}")
  stdout, stderr, status = Open3.capture3(cmd)
  if status.to_s !~ /exit 0/
    fail("COMMAND FAILED (#{status}) #{cmd}")
  end
  if stderr.strip!
    STDERR.puts "#{stderr}"
  end
  if stdout.nil?
    stdout = ""
  end
  return stdout.strip
end

def debug(msg)
  STDERR.puts "#{FGMAG}#{BOLD}#{msg}#{RESET}"
end

def warn(msg)
  STDERR.puts "#{BGCYN}#{FGWHT}#{BOLD}WARNING:#{RESET} #{FGCYN}#{BOLD}#{msg}#{RESET}"
end

def info(msg)
  STDERR.puts "#{FGCYN}#{BOLD}#{msg}#{RESET}"
end

def err(msg)
  STDERR.puts "#{FGRED}#{BOLD}#{msg}#{RESET}"
end
