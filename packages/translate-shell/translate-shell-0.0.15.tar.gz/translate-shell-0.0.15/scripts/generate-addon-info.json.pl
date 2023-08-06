#!/usr/bin/env -S perl -pi
BEGIN {
    # https://github.com/actions/checkout/issues/1190
    $version = `git describe --abbrev=0`;
    chomp $version;
}
unless ( $#ARGV < 0 ) {
    $name        = $1 if /^name = "([^"]*+)"/;
    $description = $1 if /^description = "([^"]*+)"/;
    $url         = $1 if /^Source = "([^"]*+)"/;
    $author      = "$1 <$2>"
      if /^authors = \[\{ name = "([^"]*+)", email = "([^"]*+)" }]/;
    next;
}
s/(?<="name": ")([^"]*+)(?=")/$name/;
s/(?<="description": ")([^"]*+)(?=")/$description/;
s/(?<="version": ")([^"]*+)(?=")/$version/;
s/(?<="author": ")([^"]*+)(?=")/$author/;
s/(?<="url": ")([^"]*+)(?=")/$url/;
