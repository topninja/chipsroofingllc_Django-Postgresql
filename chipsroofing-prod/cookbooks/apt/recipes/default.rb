#
# Cookbook Name:: apt
# Recipe:: default
#

execute "apt-get-update" do
  command "apt-get update"
  ignore_failure true
end