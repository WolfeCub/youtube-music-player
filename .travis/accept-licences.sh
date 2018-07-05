#!/usr/bin/expect -f

# Usage example:
#  ./accept-licenses "android update sdk --no-ui --all --filter build-tools" "android-sdk-license-bcbbd656|intel-android-sysimage-license-1ea702d1"

set timeout 1800
set cmd [lindex $argv 0]

spawn {*}$cmd
expect {
  "Do you accept the license '*-license-*'*" {
        exp_send "y\r"
        exp_continue
  }
  eof
}

