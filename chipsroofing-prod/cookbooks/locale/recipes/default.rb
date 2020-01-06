#
# Cookbook Name:: postgresql
# Recipe:: default
#

execute "echo 'ru_RU.UTF8 UTF-8' >> /etc/locale.gen"
execute "locale-gen"